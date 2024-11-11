import threading
from queue import Queue
from core.geoip import get_geoip_info
from core.network import DNSResolver
from core.whois import WhoisLookup
import csv

from core.cli_printer import ConsolePrinter

class Scanner:
    def __init__(self, permutations, threads=1000, output_file=None, output_format='csv', available_only=False, not_available_only=False):
        self.permutations = permutations
        self.threads = threads
        self.queue = Queue()
        self.output_file = output_file
        self.output_format = output_format
        self.results = []
        self.available_only = available_only
        self.not_available_only = not_available_only
        self.processed_count = 0
        self.lock = threading.Lock()
        self.printer = ConsolePrinter()

    def run_scans(self):
        for domain in self.permutations:
            self.queue.put(domain)

        thread_list = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.worker)
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()

        if self.output_file:
            self.save_results()

    def worker(self):
        while not self.queue.empty():
            domain = self.queue.get()
            try:
                result = self.scan_domain(domain)

                with self.lock:
                    self.processed_count += 1
                    self.printer.print_progress(self.processed_count, len(self.permutations))

                if result:
                    if self.available_only and result['is_available'] != "AVAILABLE":
                        continue
                    if self.not_available_only and result['is_available'] != "NOT AVAILABLE":
                        continue
                    with self.lock:
                        self.printer.print_header()
                        self.printer.print_result(result)
            finally:
                self.queue.task_done()


    def scan_domain(self, domain):
        dns_resolver = DNSResolver(domain)
        dns_info = dns_resolver.resolve()
        ip_address = dns_info['A'][0] if dns_info.get('A') else None

        if ip_address:
            whois_lookup = WhoisLookup(domain)
            whois_info = whois_lookup.lookup()
            available = not whois_info or whois_info.get('error') or not whois_info.get('domain_name')
            whois_status = "Registered" if not available else "Not Registered"
        else:
            whois_info = {'status': 'Domain not registered (no DNS resolution)'}
            whois_status = "Not Registered"

        geoip_info = None
        if ip_address:
            geoip_info = get_geoip_info(ip_address)

        try:
            import idna
            encoded_domain = idna.encode(domain).decode('ascii')
            punycode_status = "Y" if encoded_domain != domain else "N"
        except (idna.IDNAError, UnicodeEncodeError):
            punycode_status = "N"

        result = {
            'domain': domain,
            'is_available': "NOT AVAILABLE" if ip_address else "AVAILABLE",
            'ip_address': ip_address or 'N/A',
            'geoip': geoip_info or 'N/A',
            'punycode': punycode_status,
            'whois_status': whois_status
        }
        return result

    def save_results(self):
        try:
            with open(self.output_file, 'w', newline='') as f:
                if self.output_format == 'json':
                    import json
                    json.dump(self.results, f, indent=2)
                else:
                    fieldnames = ['domain', 'is_available', 'ip_address', 'geoip', 'punycode', 'whois_status']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in self.results:
                        writer.writerow(result)
            print(f"Results saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving results to {self.output_file}: {e}")
