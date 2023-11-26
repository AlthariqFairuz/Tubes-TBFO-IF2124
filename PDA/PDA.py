# Simpan kata yang akan di cek oleh PDA
start_input = ""

# Penannda apakah diterima PDA atau tidak
found = 0

# Simpan konfigurasi yang diterima
accepted_config = []

# Production rules ("read input", "pop stack", "push stack", "next state")
productions = {}

# Start state
start_symbol = ""

# Simbol awal pada stack
stack_start = ""

# array of acceptable states
acceptable_states = []

# E = empty stack, F = final state
accept_with = ""


def generate(state, input, stack, config):
    global productions
    global found

    total = 0

    # Jika found sudah bernilai 1 (input sudah diterima), fungsi generate akan segera berhenti dan mengembalikan 0 (tidak ada lagi gerakan yang perlu dihasilkan).
    if found:
        return 0

    if is_accepted(state, input, stack):
        # Tanda bahwa input sudah diterima oleh PDA jadinya tree node lainnya akan berhenti
        found = 1

        # Tambahkan konfigurasi yang diterima ke dalam array accepted_config
        accepted_config.extend(config)

        return 1

    # Jika tidak ditemukan, maka akan dilakukan generate gerakan yang mungkin dari state, input, dan stack yang diberikan
    moves = get_moves(state, input, stack)
    if len(moves) == 0:
        # Jika tidak ada gerakan yang mungkin untuk suatu state, maka akan mengembalikan 0
        return 0

    # Jika ada gerakan yang mungkin, maka akan dilakukan generate gerakan yang mungkin dari state, input, dan stack yang diberikan
    for i in moves:
        total = total + generate(i[0], i[1], i[2], config + [(i[0], i[1], i[2])])

    return total


# Fungsi untuk mendapatkan semua gerakan yang mungkin dari state, input, dan stack yang diberikan
def check(state, input, stack):
    global productions

    moves = []
    # print("INI PRODUCTIONS",productions)
    for i in productions:
        if i != state:
            continue

        for j in productions[i]:
            current = j
            new = []
            # print ("INI CURRENT",current)
            new.append(current[3])
            # Baca symbol input jika masih ada
            if len(current[0]) > 0:
                # print("INI INPUT",input)
                if len(input) > 0 and input[: len(current[0])] == current[0]:
                    new.append(input[len(current[0]) :])
                else:
                    continue
            else:
                new.append(input)

            # Baca stack symbol
            # print("INI STACK",stack)
            if len(current[1]) > 0:
                if len(stack) > 0 and stack[: len(current[1])] == current[1]:
                    new.append(current[2] + stack[len(current[1]) :])
                else:
                    continue
            else:
                new.append(current[2] + stack)

            moves.append(new)
    return moves


# Fungsi ini memeriksa apakah kata input diterima sesuai dengan kondisi penerimaan.
def is_accepted(state, input, stack):
    global accept_with
    global acceptable_states

    # Cek apakah semua symbol sudah dibaca
    if len(input) > 0:
        return 0

    # Cek apakah diterima dengan empty stack atau final state
    if accept_with == "E":
        if len(stack) < 1:
            return 1

        return 0

    else:
        for i in acceptable_states:
            if i == state:
                return 1

        return 0


# Fungsi ini membaca file dan mengurai PDA darinya.
def read_rules(filename):
    global productions
    global start_symbol
    global start_stack
    global acceptable_states
    global accept_with

    # Baca file
    try:
        lines = [line.rstrip() for line in open(filename)]

    # Jika error, return false
    except:
        return 0

    start_stack = lines[2]
    start_symbol = lines[3]
    
    start_stack = lines[4]

    acceptable_states.extend(lines[5].split())

    # E = empty stack, F = final state
    accept_with = lines[6]

    # Add rules
    for i in range(7, len(lines)):
        line = lines[i].strip()  # Abaikan Newline atau Whitespace
        if line:  # Line akan di split jika tidak ada newline
            production = line.split()
            configuration = [
                (production[1], production[2], production[4], production[3])
            ]
            if not production[0] in productions.keys():
                productions[production[0]] = []
            configuration = [
                tuple(s if s != "e" else "" for s in tup) for tup in configuration
            ]

            productions[production[0]].extend(configuration)

    print("Start state: ", start_symbol)
    print("Staert Stack: ", start_stack)
    print("Final states: ", acceptable_states)
    if accept_with == "E":
        print("Accept with empty stack")
    else:
        print("Accept with final state")
    print("List of production rules: ")
    for i in range(7, len(lines)):
        rules = lines[i].split()
        print(rules)
    print("\n")

    return 1


# # Ask the user for the name of the configuration file
# config_file = input("Masukkan nama file konfigurasi: ")

# # Parse the configuration file
# if not file_parser(config_file):
#     print("Gagal membaca file konfigurasi.")
#     exit(1)

# start_input = input("Masukkan kata yang akan dicek: ")
# def load_html (start_input):
#     with open(start_input, 'r') as file:
#         html = file.read()
#     return html

# start_input = load_html(start_input)
# print(start_input)

# # Generate the automaton with the given start symbol, input word, and start stack symbol
# result = generate(start_symbol, start_input, start_stack, [(start_symbol, start_input, start_stack)])
# if result :
#     print("""
#     ██╗░░░██╗░█████╗░██╗░░░░░██╗██████╗░  ██╗░░██╗████████╗███╗░░░███╗██╗░░░░░
#     ██║░░░██║██╔══██╗██║░░░░░██║██╔══██╗  ██║░░██║╚══██╔══╝████╗░████║██║░░░░░
#     ╚██╗░██╔╝███████║██║░░░░░██║██║░░██║  ███████║░░░██║░░░██╔████╔██║██║░░░░░
#     ░╚████╔╝░██╔══██║██║░░░░░██║██║░░██║  ██╔══██║░░░██║░░░██║╚██╔╝██║██║░░░░░
#     ░░╚██╔╝░░██║░░██║███████╗██║██████╔╝  ██║░░██║░░░██║░░░██║░╚═╝░██║███████╗
#     ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝╚═════╝░  ╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝╚══════╝""")
