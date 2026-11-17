"""Build the right-to-left copies of the Dawra style files, used when the app is shown in Arabic.

Each copy is the same stylesheet with left and right swapped: margin, padding, border and position
sides, text alignment, floats, corner radii, horizontal movement and shadows, and gradient directions.
Run it after changing a style file:  python tools/build_rtl_css.py   (from the src folder)
"""
import re
from pathlib import Path

STATIC = Path(__file__).resolve().parent.parent / "static" / "dawra"
FILES = ["styles.css", "app.css", "motion.css", "ui.css", "dark.css", "effects.css"]

# Rules that must not be mirrored: the logo image is a fixed picture cropped by its left offset.
NO_FLIP = (".logo img",)

FOUR_SIDES = {"margin", "padding", "inset", "border-width", "border-style", "border-color", "scroll-padding",
              "scroll-margin"}


def swap_words(text):
    """left <-> right inside names and keywords."""
    return re.sub(r"\b(left|right)\b", lambda m: "right" if m.group(1) == "left" else "left", text)


def split_top(text, sep):
    """Split on sep where it is not inside brackets or quotes."""
    parts, depth, quote, buf = [], 0, None, ""
    for ch in text:
        if quote:
            buf += ch
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    return parts


def negate(length):
    length = length.strip()
    if length in ("0", "0px") or length.startswith("var(") or length.startswith("calc("):
        return length if not length.startswith("calc(") else f"calc(-1 * {length[5:-1]})"
    return length[1:] if length.startswith("-") else "-" + length


def flip_transform(value):
    value = re.sub(r"translateX\(([^)]*)\)", lambda m: f"translateX({negate(m.group(1))})", value)

    def translate(m):
        args = split_top(m.group(1), ",")
        args[0] = negate(args[0])
        return "translate(" + ",".join(a.strip() for a in args) + ")"

    return re.sub(r"translate\(([^()]*(?:\([^()]*\)[^()]*)*)\)", translate, value)


def flip_shadow(value):
    shadows = []
    for shadow in split_top(value, ","):
        tokens = shadow.split()
        lengths = [i for i, t in enumerate(tokens) if re.match(r"^-?[\d.]+(px|rem|em)?$", t)]
        if lengths and tokens[0] != "inset" or (len(lengths) >= 1 and tokens[0] == "inset"):
            i = lengths[0]
            tokens[i] = negate(tokens[i])
        shadows.append(" ".join(tokens))
    return ",".join(shadows)


def flip_gradient(value):
    value = re.sub(r"linear-gradient\(\s*(-?[\d.]+)deg", lambda m: f"linear-gradient({(360 - float(m.group(1))) % 360:g}deg", value)
    return re.sub(r"\bto (left|right)\b", lambda m: "to " + ("right" if m.group(1) == "left" else "left"), value)


def flip_declaration(prop, value):
    p = prop.strip()
    v = value.strip()
    low = p.lower()
    if low.startswith("--"):
        return p, v
    new_prop = swap_words(p)
    if low in ("text-align", "float", "clear", "transform-origin", "background-position", "caption-side"):
        v = swap_words(v)
    if low in FOUR_SIDES:
        parts = v.split()
        if len(parts) == 4 and "!important" not in v:
            parts[1], parts[3] = parts[3], parts[1]
            v = " ".join(parts)
    if low == "border-radius" and "/" not in v:
        parts = v.replace("!important", "").split()
        important = " !important" if "!important" in v else ""
        if len(parts) == 4:
            v = f"{parts[1]} {parts[0]} {parts[3]} {parts[2]}{important}"
        elif len(parts) == 3:
            v = f"{parts[1]} {parts[0]} {parts[1]} {parts[2]}{important}"
        elif len(parts) == 2:
            v = f"{parts[1]} {parts[0]}{important}"
    if low == "transform" or low == "translate":
        v = flip_transform(v)
    if low == "box-shadow":
        v = flip_shadow(v)
    if "linear-gradient" in v:
        v = flip_gradient(v)
    v = re.sub(r"url\((['\"]?)(?!data:|https?:|/|\.\./)", r"url(\1../", v)
    return new_prop, v


def flip_block(css):
    """Flip a stylesheet or the inside of an @media block."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j == -1:
            out.append(css[i:])
            break
        prelude = css[i:j]
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        body = css[j + 1:k - 1]
        head = prelude.strip()
        if head.startswith(("@media", "@supports", "@keyframes", "@layer", "@container")):
            out.append(prelude + "{" + flip_block(body) + "}")
        elif any(part.strip().startswith(NO_FLIP) for part in head.split(",")):
            out.append(prelude + "{" + body + "}")
        else:
            decls = []
            for decl in split_top(body, ";"):
                if ":" in decl and decl.strip():
                    prop, value = decl.split(":", 1)
                    new_prop, new_value = flip_declaration(prop, value)
                    decls.append(f"{new_prop}:{new_value}")
                elif decl.strip():
                    decls.append(decl.strip())
            out.append(prelude + "{" + ";".join(decls) + "}")
        i = k
    return "".join(out)


def main():
    target = STATIC / "rtl"
    target.mkdir(exist_ok=True)
    for name in FILES:
        source = (STATIC / name).read_text(encoding="utf-8")
        source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
        header = f"/* Right-to-left copy of {name}, made by tools/build_rtl_css.py. Do not edit by hand. */\n"
        (target / name).write_text(header + flip_block(source).strip() + "\n", encoding="utf-8")
        print("wrote", target / name)


if __name__ == "__main__":
    main()
