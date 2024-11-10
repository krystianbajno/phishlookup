import whois
import time
from core.helpers import logger

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
                    logger.warning(f"Error during WHOIS lookup for {self.domain} (attempt {attempt + 1}): {e}")
                    time.sleep(self.RETRY_DELAY)
                else:
                    logger.error(f"WHOIS lookup failed for {self.domain} after {self.MAX_RETRIES} attempts: {e}")
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
            logger.warning(f"Failed to retrieve attribute {attr} from WHOIS data: {e}")
            return None
