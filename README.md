# Phishlookup
Phishlookup - Advanced Phishing detection, Domain Name Permutation and Scanning Tool.

```
      /`·.¸
     /¸...¸`:·
 ¸.·´  ¸   `·.¸.·´)
: © ):´;      ¸  {
 `·.¸ `·  ¸.·´\`·¸)
     `\\´´\¸.·´
```

# Usage
```
phishlookup.py <domain> # show all
phishlookup.py <domain> --available # show only available
phishlookup.py <domain> --taken # show only taken
```

```
usage: phishlookup.py [-h] [-d DICTIONARY] [-td TLD_DICTIONARY] [-t THREADS] [-o OUTPUT] [--output-format {json,text}] [--only-resolved] [--available] [--taken] [-v]
                      domain

Phishlookup - Advanced phishing detection, domain name permutation and scanning tool.

positional arguments:
  domain                Domain name or URL to scan

options:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Path to dictionary file for additional permutations
  -td TLD_DICTIONARY, --tld-dictionary TLD_DICTIONARY
                        Path to TLD dictionary for TLD permutations
  -t THREADS, --threads THREADS
                        Number of threads to use
  -o OUTPUT, --output OUTPUT
                        Output file to save results
  --output-format {json,csv}
                        Output format for results (default: csv)
  --only-resolved       Show only domains that resolved to an IP
  --available           Show only available domains
  --taken               Show only taken domains
  -v, --verbose         Increase verbosity level
```