from PDA import PDA
from Tokenizer import Tokenizer as tokenize
from TagChecker import TagChecker as tagcheck

def valid ():
    print("""
    ██╗░░░██╗░█████╗░██╗░░░░░██╗██████╗░  ██╗░░██╗████████╗███╗░░░███╗██╗░░░░░
    ██║░░░██║██╔══██╗██║░░░░░██║██╔══██╗  ██║░░██║╚══██╔══╝████╗░████║██║░░░░░
    ╚██╗░██╔╝███████║██║░░░░░██║██║░░██║  ███████║░░░██║░░░██╔████╔██║██║░░░░░
    ░╚████╔╝░██╔══██║██║░░░░░██║██║░░██║  ██╔══██║░░░██║░░░██║╚██╔╝██║██║░░░░░
    ░░╚██╔╝░░██║░░██║███████╗██║██████╔╝  ██║░░██║░░░██║░░░██║░╚═╝░██║███████╗
    ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝╚═════╝░  ╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝╚══════╝""")

def invalid () :    
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

config_file = input("Masukkan nama file konfigurasi: ")

# Parse the configuration file
if not PDA.parse_file(config_file):
    print("Gagal membaca file konfigurasi.")
    exit(1)

# Ask the user for the word to check
html_file = input("Masukkan file html yang akan di cek: ")
html = load_html(html_file)
tokens = tokenize.tokenizer(html)
for token in tokens:
    if tagcheck.tag_checker(token) == False:
        invalid()
        print(f"Invalid Token: {token}")
        exit(1)

# Check if the first and last token is <html> and </html>
if tokens[0] != "<html>" or tokens[len(tokens)-1] != "</html>":
    invalid()
    exit(1)

# Generate the automaton with the given start symbol, input word, and start stack symbol
result = PDA.generate(PDA.start_symbol, tokens, PDA.start_stack, [(PDA.start_symbol, tokens, PDA.start_stack)])

if result == 1:
    valid()
else:
    invalid()

