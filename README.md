# Phishlookup
[![CodeFactor](https://www.codefactor.io/repository/github/krystianbajno/phishlookup/badge)](https://www.codefactor.io/repository/github/krystianbajno/phishlookup)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/398a05eb37fc4e79a560cab910208ad6)](https://app.codacy.com/gh/krystianbajno/phishlookup?utm_source=github.com&utm_medium=referral&utm_content=krystianbajno/phishlookup&utm_campaign=Badge_Grade)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup.svg?type=shield&issueType=security)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup?ref=badge_shield&issueType=security)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup?ref=badge_shield)

Phishlookup - Advanced phishing detection, domain name permutation and scanning tool.

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
phishlookup.py <domain> --lookup # lookup the single domain to determine if it was taken or is free to take
```

```
usage: phishlookup.py [-h] [-d DICTIONARY] [-td TLD_DICTIONARY] [-t THREADS] [-o OUTPUT] [--output-format {json,csv}] [--only-resolved] [--available] [--taken] [--lookup]
                      [-v]
                      domain

Phishlookup - Advanced phishing detection, domain name permutation, and scanning tool.

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
  --lookup              Show only taken domains
  -v, --verbose         Increase verbosity level
```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup?ref=badge_large)
