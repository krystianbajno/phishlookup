# Phishlookup
[![CodeFactor](https://www.codefactor.io/repository/github/krystianbajno/phishlookup/badge)](https://www.codefactor.io/repository/github/krystianbajno/phishlookup)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/398a05eb37fc4e79a560cab910208ad6)](https://app.codacy.com/gh/krystianbajno/phishlookup?utm_source=github.com&utm_medium=referral&utm_content=krystianbajno/phishlookup&utm_campaign=Badge_Grade)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup.svg?type=shield&issueType=security)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup?ref=badge_shield&issueType=security)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup?ref=badge_shield)

Phishlookup is an advanced phishing detection, domain name permutation, and scanning tool designed to enhance your cybersecurity toolkit. This tool enables you to uncover potential phishing domains by analyzing and generating permutations based on the input domain name.

```
      /`·.¸
     /¸...¸`:·
 ¸.·´  ¸   `·.¸.·´)
: © ):´;      ¸  {
 `·.¸ `·  ¸.·´\`·¸)
     `\\´´\¸.·´
```

<img src="https://raw.githubusercontent.com/krystianbajno/krystianbajno/main/img/phishlookup.png"/>

# Features

- **Comprehensive Permutations**: Supports a wide range of mutation methods to simulate potential phishing domains.
- **TLD Variations**: Tests domains across different top-level domains (TLDs).
- **Phishing Detection**: Identify domains that could be used for typosquatting or impersonation.
- **Fast & Extensible**: Uses multi-threading for quick scans and allows for easy integration of custom dictionaries and TLDs.

# Installation
```
git clone https://github.com/krystianbajno/phishlookup.git
cd phishlookup
pip install -r requirements.txt
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

# Methods
Phishlookup uses the following mutation techniques to generate domain permutations:

- Addition
- Bitsquatting
- Homoglyphs
- Hyphenation
- Dotting
- Insertion
- Omission
- Pluralization
- Repetition
- Replacement
- Transposition
- Visually Similar Characters
- Vowel Swap
- Dictionary Words
- Double Insertion
- Keyboard Proximity
- Repeated Characters
- All Possible Deletions

Supports Custom TLDs and Dictionary Integration!

# FAQ

Q: Does this tool detect domains with special characters like Turkish letters or punycode?

A: Yes, Phishlookup is fully equipped to handle punycode domains and special characters.

Q: Can it identify typosquatting domains?

A: Absolutely. The tool is designed to generate and detect common typosquatting variations.

Q: What inspired the creation of this tool?

A: This tool was inspired by [dnstwist](https://github.com/elceef/dnstwist) by [@elceef](https://github.com/elceef). Kudos to @elceef for their outstanding work! While dnstwist is excellent, Phishlookup aims to be more extensible and incorporate additional methods for domain permutations.

# Contributing
Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the tool.

# License
Phishlookup is licensed under the MIT License.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fkrystianbajno%2Fphishlookup?ref=badge_large)
