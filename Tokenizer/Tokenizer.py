from TagChecker.TagChecker import tag_checker


def tokenizer(html):
    # List of tokens
    # Token berisi tag-tag html atau text diantara tag html
    # Untuk text, disimpan dalam "TEXT"
    # Untuk tag html, disimpan dalam "<tag>" atau "</tag>"" atau "<tag />"
    list_of_tokens = list()
    current_token = ""
    is_tag = False

    # Loop through the html string
    for i in range(len(html)):
        char = html[i]

        if char == "<":
            # Jika current_token tidak kosong,
            # Ada text sebelum <tag> atau </tag> misal: foo</p>
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
                # Jika is_tag == False, artinya sedang membaca text
                # Detect character pertama dari text (currentToken kosong)
                if (
                    current_token == ""
                    and char != " "
                    and char != "\n"
                    and char != "\t"
                    and char != "\r"
                ):
                    current_token += "TEXT"

        # i = len(html) - 1 dan current_token belum kosong
        # Artinya text diakhir seperti </html>BACA_INI (INVALID, divalidasi di PDA.)
        if (i == len(html) - 1) and (current_token != ""):
            list_of_tokens.append("TEXT")

    # Filter the tokens to tags only
    list_of_tags = list(
        filter(lambda x: x.startswith("<") or x.endswith(">"), list_of_tokens)
    )

    # Check if the html tags are valid
    is_valid = True
    for token in list_of_tags:
        if tag_checker(token) == False:
            is_valid = False
            break

    if is_valid:
        # Return the list of tokens if valid
        # Next: validate structure using PDA.
        return list_of_tokens
    else:
        # Invalid html tags
        print(
            """
        ░██████╗██╗░░░██╗███╗░░██╗████████╗░█████╗░██╗░░██╗  ███████╗██████╗░██████╗░░█████╗░██████╗░
        ██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔══██╗╚██╗██╔╝  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
        ╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░███████║░╚███╔╝░  █████╗░░██████╔╝██████╔╝██║░░██║██████╔╝
        ░╚═══██╗░░╚██╔╝░░██║╚████║░░░██║░░░██╔══██║░██╔██╗░  ██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗
        ██████╔╝░░░██║░░░██║░╚███║░░░██║░░░██║░░██║██╔╝╚██╗  ███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
        ╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝"""
        )
        print(f"Invalid Token: {token}")
        exit(1)
