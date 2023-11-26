import argparse
from PDA import PDA
from Tokenizer import Tokenizer as tokenize
import argparse

# Load arguments with argparse
parser = argparse.ArgumentParser()
parser.add_argument("pda_filename", help="PDA filename")
parser.add_argument("html_filename", help="HTML filename")
args = parser.parse_args()

# Get arguments
pda_filename = args.pda_filename
html_filename = args.html_filename

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
    with open(filename, 'r') as file:
        html = file.read()
    return html

# Parse the configuration file
if not PDA.file_parser(pda_filename):
    print("Gagal membaca file konfigurasi.")
    exit(1)

# Tokenize html file
html = load_html(html_filename)
tokens = tokenize.tokenizer(html)

# Generate automata dengan start symbol, input word, dan start stack symbol yang ada.
result = PDA.generate(PDA.start_symbol, "".join(tokens), PDA.start_stack, [(PDA.start_symbol, "".join(tokens), PDA.start_stack)])

if result == 1:
    valid()
else:
    invalid()
