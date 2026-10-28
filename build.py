"""Build docs/ (the published site) from src/index.src.html.

Puts the Loop logo in as an inline SVG symbol (NetFree blocks logo image files),
fills in the contact form address from form-endpoint.txt, and writes the favicon.
Run: python build.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "brand", "edition-02", "design-system", "assets", "Logos")
SRC = os.path.join(HERE, "src", "index.src.html")
OUT = os.path.join(HERE, "docs")


def logo_parts(name, grad_id):
    s = open(os.path.join(KIT, name), encoding="utf-8").read()
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    m = re.match(r"<svg\b[^>]*>", s)
    body = s[m.end(): s.rindex("</svg>")]
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    defs = re.search(r"<defs>(.*?)</defs>", body, flags=re.S).group(1)
    shape = re.sub(r"<defs>.*?</defs>", "", body, flags=re.S)
    old = re.search(r'id="([^"]+)"', defs).group(1)
    defs = defs.replace('id="%s"' % old, 'id="%s"' % grad_id)
    shape = shape.replace("url(#%s)" % old, "url(#%s)" % grad_id)
    assert "url(#%s)" % grad_id in shape
    return defs, shape


def main():
    html = open(SRC, encoding="utf-8").read()

    defs, shape = logo_parts("loop-reference-primary.svg", "loop-logo-grad")
    sprite = (
        '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
        "<defs>%s<symbol id=\"loop-logo\" viewBox=\"0 0 944 543\">%s</symbol></defs></svg>" % (defs, shape)
    )
    assert html.count("<!--LOGO-SPRITE-->") == 1
    html = html.replace("<!--LOGO-SPRITE-->", sprite)

    ep_file = os.path.join(HERE, "form-endpoint.txt")
    endpoint = open(ep_file, encoding="utf-8").read().strip() if os.path.exists(ep_file) else ""
    assert html.count("__FORM_ENDPOINT__") == 1
    html = html.replace("__FORM_ENDPOINT__", endpoint)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    # Favicon: the full primary logo on a navy square.
    favicon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 944 944">'
        '<defs>%s</defs><rect width="944" height="944" rx="180" fill="#0D033B"/>'
        '<g transform="translate(0 200)">%s</g></svg>' % (defs, shape)
    )
    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(favicon)

    with open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8", newline="\n") as f:
        f.write("www.loopny.net\n")

    print("built docs/index.html", len(html), "chars; form endpoint:", endpoint or "(not set)")


if __name__ == "__main__":
    main()
