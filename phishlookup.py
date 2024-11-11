import argparse
from core.cli import logo
from core.fuzzer import Fuzzer
from core.helpers import setup_logging
from core.scanner import Scanner

def main():
    print(logo())
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
    setup_logging(verbosity=args.verbose)

    fuzzer = Fuzzer(args.domain, dictionary_path=args.dictionary, tld_dictionary=args.tld_dictionary)
    permutations = fuzzer.generate_permutations()

    scanner = Scanner(permutations, threads=args.threads, output_file=args.output, output_format=args.output_format,
                      available_only=args.available, not_available_only=args.taken)
    scanner.run_scans()

if __name__ == '__main__':
    main()