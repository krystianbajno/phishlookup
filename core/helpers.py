import re
import logging
import sys
import idna

def setup_logging(verbosity=0):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, verbosity)]
    logging.basicConfig(level=level, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')

def domain_tld(domain):
    domain = domain.lower()
    try:
        domain = idna.encode(domain).decode()
    except idna.IDNAError:
        pass
    parts = domain.split('.')
    if len(parts) >= 3:
        return parts[0], parts[1], '.'.join(parts[2:])
    elif len(parts) == 2:
        return '', parts[0], parts[1]
    else:
        return '', domain, ''

def is_valid_domain(domain):
    regex = r'^(?!\-)([A-Za-z0-9\-]{1,63}(?<!\-)\.)+[A-Za-z]{2,}$'
    if re.match(regex, domain):
        return True
    try:
        punycode = idna.encode(domain).decode('ascii')
        return re.match(regex, punycode) is not None
    except idna.IDNAError:
        return False
    
# logger = logging.getLogger(__name__)

import requests

def fetch_tlds():
    tld_url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    try:
        response = requests.get(tld_url)
        response.raise_for_status()
        tlds = response.text.splitlines()[1:]
        return [tld.lower() for tld in tlds]
    except requests.RequestException as e:
        print(f"Error fetching TLDs: {e}")
        return []
