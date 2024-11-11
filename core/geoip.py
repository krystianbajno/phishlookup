import requests

def ip_api_handler(data):
    if data.get('status') == 'success':
        country = data.get('country', '')
        city = data.get('city', '')
        return f"{country}, {city}"
    return None

def ipwhois_handler(data):
    if data.get('success') is True:
        country = data.get('country', '')
        city = data.get('city', '')
        return f"{country}, {city}"
    return None

def ipinfo_handler(data):
    country = data.get('country', '')
    city = data.get('city', '')
    if country or city:
        return f"{country}, {city}"
    return None

def freegeoip_handler(data):
    country = data.get('country_name', '')
    city = data.get('city', '')
    if country or city:
        return f"{country}, {city}"
    return None

def get_geoip_info(ip_address):
    providers = [
        {
            'url': f'http://ip-api.com/json/{ip_address}',
            'response_handler': ip_api_handler
        },
        {
            'url': f'https://ipwho.is/{ip_address}',
            'response_handler': ipwhois_handler
        },
        {
            'url': f'https://ipinfo.io/{ip_address}/json',
            'response_handler': ipinfo_handler
        },
        {
            'url': f'https://freegeoip.app/json/{ip_address}',
            'response_handler': freegeoip_handler
        }
    ]
    
    for provider in providers:
        try:
            url = provider['url']
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result = provider['response_handler'](data)
                if result:
                    return result
        except requests.RequestException:
            continue
    return 'N/A'