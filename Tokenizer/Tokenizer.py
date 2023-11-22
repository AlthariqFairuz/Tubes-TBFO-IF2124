from TagChecker.TagChecker import tag_checker
import shlex


def tokenizer(html):
    # List of tokens
    # Token berisi tag-tag html atau SENTENCE diantara tag html
    # Untuk SENTENCE, disimpan dalam "SENTENCE"
    # Untuk tag html, disimpan dalam "<tag>" atau "</tag>"" atau "<tag />"
    list_of_tokens = list()
    current_token = ""
    is_tag = False

    # Loop through the html string
    for i in range(len(html)):
        char = html[i]

        if char == "<":
            # Jika current_token tidak kosong,
            # Ada SENTENCE sebelum <tag> atau </tag> misal: foo</p>
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
                # Jika is_tag == False, artinya sedang membaca SENTENCE
                # Detect character pertama dari SENTENCE (currentToken kosong)
                if (
                    current_token == ""
                    and char != " "
                    and char != "\n"
                    and char != "\t"
                    and char != "\r"
                ):
                    current_token += "SENTENCE"

        # i = len(html) - 1 dan current_token belum kosong
        # Artinya SENTENCE diakhir seperti </html>BACA_INI (INVALID, divalidasi di PDA.)
        if (i == len(html) - 1) and (current_token != ""):
            list_of_tokens.append("SENTENCE")

    # Filter the tokens to tags only
    list_of_tags = list(
        filter(lambda x: x.startswith("<") or x.endswith(">"), list_of_tokens)
    )

    # Check if the html tags are valid
    is_valid = True
    list_of_seperated_tokens = list()
    for token in list_of_tokens:
        if tag_checker(token) == False and token != "SENTENCE":
            is_valid = False
            print(token)
            # break
        elif token == "SENTENCE":
            list_of_seperated_tokens.append(token)
        else:
            token = token[1:-1]

            isClosing = False
            if token[-1] == "/":
                token = token[:-1]
                isClosing = True
            elif token[0] == "/":
                token = token[1:]
                isClosing = True

            separated = [elem.strip(" ") for elem in shlex.split(token)]
            tag = separated[0]

            for i in range(len(separated)):
                if "=" in separated[i]:
                    temp = separated[i].split("=")
                    attr = temp[0]
                    value = temp[1]
                    separated[i] = attr
                    if tag == "button":
                        if attr == "type":
                            if value in ["submit", "reset", "button"]:
                                separated.insert(i + 1, value)
                            else:
                                separated.insert(i + 1, "INVALID")
                            i += 1
                    elif tag == "form":
                        if attr == "method":
                            if value in ["GET", "POST"]:
                                separated.insert(i + 1, value)
                            else:
                                separated.insert(i + 1, "INVALID")
                            i += 1
                    elif tag == "input":
                        if attr == "type":
                            if value in [
                                "text",
                                "password",
                                "email",
                                "number",
                                "checkbox",
                            ]:
                                separated.insert(i + 1, value)
                            else:
                                separated.insert(i + 1, "INVALID")
                            i += 1

            if tag in ["link", "br", "hr", "img", "input"]:
                separated[0] = "<" + tag + ">"
                separated.append("</" + tag + ">")
            else:
                if isClosing:
                    separated[0] = "</" + tag + ">"
                else:
                    separated[0] = "<" + tag + ">"

            list_of_seperated_tokens.extend(separated)

    return list_of_seperated_tokens
    # if is_valid:
    #     # Return the list of tokens if valid
    #     # Next: validate structure using PDA.
    #     return list_of_tokens
    # else:
    #     # Invalid html tags
    #     print(
    #         """
    #     ░██████╗██╗░░░██╗███╗░░██╗████████╗░█████╗░██╗░░██╗  ███████╗██████╗░██████╗░░█████╗░██████╗░
    #     ██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔══██╗╚██╗██╔╝  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    #     ╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░███████║░╚███╔╝░  █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝
    #     ░╚═══██╗░░╚██╔╝░░██║╚████║░░░██║░░░██╔══██║░██╔██╗░  ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗
    #     ██████╔╝░░░██║░░░██║░╚███║░░░██║░░░██║░░██║██╔╝╚██╗  ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
    #     ╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝"""
    #     )
    #     print(f"Invalid Token: {token}")
    #     exit(1)
