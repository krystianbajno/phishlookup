import logging
import whois
import time
logging.getLogger('whois').setLevel(logging.CRITICAL)

class WhoisLookup:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self, domain):
        self.domain = domain

    def lookup(self):
        for attempt in range(self.MAX_RETRIES):
            try:
                whois_data = whois.whois(self.domain)
                return {
                    'domain_name': self.safe_get_attr(whois_data, 'domain_name'),
                    'registrar': self.safe_get_attr(whois_data, 'registrar'),
                    'creation_date': self.safe_get_attr(whois_data, 'creation_date'),
                    'expiration_date': self.safe_get_attr(whois_data, 'expiration_date'),
                    'updated_date': self.safe_get_attr(whois_data, 'updated_date'),
                    'name_servers': self.safe_get_attr(whois_data, 'name_servers'),
                    'status': self.safe_get_attr(whois_data, 'status'),
                    'emails': self.safe_get_attr(whois_data, 'emails'),
                }
            except Exception as e:
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                else:
                    return {'error': 'WHOIS lookup failed', 'details': str(e)}
        return {'error': 'WHOIS lookup failed after retries'}

    @staticmethod
    def safe_get_attr(whois_data, attr):
        try:
            value = getattr(whois_data, attr, None)
            if isinstance(value, list) and len(value) == 1:
                return value[0]
            return value
        except Exception as e:
            return None
