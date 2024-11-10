import dns.resolver
from core.helpers import logger

class DNSResolver:
    def __init__(self, domain):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

    def resolve(self):
        records = {}
        try:
            a_records = self.resolver.resolve(self.domain, 'A')
            records['A'] = [r.to_text() for r in a_records]
        except dns.resolver.NoAnswer:
            records['A'] = []
        except dns.resolver.NXDOMAIN:
            records['A'] = []
        except Exception as e:
            logger.error(f"Error resolving A record for {self.domain}: {e}")
            records['A'] = []

        try:
            mx_records = self.resolver.resolve(self.domain, 'MX')
            records['MX'] = [r.to_text() for r in mx_records]
        except dns.resolver.NoAnswer:
            records['MX'] = []
        except dns.resolver.NXDOMAIN:
            records['MX'] = []
        except Exception as e:
            logger.error(f"Error resolving MX record for {self.domain}: {e}")
            records['MX'] = []

        return records
