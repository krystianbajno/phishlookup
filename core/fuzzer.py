import idna

from core.helpers import domain_tld, fetch_tlds, is_valid_domain

class Fuzzer:
    def __init__(self, domain, controller=None, dictionary_path=None, tld_dictionary=None):
        self.subdomain, self.domain, self.tld = domain_tld(domain)
        self.domain_ascii = idna.decode(self.domain)
        self.dictionary = self.load_dictionary(dictionary_path)
        self.tld_dictionary = self.load_tld_dictionary(tld_dictionary) if tld_dictionary else fetch_tlds()
        self.permutations = set()
        self.controller = controller  


    def load_dictionary(self, path):
        if not path:
            return []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return [line.strip().lower() for line in file if line.strip()]
        except Exception as e:
            self.controller.display_message(f"Error loading TLD dictionary file: {e}", color_pair=1)
            return []

    def load_tld_dictionary(self, path):
        if not path:
            return []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return [line.strip().lower() for line in file if line.strip()]
        except Exception as e:
            self.controller.display_message(f"Error loading TLD dictionary file: {e}", color_pair=1)
            return []

    def generate_permutations(self):
        if self.controller:
            self.controller.display_message("[*] Generating permutations...", color_pair=3)
        
        self.permutations = {self.full_domain()}

        base_domains = [self.full_domain()]
        for method in [
            self.addition, self.bitsquatting, self.homoglyphs, self.hyphenation, self.dotting,
            self.insertion, self.omission, self.pluralization, self.repetition,
            self.replacement, self.transposition, self.visually_similar_characters,
            self.vowel_swap, self.dictionary_words, self.double_insertion,
            self.keyboard_proximity, self.repeated_characters, self.all_possible_deletions
        ]:
            self.permutations.update(method(base_domains))

        self.permutations = [*{domain.lower() for domain in self.permutations if domain and is_valid_domain(domain)}]
        self.permutations.extend([domain.lower() for domain in self.generate_all_tld_permutations() if domain and is_valid_domain(domain)])
        
        if self.controller:
            self.controller.display_message(f"[+] Generated {len(self.permutations)} permutations.", color_pair=3)
        
        return self.permutations
        
    def generate_all_tld_permutations(self):
        if not self.tld_dictionary:
            print("No TLD dictionary loaded.")
            return set()
        
        permutations = set()
        for domain in self.permutations:
            domain_parts = domain.split('.')
            if len(domain_parts) > 1:
                base_domain = '.'.join(domain_parts[:-1])
                for tld in self.tld_dictionary:
                    if tld != self.tld:
                        permutations.add(f"{base_domain}.{tld}")
                        
        return permutations
    
    def generate_subdomain_permutations(self):
        decoys = ["www", "mail", "secure", "microsoft", "login", "mfa", "onmicrosoft", "auth", "register"]
        results = set()
        
        for domain in self.permutations:
            if not self.subdomain:
                results.update(f"{decoy}.{domain}" for decoy in decoys)
            else:
                results.add(domain)
        return results

    def full_domain(self, domain_part=None, tld_part=None):
        domain_part = domain_part if domain_part else self.domain
        tld_part = tld_part if tld_part else self.tld
        return f"{self.subdomain}.{domain_part}.{tld_part}" if self.subdomain else f"{domain_part}.{tld_part}"

    def addition(self, domains):
        return {domain + c for domain in domains for c in 'abcdefghijklmnopqrstuvwxyz'}

    def bitsquatting(self, domains):
        masks = [1 << i for i in range(8)]
        results = set()
        for domain in domains:
            for i in range(len(domain)):
                for mask in masks:
                    c = domain[i]
                    b = chr(ord(c) ^ mask)
                    if b.isalnum() or b == '-':
                        results.add(domain[:i] + b + domain[i+1:])
        return results
    
    def homoglyphs(self, domains):
        glyphs = {
            'A': ['Â', 'Ä', 'À', 'Á', 'Å'],
            'C': ['Ç'],
            'G': ['Ğ'],
            'I': ['İ', 'ı'],
            'O': ['Ö'],
            'S': ['Ş'],
            'U': ['Ü', 'Û'],
            'a': ['â', 'ä', 'à', 'á', 'å'],
            'c': ['ç'],
            'g': ['ğ'],
            'i': ['ı', 'ï', 'í', 'ì'],
            'o': ['ö'],
            's': ['ş'],
            'u': ['ü', 'û']
        }

        results = set()
        for domain in domains:
            for i in range(len(domain)):
                c = domain[i]
                if c in glyphs:
                    for g in glyphs[c]:
                        results.add(domain[:i] + g + domain[i+1:])
                    break
        return results    
    
    def dotting(self, domains):
        return {domain[:i] + '.' + domain[i:] for domain in domains for i in range(1, len(domain))}

    def hyphenation(self, domains):
        return {domain[:i] + '-' + domain[i:] for domain in domains for i in range(1, len(domain))}

    def insertion(self, domains):
        return {domain[:i] + c + domain[i:] for domain in domains for i in range(len(domain) + 1) for c in 'abcdefghijklmnopqrstuvwxyz0123456789'}
  
    def omission(self, domains):
        return {domain[:i] + domain[i+1:] for domain in domains for i in range(len(domain))}

    def pluralization(self, domains):
        results = set()
        for domain in domains:
            if not domain.endswith('s'):
                results.add(domain + 's')
            if not domain.endswith('es'):
                results.add(domain + 'es')
        return results

    def repetition(self, domains):
        return {domain[:i] + domain[i] + domain[i] + domain[i+1:] for domain in domains for i in range(len(domain))}

    def replacement(self, domains):
        keyboard_adjacent = {
            'a': ['q', 'w', 's', 'z'],
            'b': ['v', 'g', 'h', 'n'],
            'c': ['x', 'd', 'f', 'v'],
            'd': ['s', 'e', 'r', 'f', 'x', 'c'],
            'e': ['w', 's', 'd', 'r'],
            'f': ['d', 'r', 't', 'g', 'c', 'v'],
            'g': ['f', 't', 'y', 'h', 'v', 'b'],
            'h': ['g', 'y', 'u', 'j', 'b', 'n'],
            'i': ['u', 'j', 'k', 'o'],
            'j': ['h', 'u', 'i', 'k', 'n', 'm'],
            'k': ['j', 'i', 'o', 'l', 'm'],
            'l': ['k', 'o', 'p'],
            'm': ['n', 'j', 'k'],
            'n': ['b', 'h', 'j', 'm'],
            'o': ['i', 'k', 'l', 'p'],
            'p': ['o', 'l'],
            'q': ['w', 'a'],
            'r': ['e', 'd', 'f', 't'],
            's': ['a', 'w', 'e', 'd', 'z', 'x'],
            't': ['r', 'f', 'g', 'y'],
            'u': ['y', 'h', 'j', 'i'],
            'v': ['c', 'f', 'g', 'b'],
            'w': ['q', 'a', 's', 'e'],
            'x': ['z', 's', 'd', 'c'],
            'y': ['t', 'g', 'h', 'u'],
            'z': ['a', 's', 'x'],
            '1': ['2', 'q'],
            '2': ['1', '3', 'q', 'w'],
            '3': ['2', '4', 'w', 'e'],
            '4': ['3', '5', 'e', 'r'],
            '5': ['4', '6', 'r', 't'],
            '6': ['5', '7', 't', 'y'],
            '7': ['6', '8', 'y', 'u'],
            '8': ['7', '9', 'u', 'i'],
            '9': ['8', '0', 'i', 'o'],
            '0': ['9', 'o', 'p'],
        }
        results = set()
        for domain in domains:
            for i in range(len(domain)):
                c = domain[i]
                if c in keyboard_adjacent:
                    results.update(domain[:i] + adj + domain[i+1:] for adj in keyboard_adjacent[c])
        return results 

    def transposition(self, domains):
        return {domain[:i] + domain[i+1] + domain[i] + domain[i+2:] for domain in domains for i in range(len(domain) - 1)}

    def vowel_swap(self, domains, custom_vowels=None):
        vowels = custom_vowels if custom_vowels else 'aeiou'
        results = set()
        for domain in domains:
            for i in range(len(domain)):
                c = domain[i]
                if c in vowels:
                    results.update(domain[:i] + v + domain[i+1:] for v in vowels if v != c)
        return results

    def dictionary_words(self, domains):
        results = set()
        for domain in domains:
            results.update({domain + word, word + domain, domain + '-' + word, word + '-' + domain} for word in self.dictionary)
            results.update({domain + word, word + domain, domain + '.' + word, word + '.' + domain} for word in self.dictionary)
        return results
    
    def tld_swap(self, domains):
        return {f"{domain.split('.')[0]}.{tld}" for domain in domains for tld in self.tld_dictionary if tld != self.tld}

    def double_insertion(self, domains):
        return {domain[:i] + domain[i]*2 + domain[i+1:] for domain in domains for i in range(len(domain))}

    def keyboard_proximity(self, domains):
        keyboard = {
            'q': ['w', 'a'],
            'w': ['q', 'e', 's'],
            'e': ['w', 'r', 'd'],
            'r': ['e', 't', 'f'],
            't': ['r', 'y', 'g'],
            'y': ['t', 'u', 'h'],
            'u': ['y', 'i', 'j'],
            'i': ['u', 'o', 'k'],
            'o': ['i', 'p', 'l'],
            'p': ['o', 'l'],
            'a': ['q', 's', 'z'],
            's': ['a', 'd', 'w', 'z', 'x'],
            'd': ['s', 'f', 'e', 'x', 'c'],
            'f': ['d', 'g', 'r', 'c', 'v'],
            'g': ['f', 'h', 't', 'v', 'b'],
            'h': ['g', 'j', 'y', 'b', 'n'],
            'j': ['h', 'k', 'u', 'n', 'm'],
            'k': ['j', 'l', 'i', 'm'],
            'l': ['k', 'o'],
            'z': ['a', 's', 'x'],
            'x': ['z', 'd', 's', 'c'],
            'c': ['x', 'v', 'f', 'd'],
            'v': ['c', 'b', 'g', 'f'],
            'b': ['v', 'n', 'h', 'g'],
            'n': ['b', 'm', 'j', 'h'],
            'm': ['n', 'k', 'j'],
            '1': ['2', 'q'],
            '2': ['1', '3', 'q', 'w'],
            '3': ['2', '4', 'w', 'e'],
            '4': ['3', '5', 'e', 'r'],
            '5': ['4', '6', 'r', 't'],
            '6': ['5', '7', 't', 'y'],
            '7': ['6', '8', 'y', 'u'],
            '8': ['7', '9', 'u', 'i'],
            '9': ['8', '0', 'i', 'o'],
            '0': ['9', 'o', 'p'],
            '!': ['@', '1'],
            '@': ['!', '#', '2'],
            '#': ['@', '$', '3'],
            '$': ['#', '%', '4'],
            '%': ['$', '^', '5'],
            '^': ['%', '&', '6'],
            '&': ['^', '*', '7'],
            '*': ['&', '(', '8'],
            '(': ['*', ')', '9'],
            ')': ['(', '0'],
            '-': ['_', '='],
            '_': ['-', '+'],
            '+': ['_', '='],
            '=': ['-', '+']
        }

        results = set()
        for domain in domains:
            for i in range(len(domain)):
                c = domain[i]
                if c in keyboard:
                    results.update(domain[:i] + adj + domain[i+1:] for adj in keyboard[c])
        return results

    def repeated_characters(self, domains, min_repeats=2, max_repeats=5):
        results = set()
        for domain in domains:
            for i in range(len(domain)):
                for n in range(min_repeats, max_repeats + 1):
                    results.add(domain[:i] + domain[i] * n + domain[i+1:])
        return results
    
    def all_possible_deletions(self, domains):
        results = set()
        for domain in domains:
            if '.' in domain:
                parts = domain.rsplit('.', 1)
                domain_name, tld = parts[0], parts[1]

                for i in range(len(domain_name)):
                    mutated_domain = domain_name[:i] + domain_name[i + 1:]
                    results.add(f"{mutated_domain}.{tld}")
            else:
                for i in range(len(domain)):
                    mutated_domain = domain[:i] + domain[i + 1:]
                    results.add(mutated_domain)
        return results

    def visually_similar_characters(self, domain, custom_mappings=None):
        non_punycode_similar_chars = {
            'a': ['à', 'á', 'â', 'ã', 'ä', 'å'],
            'c': ['ç'],
            'e': ['é', 'è', 'ê', 'ë'],
            'i': ['í', 'ì', 'î', 'ï'],
            'n': ['ñ'],
            'o': ['ó', 'ò', 'ô', 'ö', 'õ'],
            'u': ['ú', 'ù', 'û', 'ü'],
            'y': ['ý', 'ÿ'],
            's': ['ş'],
            'g': ['ğ'],
            'l': ['1', 'I'],
            '1': ['l', 'I'],
            'I': ['l', '1'],
            'm': ['rn'],
            'f': ['t'],
            't': ['f'],
            'rn': ['m'],
            'o': ['0'],
            '0': ['o'],
            'u': ['v'],
            'v': ['u'],
            'p': ['b'],
            'b': ['p'],
            'd': ['cl'],
            'h': ['b'],
            's': ['5', 'z'],
            'z': ['s', '2']
        }

        punycode_similar_chars = {
            'a': ['а'],
            'b': ['в'],
            'c': ['с'],
            'e': ['е'],
            'h': ['һ', 'н'],
            'i': ['і'],
            'j': ['ј'],
            'k': ['к'],
            'm': ['м'],
            'n': ['п'],
            'o': ['о'],
            'p': ['р'],
            'r': ['г'],
            's': ['ѕ'],
            't': ['т'],
            'u': ['ц'],
            'x': ['х'],
            'y': ['у'],
            'z': ['з'],
            'g': ['Ԍ', 'ԍ'],
            'w': ['ѡ'],
            'o': ['ö'],
            'u': ['ü'],
            's': ['ş'],
            'ç': ['c'],
            'ğ': ['g'],
            'ı': ['i']
        }

        if custom_mappings:
            for key, values in custom_mappings.get('non_punycode', {}).items():
                if key in non_punycode_similar_chars:
                    non_punycode_similar_chars[key] = list(set(non_punycode_similar_chars[key] + values))
                else:
                    non_punycode_similar_chars[key] = values

            for key, values in custom_mappings.get('punycode', {}).items():
                if key in punycode_similar_chars:
                    punycode_similar_chars[key] = list(set(punycode_similar_chars[key] + values))
                else:
                    punycode_similar_chars[key] = values

        permutations = set()
        for i in range(len(domain)):
            for orig, swaps in non_punycode_similar_chars.items():
                if domain[i:i + len(orig)] == orig:
                    for swap in swaps:
                        mutated = domain[:i] + swap + domain[i + len(orig):]
                        permutations.add(mutated.lower())

            for orig, swaps in punycode_similar_chars.items():
                if domain[i:i + len(orig)] == orig:
                    for swap in swaps:
                        mutated = domain[:i] + swap + domain[i + len(orig):]
                        permutations.add(mutated.lower())

        return permutations