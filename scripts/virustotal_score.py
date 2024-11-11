import asyncio
import argparse
from typing import List, Union
from playwright.async_api import async_playwright

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

class VirusTotalScoreClient:
    async def get_score(self, entity: Union[str, List[str]]) -> List[dict]:
        if isinstance(entity, str):
            entities = [entity]
        else:
            entities = entity

        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            for entity in entities:
                url = f"https://www.virustotal.com/gui/search/{entity}"
                await page.goto(url, wait_until='networkidle')

                score_text = "Error retrieving score"
                original_text = "Error retrieving score"
                try:
                    css_selector = 'div.card-header.hstack.flex-wrap.justify-content-between.gap-2 div.hstack.gap-2.fw-bold'
                    original_text = await page.inner_text(css_selector)
                    if "No security vendors" in original_text:
                        score_text = "0/94"
                    else:
                        parts = original_text.split()
                        score_text = parts[0] if parts else "Error parsing score"
                except Exception:
                    score_text = "Error retrieving score"

                results.append({
                    "subject": entity,
                    "score": score_text.strip(),
                    "message": original_text.strip()
                })

            await context.close()
            await browser.close()

        return results

def parse_input():
    parser = argparse.ArgumentParser(description="Fetch VirusTotal scores.")
    parser.add_argument("entity", nargs="?", help="A single IP, domain, or hash.")
    parser.add_argument("-f", "--file", help="A file containing a list of entities (one per line).")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    elif args.entity:
        return [args.entity]
    else:
        parser.error("Provide an entity or a file.")

async def main():
    entities = parse_input()
    vt_client = VirusTotalScoreClient()
    results = await vt_client.get_score(entities)
    print(f"subject,message,score")
    for result in results:
        color = GREEN if "No security vendors" in result['message'] else RED
        print(f"{result['subject']},{color}{result['message']}{RESET},{result['score']}")

if __name__ == "__main__":
    asyncio.run(main())
