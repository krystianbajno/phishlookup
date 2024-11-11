from datetime import date
import random
import os

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLACK_ON_WHITE = "\033[30;47m"

def logo():    
    colors = [
        BOLD + RED,
        BOLD + GREEN,
        BOLD + YELLOW,
        ""
    ]
    
    choice_img = random.choice(IMAGES)
    choice_color = random.choice(colors)
    choice_text = random.choice(TEXTS)
    
    return f"""
{choice_color}{choice_img}{RESET}

{choice_text}

{RED}{BOLD}PHISH :: LOOKUP{RESET} v1.2.0

{BOLD}{GREEN}https://github.com/krystianbajno/phishlookup{RESET}
"""

UPPERCASE_USERNAME = lambda: os.environ.get('USER', os.environ.get("USERNAME")).capitalize()
TEXTS = [
    f"Who are we looking for today, {UPPERCASE_USERNAME()}?",
    f"I am gone phishing, but this bait isn't working yet.",
    f"Hook, line, and sinker? Not so fast, {UPPERCASE_USERNAME()}!",
    f"Beware the phishy waters, {UPPERCASE_USERNAME()}. Navigate carefully.",
    f"Phishing attempts detected.",
    f"No hooks allowed here. Only safe waters for you, {UPPERCASE_USERNAME()}.",
    f"Spot the phish! Today's catch looks a bit... off, {UPPERCASE_USERNAME()}.",
    f"Don't click the bait, even if it sparkles, {UPPERCASE_USERNAME()}.",
    f"The only phishing allowed here is awareness training.",
    f"New bait, same old tricks.",
    f"Fishing for data? Phishing alert, more like!",
    f"Phishing campaign detected. It's time to cast our net.",
    f"Phishing attempts thrive on slips, {UPPERCASE_USERNAME()}.",
    f"Analyzing the bait.",
    f"Not all that glitters is a valid link, {UPPERCASE_USERNAME()}.",
]

IMAGES = [
"""
      /`·.¸
     /¸...¸`:·
 ¸.·´  ¸   `·.¸.·´)
: © ):´;      ¸  {
 `·.¸ `·  ¸.·´\\`·¸)
     `\\\´´\\¸.·´
""",
"""
       .
      ":"
    ___:____     |"\\/"|
  ,'        `.    \\  /
  |  O        \\___/  |
~^~^~^~^~^~^~^~^~^~^~^~^~
""",
"""
  ;,//;,    ,;/
 o:::::::;;///
>::::::::;;\\\\
  ''\\\\\\\'" ';\
""",
"""
 o
o      ______/~/~/~/__           /((
  o  // __            ====__    /_((
 o  //  @))       ))))      ===/__((
    ))           )))))))        __((
    \\\\     \\)     ))))    __===\\ _((
     \\\\_______________====      \\_((
                                 \\((
""",
'''
      _______
 ,-~~~       ~~~-,
(                 )
 \\_-, , , , , ,-_/
    / / | | \\ \\
    | | | | | |
    | | | | | |
   / / /   \\ \\ \\
   | | |   | | |
'''
]