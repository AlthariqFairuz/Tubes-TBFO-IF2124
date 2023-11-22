from TagChecker.TagChecker import tag_checker
import shlex


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
    is_valid = True
    list_of_seperated_tokens = list()
    for token in list_of_tokens:
        if tag_checker(token) == False and token != "sentence":
            is_valid = False
            break
        elif token == "sentence":
            list_of_seperated_tokens.append(token)
        else:
            token = token[1:-1]

            isClosing = False
            if token[0] == "/":
                token = token[1:]
                isClosing = True

            separated = [elem.strip(" ") for elem in shlex.split(token)]
            separated_tag = list()
            tag = separated[0]
            separated_tag.append(tag)
            # print(separated)
            for i in range(len(separated)):
                if "=" in separated[i]:
                    temp = separated[i].split("=")
                    attr = temp[0]
                    value = temp[1]
                    separated_tag.append(attr)
                    if tag == "button":
                        if attr == "type":
                            if value in ["submit", "reset", "button"]:
                                separated_tag.append(value)
                            else:
                                separated_tag.append("invalid")
                    elif tag == "form":
                        if attr == "method":
                            if value in ["GET", "POST"]:
                                separated_tag.append(value.lower())
                            else:
                                separated_tag.append("invalid")
                    elif tag == "input":
                        if attr == "type":
                            if value in [
                                "text",
                                "password",
                                "email",
                                "number",
                                "checkbox",
                            ]:
                                separated_tag.append(value)
                            else:
                                separated_tag.append("invalid")

            if tag in ["link", "br", "hr", "img", "input"]:
                separated_tag[0] = "<" + tag + ">"
                separated_tag.append("</" + tag + ">")
            else:
                if isClosing:
                    separated_tag[0] = "</" + tag + ">"
                else:
                    separated_tag[0] = "<" + tag + ">"

            list_of_seperated_tokens.extend(separated_tag)

    if is_valid:
        return list_of_seperated_tokens
    else:
        invalid()
        print(f"Invalid Token: {token}")
        exit(1)
    # return list_of_seperated_tokens
    # if is_valid:
    #     # Return the list of tokens if valid
    #     # Next: validate structure using PDA.
    #     return list_of_tokens
    # else:
    #     # Invalid html tags
    # print(
    #     """
    # ░██████╗██╗░░░██╗███╗░░██╗████████╗░█████╗░██╗░░██╗  ███████╗██████╗░██████╗░░█████╗░██████╗░
    # ██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔══██╗╚██╗██╔╝  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    # ╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░███████║░╚███╔╝░  █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝
    # ░╚═══██╗░░╚██╔╝░░██║╚████║░░░██║░░░██╔══██║░██╔██╗░  ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗
    # ██████╔╝░░░██║░░░██║░╚███║░░░██║░░░██║░░██║██╔╝╚██╗  ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
    # ╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝"""
    # )
    # print(f"Invalid Token: {token}")
    # exit(1)
