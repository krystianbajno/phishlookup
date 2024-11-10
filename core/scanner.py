import threading
from queue import Queue
import requests
from core.network import DNSResolver
from core.whois import WhoisLookup
from core.helpers import logger
import idna

class Scanner:
    def __init__(self, permutations, threads=10, output_file=None, output_format='text', available_only=False, not_available_only=False):
        self.permutations = permutations
        self.threads = threads
        self.queue = Queue()
        self.output_file = output_file
        self.output_format = output_format
        self.results = []
        self.available_only = available_only
        self.not_available_only = not_available_only

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
                if result:
                    # Apply filtering logic based on availability
                    if self.available_only and result['is_available'] != "IS AVAILABLE":
                        continue
                    if self.not_available_only and result['is_available'] != "NOT AVAILABLE":
                        continue
                    self.print_result(result)
                    self.results.append(result)
            finally:
                self.queue.task_done()

    def scan_domain(self, domain):
        logger.info(f"Scanning domain: {domain}")

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
            geoip_info = self.get_geoip_info(ip_address)

        try:
            encoded_domain = idna.encode(domain).decode('ascii')
            punycode_status = "Y" if encoded_domain != domain else "N"
        except (idna.IDNAError, UnicodeEncodeError):
            punycode_status = "N"

        result = {
            'domain': domain,
            'is_available': "NOT AVAILABLE" if ip_address else "IS AVAILABLE",
            'ip_address': ip_address or 'N/A',
            'geoip': geoip_info or 'N/A',
            'punycode': punycode_status,
            'whois_status': whois_status
        }
        return result

    def get_geoip_info(self, ip_address):
        try:
            response = requests.get(f'http://ip-api.com/json/{ip_address}')
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return f"{data.get('country', '')}, {data.get('city', '')}"
        except Exception as e:
            logger.error(f"Error during GeoIP lookup for {ip_address}: {e}")
        return 'N/A'

    def print_result(self, result):
        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'

        color = GREEN if result['is_available'] == "IS AVAILABLE" else RED
        availability = f"{color}{result['is_available']}{RESET}"

        if not hasattr(self, 'header_printed'):
            print(f"{'Domain':<25} | {'Is Available':<12} | {'IP Address':<15} | {'GeoLookup':<30} | {'Punycode':<8} | {'WHOIS Status'}")
            print("-" * 120)
            self.header_printed = True

        print(f"{result['domain']:<25} | {availability:<12} | {result['ip_address']:<15} | {result['geoip']:<30} | {result['punycode']:<8} | {result['whois_status']}")

    def save_results(self):
        try:
            with open(self.output_file, 'w') as f:
                if self.output_format == 'json':
                    import json
                    json.dump(self.results, f, indent=2)
                else:
                    for result in self.results:
                        f.write(
                            f"{result['domain']} | {result['is_available']} | {result['ip_address']} | "
                            f"{result['geoip']} | {result['punycode']} | {result['whois_status']}\n"
                        )
            logger.info(f"Results saved to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving results to {self.output_file}: {e}")
