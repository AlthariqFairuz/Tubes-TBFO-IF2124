import os
import argparse
from PDA import PDA
from Tokenizer import Tokenizer as tokenize

def valid():
    print("""
    ██╗░░░██╗░█████╗░██╗░░░░░██╗██████╗░  ██╗░░██╗████████╗███╗░░░███╗██╗░░░░░
    ██║░░░██║██╔══██╗██║░░░░░██║██╔══██╗  ██║░░██║╚══██╔══╝████╗░████║██║░░░░░
    ╚██╗░██╔╝███████║██║░░░░░██║██║░░██║  ███████║░░░██║░░░██╔████╔██║██║░░░░░
    ░╚████╔╝░██╔══██║██║░░░░░██║██║░░██║  ██╔══██║░░░██║░░░██║╚██╔╝██║██║░░░░░
    ░░╚██╔╝░░██║░░██║███████╗██║██████╔╝  ██║░░██║░░░██║░░░██║░╚═╝░██║███████╗
    ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝╚═════╝░  ╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝╚══════╝""")

def invalid():
    print("""
    ░██████╗██╗░░░██╗███╗░░██╗████████╗░█████╗░██╗░░██╗  ███████╗██████╗░██████╗░░█████╗░██████╗░
    ██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔══██╗╚██╗██╔╝  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    ╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░███████║░╚███╔╝░  █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝
    ░╚═══██╗░░╚██╔╝░░██║╚████║░░░██║░░░██╔══██║░██╔██╗░  ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗
    ██████╔╝░░░██║░░░██║░╚███║░░░██║░░░██║░░██║██╔╝╚██╗  ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
    ╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝""")

# Fungsi untuk membaca file HTML
def load_html(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html = file.read()
    return html


# Bikin parser
parser = argparse.ArgumentParser()

parser.add_argument("ConfigFile", metavar="config", type=str, help="File Rules PDA")
parser.add_argument("HtmlFile", metavar="html", type=str, help="HTML yang akan dicek")

args = parser.parse_args()

# Directory testcase dan pda di file input
input_dir = 'input'

# Parse rules PDA
if not PDA.read_rules(os.path.join(input_dir, args.ConfigFile)):
    print("Gagal membaca file konfigurasi.")
    exit(1)

# Load the HTML file
html = load_html(os.path.join(input_dir, args.HtmlFile))
tokens = tokenize.tokenizer(html)

# Generate the automaton with the given start symbol, input word, and start stack symbol
result = PDA.generate(PDA.start_symbol, "".join(tokens), PDA.start_stack, [(PDA.start_symbol, "".join(tokens), PDA.start_stack)])

if result == 1:
    valid()
else:
    invalid()