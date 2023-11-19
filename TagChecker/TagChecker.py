import re
from itertools import permutations, combinations


def attr_brute(tag: str, req_attr: list[str], opt_attr: list[str] = []) -> list[str]:
    """Brute force all possible attribute combinations for a given tag.

    Args:
        tag (str): Tag to brute force.
        req_attr (list[str]): Required attributes.
        opt_attr (list[str], optional): Optional attributes. Defaults to [].

    Returns:
        list[str]: List of all possible attribute combinations.
    """

    if tag not in ["link", "br", "hr", "img", "input"]:
        if len(req_attr) == 0:
            attr_rules = [re.compile(r"<" + tag + r"\s*>")]
        else:
            attr_rules = []

        # req_attr must exist in every combination
        for i in range(0, len(opt_attr) + 1):
            for kemungkinan in combinations(opt_attr, i):
                attr_rule = req_attr + list(kemungkinan)
                for rule in permutations(attr_rule):
                    attr_rules.append(
                        re.compile(r"<" + tag + r"\s+" + r"\s+".join(rule) + r"\s*>")
                    )

        # append closing tag
        attr_rules.append(re.compile(r"</" + tag + r"\s*>"))
    else:
        if len(req_attr) == 0:
            attr_rules = attr_rules = [re.compile(r"<" + tag + r"/>")]
        else:
            attr_rules = []

        for i in range(0, len(opt_attr) + 1):
            for kemungkinan in combinations(opt_attr, i):
                attr_rule = req_attr + list(kemungkinan)
                for rule in permutations(attr_rule):
                    attr_rules.append(
                        re.compile(r"<" + tag + r"\s+" + r"\s+".join(rule) + r"\s*/>")
                    )

    return attr_rules


def tag_checker(tag: str) -> bool:
    """Check if a tag is valid."""

    if (tag.startswith("<html") and tag.endswith(">")) or (
        tag.startswith("</html") and tag.endswith(">")
    ):
        html = attr_brute("html", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in html:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<head") and tag.endswith(">")) or (
        tag.startswith("</head") and tag.endswith(">")
    ):
        head = attr_brute("head", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in head:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<body") and tag.endswith(">")) or (
        tag.startswith("</body") and tag.endswith(">")
    ):
        body = attr_brute("body", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in body:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<title") and tag.endswith(">")) or (
        tag.startswith("</title") and tag.endswith(">")
    ):
        title = attr_brute("title", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in title:
            if re.match(rule, tag):
                return True
    elif tag.startswith("<link") and tag.endswith("/>"):
        link = attr_brute(
            "link",
            [r'rel=".*"'],
            [r'class=".*"', r'id=".*"', r'style=".*"', r'href=".*"'],
        )
        for rule in link:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<script") and tag.endswith(">")) or (
        tag.startswith("</script") and tag.endswith(">")
    ):
        script = attr_brute(
            "script", [], [r'class=".*"', r'id=".*"', r'style=".*"', r'src=".*"']
        )
        for rule in script:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<h1") and tag.endswith(">")) or (
        tag.startswith("</h1") and tag.endswith(">")
    ):
        h1 = attr_brute("h1", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in h1:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<h2") and tag.endswith(">")) or (
        tag.startswith("</h2") and tag.endswith(">")
    ):
        h2 = attr_brute("h2", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in h2:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<h3") and tag.endswith(">")) or (
        tag.startswith("</h3") and tag.endswith(">")
    ):
        h3 = attr_brute("h3", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in h3:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<h4") and tag.endswith(">")) or (
        tag.startswith("</h4") and tag.endswith(">")
    ):
        h4 = attr_brute("h4", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in h4:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<h5") and tag.endswith(">")) or (
        tag.startswith("</h5") and tag.endswith(">")
    ):
        h5 = attr_brute("h5", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in h5:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<h6") and tag.endswith(">")) or (
        tag.startswith("</h6") and tag.endswith(">")
    ):
        h6 = attr_brute("h6", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in h6:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<p") and tag.endswith(">")) or (
        tag.startswith("</p") and tag.endswith(">")
    ):
        p = attr_brute("p", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in p:
            if re.match(rule, tag):
                return True
    elif tag.startswith("<br") and tag.endswith("/>"):
        br = attr_brute("br", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in br:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<em") and tag.endswith(">")) or (
        tag.startswith("</em") and tag.endswith(">")
    ):
        em = attr_brute("em", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in em:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<b") and tag.endswith(">")) or (
        tag.startswith("</b") and tag.endswith(">")
    ):
        b = attr_brute("b", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in b:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<abbr") and tag.endswith(">")) or (
        tag.startswith("</abbr") and tag.endswith(">")
    ):
        abbr = attr_brute("abbr", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in abbr:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<strong") and tag.endswith(">")) or (
        tag.startswith("</strong") and tag.endswith(">")
    ):
        strong = attr_brute("strong", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in strong:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<small") and tag.endswith(">")) or (
        tag.startswith("</small") and tag.endswith(">")
    ):
        small = attr_brute("small", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in small:
            if re.match(rule, tag):
                return True
    elif tag.startswith("<hr") and tag.endswith("/>"):
        hr = attr_brute("hr", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in hr:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<div") and tag.endswith(">")) or (
        tag.startswith("</div") and tag.endswith(">")
    ):
        div = attr_brute("div", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in div:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<a") and tag.endswith(">")) or (
        tag.startswith("</a") and tag.endswith(">")
    ):
        a = attr_brute(
            "a", [], [r'class=".*"', r'id=".*"', r'style=".*"', r'href=".*"']
        )
        for rule in a:
            if re.match(rule, tag):
                return True
    elif tag.startswith("<img") and tag.endswith("/>"):
        img = attr_brute(
            "img",
            [r'src=".*"'],
            [r'class=".*"', r'id=".*"', r'style=".*"', r'alt=".*"'],
        )
        for rule in img:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<button") and tag.endswith(">")) or (
        tag.startswith("</button") and tag.endswith(">")
    ):
        button = attr_brute(
            "button",
            [],
            [r'class=".*"', r'id=".*"', r'style=".*"', r'type="submit|button|reset"'],
        )
        for rule in button:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<form") and tag.endswith(">")) or (
        tag.startswith("</form") and tag.endswith(">")
    ):
        form = attr_brute(
            "form",
            [],
            [
                r'class=".*"',
                r'id=".*"',
                r'style=".*"',
                r'action=".*"',
                r'method="GET|POST"',
            ],
        )
        for rule in form:
            if re.match(rule, tag):
                return True
    elif tag.startswith("<input") and tag.endswith("/>"):
        input_tag = attr_brute(
            "input",
            [r'type=".*"'],
            [
                r'class=".*"',
                r'id=".*"',
                r'style=".*"',
                r'type="text|password|email|number|checkbox"',
            ],
        )
        for rule in input_tag:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<table") and tag.endswith(">")) or (
        tag.startswith("</table") and tag.endswith(">")
    ):
        table = attr_brute("table", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in table:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<tr") and tag.endswith(">")) or (
        tag.startswith("</tr") and tag.endswith(">")
    ):
        tr = attr_brute("tr", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in tr:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<td") and tag.endswith(">")) or (
        tag.startswith("</td") and tag.endswith(">")
    ):
        td = attr_brute("td", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in td:
            if re.match(rule, tag):
                return True
    elif (tag.startswith("<th") and tag.endswith(">")) or (
        tag.startswith("</th") and tag.endswith(">")
    ):
        th = attr_brute("th", [], [r'class=".*"', r'id=".*"', r'style=".*"'])
        for rule in th:
            if re.match(rule, tag):
                return True
    elif tag.startswith("<!--") and tag.endswith("-->"):
        return True

    return False