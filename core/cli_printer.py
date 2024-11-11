import sys

class ConsolePrinter:
    def __init__(self):
        self.header_printed = False
        self.last_status_length = 0

    def print_header(self):
        if not self.header_printed:
            headers = f"{'Domain':<50} | {'Available':<21} | {'IP Address':<15} | {'GeoLookup':<30} | {'Punycode':<8} | {'WHOIS Status'}"
            separator = "-" * len(headers)
            print(headers)
            print(separator)
            self.header_printed = True

    def print_result(self, result):
        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'

        color = GREEN if result['is_available'] == "AVAILABLE" else RED
        availability = f"{color}{result['is_available']}{RESET}"

        decoded_domain = result['domain']
        if result['punycode'] == "Y":
            try:
                import idna
                decoded_domain = f"{result['domain']} ({idna.encode(result['domain']).decode()})"
            except (idna.IDNAError, UnicodeEncodeError):
                decoded_domain = " (decoding error)"

        self.clear_last_status()

        print(f"{decoded_domain:<50} | {availability:<30} | {result['ip_address']:<15} | {result['geoip']:<30} | {result['punycode']:<8} | {result['whois_status']}")

    def print_progress(self, processed_count, total_count):
        status = f"Processed {processed_count}/{total_count} domains"
        print(status, end="\r")
        sys.stdout.flush()
        self.last_status_length = len(status)

    def clear_last_status(self):
        sys.stdout.write("\r" + " " * self.last_status_length + "\r")
