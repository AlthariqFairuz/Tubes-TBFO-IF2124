import os

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

# E - accepted by empty stack or F - acceptable state (default is false)
accept_with = ""

def generate(state, input, stack, config):
    global productions
    global found

    total = 0

    # Jika found sudah bernilai 1 (input sudah diterima), fungsi generate akan segera berhenti dan mengembalikan 0 (tidak ada lagi gerakan yang perlu dihasilkan).
    if found:
        return 0

    if is_found(state, input, stack):
        # Tanda bahwa input sudah diterima oleh PDA jadinya tree node lainnya akan berhenti
        found = 1 
        
        # Tambahkan konfigurasi yang diterima ke dalam array accepted_config
        accepted_config.extend(config)

        return 1
    
	# Jika tidak ditemukan, maka akan dilakukan generate gerakan yang mungkin dari state, input, dan stack yang diberikan
    moves = get_moves(state, input, stack, config)
    if len(moves) == 0:
		# Jika tidak ada gerakan yang mungkin, maka akan mengembalikan 0
        return 0

	# Jika ada gerakan yang mungkin, maka akan dilakukan generate gerakan yang mungkin dari state, input, dan stack yang diberikan
    for i in moves:
        total = total + generate(i[0], i[1], i[2], config + [(i[0], i[1], i[2])])  

    return total

# Fungsi untuk mendapatkan semua gerakan yang mungkin dari state, input, dan stack yang diberikan
def get_moves(state, input, stack, config):
    global productions

    moves = []

    for i in productions:

        if i != state:
            continue

        for j in productions[i]:
            current = j
            new = []

            new.append(current[3])

            # Baca symbol input jika masih ada
            if len(current[0]) > 0:
                if len(input) > 0 and input[0] == current[0]:
                    new.append(input[1:])
                else:
                    continue
            else:            
                new.append(input)

            # Baca stack symbol
            if len(current[1]) > 0:
                if len(stack) > 0 and stack[0] == current[1]:
                    new.append(current[2] + stack[1:])
                else:
                    continue
            else:
                new.append(current[2] + stack)

            moves.append(new)

    return moves

# Fungsi ini memeriksa apakah kata input diterima sesuai dengan kondisi penerimaan.
def is_found(state, input, stack):
    global accept_with
    global acceptable_states

    # check if all symbols are read
    if len(input) > 0: 
        return 0

    # check if we accept with empty stack or end state
    if accept_with == "E":
        if len(stack) < 1:  # accept if stack is empty
            return 1

        return 0

    else:
        for i in acceptable_states:
            if i == state: # accept if we are in terminal state
                return 1

        return 0

# Buat mencetak semua konfigurasi yang diterima
def print_config(config):
    for i in config:
        print(i)

# Fungsi ini membaca file dan mengurai PDA darinya.
def parse_file(filename):
    global productions
    global start_symbol
    global start_stack
    global acceptable_states
    global accept_with

    try:
        lines = [line.rstrip() for line in open(filename)]

    except:
        return 0

    start_symbol = lines[3]

    start_stack = lines[4]

    acceptable_states.extend(lines[5].split())

    # E - accept on empty stack or F - acceptable state (default is false)
    accept_with = lines[6] 

    # add rules
    for i in range(7, len(lines)):
        production = lines[i].split()

        configuration = [(production[1], production[2], production[4], production[3])]

        if not production[0] in productions.keys(): 
            productions[production[0]] = []

        configuration = [tuple(s if s != "e" else "" for s in tup) for tup in configuration]

        productions[production[0]].extend(configuration)

    print(productions)
    print(start_symbol)
    print(start_stack)
    print(acceptable_states)
    print(accept_with)

    return 1

# # Ask the user for the name of the configuration file
# config_file = input("Masukkan nama file konfigurasi: ")

# # Parse the configuration file
# if not parse_file(config_file):
#     print("Gagal membaca file konfigurasi.")
#     exit(1)

# # Ask the user for the word to check
# start_input = input("Masukkan kata yang akan dicek: ")

# # Generate the automaton with the given start symbol, input word, and start stack symbol
# result = generate(start_symbol, start_input, start_stack, [(start_symbol, start_input, start_stack)])

# print(result)
