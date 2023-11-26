import re


def invalid():
    print(
        """
    ░██████╗██╗░░░██╗███╗░░██╗████████╗░█████╗░██╗░░██╗  ███████╗██████╗░██████╗░░█████╗░██████╗░
    ██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔══██╗╚██╗██╔╝  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    ╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░███████║░╚███╔╝░  █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝
    ░╚═══██╗░░╚██╔╝░░██║╚████║░░░██║░░░██╔══██║░██╔██╗░  ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗
    ██████╔╝░░░██║░░░██║░╚███║░░░██║░░░██║░░██║██╔╝╚██╗  ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
    ╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝"""
    )


def tokenizer(html):
    # List of tokens
    # Token berisi tag-tag html atau sentence diantara tag html
    # Untuk sentence, disimpan dalam "sentence"
    # Untuk tag html, disimpan dalam "<tag>" atau "</tag>"" atau "<tag />"
    list_of_tokens = list()
    current_token = ""
    is_tag = False

    # Loop through the html string
    for i in range(len(html)):
        char = html[i]

        if char == "<":
            # Jika current_token tidak kosong,
            # Ada sentence sebelum <tag> atau </tag> misal: foo</p>
            # Atau tag < yang berlebihan, misal: <<p>
            if current_token != "":
                # Close tag
                list_of_tokens.append(current_token)
                current_token = ""

            # Start tag
            current_token += char
            is_tag = True
        elif char == ">":
            # Close tag
            current_token += char

            # Tambahkan ke list_of_tokens, lalu reset current_token
            list_of_tokens.append(current_token)
            current_token = ""
            is_tag = False
        else:
            # Jika is_tag == True, artinya sedang membaca tag html
            # Contoh: <BACA_TAG_INI> atau </BACA_TAG_INI>
            if is_tag:
                current_token += char
            else:
                # Jika is_tag == False, artinya sedang membaca sentence
                # Detect character pertama dari sentence (currentToken kosong)
                if (
                    current_token == ""
                    and char != " "
                    and char != "\n"
                    and char != "\t"
                    and char != "\r"
                ):
                    current_token += "sentence"

        # i = len(html) - 1 dan current_token belum kosong
        # Artinya sentence diakhir seperti </html>BACA_INI (invalid, divalidasi di PDA.)
        if (i == len(html) - 1) and (current_token != ""):
            list_of_tokens.append("sentence")

    # Check if the html tags are valid
    list_of_seperated_tokens = list()
    for token in list_of_tokens:
        if token == "sentence":
            list_of_seperated_tokens.append(token)
        elif token.startswith("<!--") and token.endswith("-->"):
            if len(token) >= 7:
                list_of_seperated_tokens.extend(["startcomment", "endcomment"])
            else:
                list_of_seperated_tokens.append(token)
        else:
            token = token[1:-1]
            isClosing = False
            if token[0] == "/":
                token = token[1:]
                isClosing = True

            separated = list()
            j = 0
            isQuoted = False
            if len(token.split()) > 1:
                for i in range(len(token)):
                    if token[i] == '"' and isQuoted == False:
                        isQuoted = True
                    elif token[i] == '"' and isQuoted == True:
                        isQuoted = False
                    elif token[i] == " " and isQuoted == False:
                        separated.append(token[j:i])
                        j = i + 1
                separated.append(token[j:])
            else:
                separated.append(token)

            separated_tag = list()
            tag = separated[0]
            separated_tag.append(tag)
            pattern = re.compile(r'^[^=]*="[^"]*"$')
            for i in range(1, len(separated)):
                match = pattern.match(separated[i])
                if match:
                    attr, value = separated[i].split("=")
                    separated_tag.append(attr)
                    if tag == "form":
                        if attr == "method":
                            separated_tag.append(value.strip('"').lower())
                    elif tag == "input":
                        if attr == "type":
                            separated_tag.append(value.strip('"'))
                    elif tag == "button":
                        if attr == "type":
                            separated_tag.append(value.strip('"'))
                else:
                    separated_tag.append(separated[i])

            if tag in ["link", "br", "hr", "img", "input"]:
                separated_tag[0] = "<" + tag + ">"
                separated_tag.append("</" + tag + ">")
            else:
                if isClosing:
                    separated_tag[0] = "</" + tag + ">"
                else:
                    separated_tag[0] = "<" + tag + ">"

            list_of_seperated_tokens.extend(separated_tag)

    return list_of_seperated_tokens
