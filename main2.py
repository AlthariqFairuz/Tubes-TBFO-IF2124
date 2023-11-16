from PDA import PDA

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

# Generate the automaton with the given start symbol, input word, and start stack symbol
result = PDA.generate(PDA.start_symbol, html, PDA.start_stack, [(PDA.start_symbol, html, PDA.start_stack)])

if result == 1:
    print("Accepted")

else:
    print("Syntax Error")
