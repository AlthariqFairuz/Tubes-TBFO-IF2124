from Tokenizer.Tokenizer import tokenizer


with open("./input/test.html", "r") as f:
    html = f.read()

print(tokenizer(html))
