import argparse

# Load arguments with argparse
parser = argparse.ArgumentParser()
parser.add_argument("pda_filename", help="PDA filename")
parser.add_argument("html_filename", help="HTML filename")
args = parser.parse_args()

# Get arguments
pda_filename = args.pda_filename
html_filename = args.html_filename

# Load PDA from file


# Load html from file


# Parse
isAccepted = True

# Print result
if isAccepted:
    print("Accepted")
else:
    print("Syntax Error")
