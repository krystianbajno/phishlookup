import csv
import json

def save_results(output_file, results, output_format='csv'):
    try:
        with open(output_file, 'w', newline='') as f:
            if output_format == 'json':
                json.dump(results, f, indent=2)
            else:
                fieldnames = ['domain', 'is_available', 'ip_address', 'geoip', 'punycode', 'whois_status']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    writer.writerow(result)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results to {output_file}: {e}")
