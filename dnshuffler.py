import argparse
import json
import csv
import sys
import idna

def generate_typos(domain, methods):
    keyboard_neighbors = {
        '1': '2q', '2': '1qw3', '3': '2we4', '4': '3er5', '5': '4rt6', '6': '5ty7', '7': '6yu8', '8': '7ui9', '9': '8io0', '0': '9op-',
        '-': '0p',
        'q': '12wa', 'w': 'q23esa', 'e': 'w34rsd', 'r': 'e45tdf', 't': 'r56yfg', 'y': 't67ugh', 'u': 'y78ihj', 'i': 'u89okj', 'o': 'i90plk',
        'p': 'o-l',
        'a': 'qwsz', 's': 'awedxz', 'd': 'serfcx', 'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'j': 'huikmn', 'k': 'jiolm', 'l': 'kop',
        'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
    }
    similar_chars = {
        'c': 'k', 'k': 'c', 's': 'z', 'z': 's',
        'o': '0', '0': 'o', '1': 'l', 'l': '1'
    }
    homoglyphs = {
        'a': ['а'],  # Cyrillic small letter A
        'c': ['с'],  # Cyrillic small letter ES
        'e': ['е'],  # Cyrillic small letter IE
        'i': ['і'],  # Cyrillic small letter BYELORUSSIAN-UKRAINIAN I
        'o': ['о'],  # Cyrillic small letter O
        'p': ['р'],  # Cyrillic small letter ER
        'x': ['х'],  # Cyrillic small letter HA
        'y': ['у'],  # Cyrillic small letter U
        'h': ['һ'],  # Cyrillic small letter SHHA
        'k': ['κ'],  # Greek small letter KAPPA
        'b': ['ь'],  # Cyrillic small letter SOFT SIGN
        'm': ['м'],  # Cyrillic small letter EM
    }
    typo_domains = set()

    for i, char in enumerate(domain):
        if 'neighbor' in methods and char in keyboard_neighbors:
            for neighbor in keyboard_neighbors[char]:
                typo_domains.add(domain[:i] + neighbor + domain[i+1:])
        
        if 'similar' in methods and char in similar_chars:
            typo_domains.add(domain[:i] + similar_chars[char] + domain[i+1:])

        if 'omit' in methods and len(domain) > 1:
            typo_domains.add(domain[:i] + domain[i+1:])

        if 'duplicate' in methods:
            typo_domains.add(domain[:i] + char + char + domain[i+1:])

        # Duplicate adjacent symbol
        if 'neighbor_duplicate' in methods and char in keyboard_neighbors:
            for neighbor in keyboard_neighbors[char]:
                typo_domains.add(domain[:i] + char + neighbor + domain[i+1:])

        # Replacement with homoglyphs
        if 'homoglyph' in methods and char in homoglyphs:
            for glyph in homoglyphs[char]:
                typo_domains.add(domain[:i] + glyph + domain[i+1:])

    # Adding a method to rearrange adjacent letters
    if 'swap' in methods:
        for i in range(len(domain) - 1):
            swapped = list(domain)
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            typo_domains.add(''.join(swapped))

    # Filter domains so that the hyphen is not at the beginning or end, the domain is not empty, there is no double hypens
    typo_domains = {typo for typo in typo_domains if len(typo) > 0 and not (typo.startswith('-') or typo.endswith('-')) and '--' not in typo}

    return typo_domains

def generate_all_typos(domains, methods):
    all_typos = {}
    for domain in domains:
        base_name, extension = domain.split('.')
        typos = generate_typos(base_name, methods)
        # Excluding the original domain
        typos.discard(base_name)
        all_typos[domain] = [idna.encode(typo + '.' + extension).decode('ascii') for typo in typos]
    return all_typos

def save_output(typos, output_file, output_format):
    if output_file:
        if output_format == 'json':
            with open(output_file, 'w') as f:
                json.dump(typos, f, indent=4)
        elif output_format == 'csv':
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                for domain, typo_list in typos.items():
                    for typo in typo_list:
                        writer.writerow([domain, typo])
        elif output_format == 'text':
            with open(output_file, 'w') as f:
                for domain, typo_list in typos.items():
                    #f.write("Typos for {}:\n".format(domain))
                    for typo in typo_list:
                        f.write("{}\n".format(typo))
                    #f.write("\n")
    else:
        if output_format == 'json':
            print(json.dumps(typos, indent=4))
        elif output_format == 'csv':
            for domain, typo_list in typos.items():
                for typo in typo_list:
                    print("{},{}".format(domain, typo))
        elif output_format == 'text':
            for domain, typo_list in typos.items():
                # print("Typos for {}:".format(domain))
                for typo in typo_list:
                    print(typo)
                #print()

def parse_args():
    parser = argparse.ArgumentParser(description='Generate typos for given domain names.')
    parser.add_argument('-d', '--domains', type=str, help='Comma-separated list of domains or a file containing domains. If not given, reads from stdin.')
    parser.add_argument('-m', '--methods', type=str, help='Methods to use for generating typos. Available methods: neighbor, similar, omit, duplicate, swap, neighbor_duplicate, homoglyph.')
    parser.add_argument('-o', '--output', type=str, help='Output file name. If not provided, output is printed to stdout.')
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'text'], default='text', help='Output file format.')
    return parser

def main():
    parser = parse_args()
    args = parser.parse_args()

    # Check for input from stdin
    if not args.domains and sys.stdin.isatty():
        print("No domains provided. Displaying help:")
        parser.print_help()
        sys.exit(1)

    methods = args.methods.split(',') if args.methods else ['neighbor', 'similar', 'omit', 'duplicate', 'swap', 'neighbor_duplicate']

    # Get domain list
    if args.domains:
        try:
            # Try to open file if argument presented
            with open(args.domains, 'r') as file:
                domains = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            # If no file then comma separated domain list
            domains = args.domains.split(',')
    else:
        # Read from stdin, if no input argument
        domains = [line.strip() for line in sys.stdin if line.strip()]

    typos = generate_all_typos(domains, methods)
    save_output(typos, args.output, args.format)

if __name__ == '__main__':
    main()
