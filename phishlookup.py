import argparse
import curses
from queue import Queue
import threading
import time
from core.cli import logo
from core.fuzzer import Fuzzer
from core.helpers import setup_logging
from core.scanner import Scanner
from core.tui.tui_controller import ConsoleController

def main(stdscr, args):
    ui_update_queue = Queue()
    controller = ConsoleController(stdscr, ui_update_queue)

    setup_logging(verbosity=args.verbose)

    fuzzer = Fuzzer(args.domain, dictionary_path=args.dictionary, tld_dictionary=args.tld_dictionary, controller=controller)
    permutations = fuzzer.generate_permutations()

    # Pass the same queue to the scanner
    scanner = Scanner(threads=args.threads, output_file=args.output, output_format=args.output_format,
                      available_only=args.available, not_available_only=args.taken, ui_update_queue=ui_update_queue)

    def run_scanner():
        scanner.run_scans(permutations)
        controller.running = False

    scan_thread = threading.Thread(target=run_scanner)
    scan_thread.daemon = True
    scan_thread.start()

    try:
        while controller.running:
            controller.handle_input()  # Handle keypresses to scroll, quit, etc.
            controller.process_queue()  # Process updates from the queue
            controller.render()  # Render the updated results to the screen
            stdscr.refresh()
            time.sleep(0.1)  # Prevent UI from freezing and give time for updates
    except KeyboardInterrupt:
        controller.running = False
    finally:
        scan_thread.join()
        controller.quit_program()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Phishlookup - Advanced phishing detection, domain name permutation, and scanning tool.")
    parser.add_argument('domain', help='Domain name or URL to scan')
    parser.add_argument('-d', '--dictionary', help='Path to dictionary file for additional permutations')
    parser.add_argument('-td', '--tld-dictionary', help='Path to TLD dictionary for TLD permutations')
    parser.add_argument('-t', '--threads', type=int, default=1000, help='Number of threads to use')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('--output-format', choices=['json', 'csv'], default='csv', help='Output format for results (default: csv)')
    parser.add_argument('--only-resolved', action='store_true', help='Show only domains that resolved to an IP')
    parser.add_argument('--available', action='store_true', help='Show only available domains')
    parser.add_argument('--taken', action='store_true', help='Show only taken domains')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity level')
    
    args = parser.parse_args()

    curses.wrapper(main, args)
