from TagChecker import tag_checker
import time

start = time.time()

nama_file = "index.html"

with open(nama_file, "r") as f:
    html = f.read()

list_of_tokens = list()
start_symbol = "<"
end_symbol = ">"
token = ""
is_token = False

for char in html:
    if char == start_symbol:
        is_token = True
    elif char == end_symbol:
        token += char
        is_token = False
        list_of_tokens.append(token)
        token = ""
    if is_token:
        token += char

isValid = True
for token in list_of_tokens:
    if tag_checker(token) == False:
        isValid = False
        break

if isValid:
    print("Valid HTML")
else:
    print("Invalid HTML")

end = time.time()
print(f"Time Taken: {end - start} seconds")
