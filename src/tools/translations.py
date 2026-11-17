"""Arabic translations without GNU gettext installed.

    python tools/translations.py extract    collect every marked text into locale/ar/LC_MESSAGES/django.po,
                                            keeping the translations already written
    python tools/translations.py compile    check the translations and write django.mo, which Django reads
    python tools/translations.py missing    list the texts that have no Arabic yet

Texts are found in the templates ({% translate %}, {% blocktranslate %}) with Django's own template
reader, and in the Python code (gettext, gettext_lazy, ngettext, pgettext and their short names).
A translation whose placeholders, such as %(code)s, differ from the English is refused, because the
page would fail when it is shown.
"""
import ast
import re
import struct
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
PO = SRC / "locale" / "ar" / "LC_MESSAGES" / "django.po"
MO = PO.with_suffix(".mo")
SKIP_DIRS = {"migrations", "tests", "tools", ".venv", "staticfiles", "__pycache__", "locale"}
FUNCS = {"_", "_lazy", "gettext", "gettext_lazy", "gettext_noop", "ngettext", "ngettext_lazy", "pgettext",
         "pgettext_lazy", "npgettext", "npgettext_lazy"}
PLURAL_FORMS = ("nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : "
                "n%100>=11 && n%100<=99 ? 4 : 5;")
PLACEHOLDER = re.compile(r"%\((\w+)\)[sd]|%[sd]")


class Entry:
    def __init__(self, msgid, plural=None, context=None):
        self.msgid, self.plural, self.context = msgid, plural, context
        self.msgstr = [""] * (6 if plural else 1)
        self.places = []

    @property
    def key(self):
        return (self.context, self.msgid)


# ---------- finding the texts ----------

def call_args(text, start):
    """Return the argument text of a call that starts at text[start] == '('."""
    depth, quote, i = 0, None, start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
        i += 1
    return ""


def from_templates(found):
    import django
    from django.conf import settings
    if not settings.configured:
        settings.configure()
        django.setup()
    from django.utils.translation.template import templatize

    for path in sorted((SRC / "templates").rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        code = templatize(source)
        place = str(path.relative_to(SRC))
        # _("...") used as a tag argument ({% include ... with label=_("Custodian") %}) is translated when the
        # page is shown, but Django's template reader does not report it, so find it here.
        for match in re.finditer(r"""\b_\(("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\)""", source):
            add(found, Entry(ast.literal_eval(match.group(1))), place)
        for match in re.finditer(r"\b(n?p?gettext)\(", code):
            args = call_args(code, match.end() - 1)
            call = ast.parse(f"f({args})", mode="eval").body
            strings = [a.value for a in call.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            name = match.group(1)
            if name == "gettext":
                add(found, Entry(strings[0]), place)
            elif name == "ngettext":
                add(found, Entry(strings[0], strings[1]), place)
            elif name == "pgettext":
                add(found, Entry(strings[1], context=strings[0]), place)
            elif name == "npgettext":
                add(found, Entry(strings[1], strings[2], strings[0]), place)


def from_python(found, problems):
    for path in sorted(SRC.rglob("*.py")):
        if SKIP_DIRS & set(path.relative_to(SRC).parts):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        place = str(path.relative_to(SRC))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func.id if isinstance(node.func, ast.Name) else (
                node.func.attr if isinstance(node.func, ast.Attribute) else None)
            if func in ("record", "change_state"):  # history actions, shown translated by audit_ui.action_text
                position = 1 if func == "record" else 3
                action = node.args[position] if len(node.args) > position else next(
                    (k.value for k in node.keywords if k.arg == "action"), None)
                if isinstance(action, ast.Constant) and isinstance(action.value, str) and action.value:
                    add(found, Entry(action.value, context="history"), f"{place}:{node.lineno}")
                continue
            if func not in FUNCS or not node.args:
                continue
            args = node.args
            if any(isinstance(a, ast.JoinedStr) for a in args):
                problems.append(f"{place}:{node.lineno} f-string inside {func}()")
                continue
            consts = [a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else None for a in args]
            if func.startswith("np"):
                if None in consts[:3]:
                    continue
                add(found, Entry(consts[1], consts[2], consts[0]), f"{place}:{node.lineno}")
            elif func.startswith("n"):
                if None in consts[:2]:
                    continue
                add(found, Entry(consts[0], consts[1]), f"{place}:{node.lineno}")
            elif func.startswith("p"):
                if None in consts[:2]:
                    continue
                add(found, Entry(consts[1], context=consts[0]), f"{place}:{node.lineno}")
            elif consts[0] is not None:
                add(found, Entry(consts[0]), f"{place}:{node.lineno}")


def add(found, entry, place):
    if not entry.msgid:
        return
    existing = found.setdefault(entry.key, entry)
    if entry.plural and not existing.plural:
        existing.plural, existing.msgstr = entry.plural, [""] * 6
    existing.places.append(place)


# ---------- reading and writing the .po file ----------

def quote(text):
    text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
    return f'"{text}"'


def unquote(text):
    return ast.literal_eval(text)


def read_po():
    entries, current, field = {}, None, None
    if not PO.exists():
        return entries
    for line in PO.read_text(encoding="utf-8").splitlines() + [""]:
        line = line.strip()
        if not line or line.startswith("#"):
            if current is not None and current.msgid:
                entries[current.key] = current
            current, field = None, None
            continue
        if current is None:
            current = Entry("")
            current.context = None
        if line.startswith("msgctxt "):
            current.context, field = unquote(line[8:]), "ctx"
        elif line.startswith("msgid_plural "):
            current.plural, field = unquote(line[13:]), "plural"
            current.msgstr = [""] * 6
        elif line.startswith("msgid "):
            current.msgid, field = unquote(line[6:]), "id"
        elif line.startswith("msgstr["):
            index = int(line[7:line.index("]")])
            current.msgstr[index] = unquote(line[line.index("]") + 2:])
            field = ("str", index)
        elif line.startswith("msgstr "):
            current.msgstr = [unquote(line[7:])]
            field = ("str", 0)
        elif line.startswith('"'):
            piece = unquote(line)
            if field == "ctx":
                current.context += piece
            elif field == "id":
                current.msgid += piece
            elif field == "plural":
                current.plural += piece
            elif isinstance(field, tuple):
                current.msgstr[field[1]] += piece
    return entries


def write_po(entries):
    PO.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Arabic translation of Dawra Campus.", 'msgid ""', 'msgstr ""',
             '"Content-Type: text/plain; charset=UTF-8\\n"', '"Language: ar\\n"',
             f'"Plural-Forms: {PLURAL_FORMS}\\n"', ""]
    for entry in sorted(entries.values(), key=lambda e: (e.places[0] if e.places else "~", e.msgid)):
        for place in sorted(set(entry.places))[:3]:
            lines.append(f"#: {place}")
        if entry.context:
            lines.append(f"msgctxt {quote(entry.context)}")
        lines.append(f"msgid {quote(entry.msgid)}")
        if entry.plural:
            lines.append(f"msgid_plural {quote(entry.plural)}")
            for i, text in enumerate(entry.msgstr):
                lines.append(f"msgstr[{i}] {quote(text)}")
        else:
            lines.append(f"msgstr {quote(entry.msgstr[0])}")
        lines.append("")
    PO.write_text("\n".join(lines), encoding="utf-8")


# ---------- commands ----------

def extract():
    found, problems = {}, []
    from_templates(found)
    from_python(found, problems)
    old = read_po()
    for key, entry in found.items():
        if key in old and (bool(old[key].plural) == bool(entry.plural)):
            entry.msgstr = old[key].msgstr
    write_po(found)
    done = sum(1 for e in found.values() if all(e.msgstr))
    print(f"{len(found)} texts ({done} translated) written to {PO.relative_to(SRC)}")
    for problem in problems:
        print("  cannot translate:", problem)


def placeholders(text):
    return sorted(PLACEHOLDER.findall(text))


def compile_mo():
    entries = read_po()
    good, bad = [], []
    for entry in entries.values():
        if not all(entry.msgstr):
            continue
        sources = [entry.msgid] + ([entry.plural] if entry.plural else [])
        expected = set(n for s in sources for n in placeholders(s))
        if any(set(placeholders(t)) - expected or (not entry.plural and set(placeholders(t)) != expected)
               for t in entry.msgstr):
            bad.append(entry)
            continue
        good.append(entry)
    header = (f"Content-Type: text/plain; charset=UTF-8\nLanguage: ar\nPlural-Forms: {PLURAL_FORMS}\n")
    pairs = [("", header)]
    for entry in good:
        key = (entry.context + "\x04" if entry.context else "") + entry.msgid
        if entry.plural:
            key += "\x00" + entry.plural
        pairs.append((key, "\x00".join(entry.msgstr)))
    pairs.sort()
    ids = [k.encode("utf-8") for k, _ in pairs]
    strs = [v.encode("utf-8") for _, v in pairs]
    n = len(pairs)
    key_start = 7 * 4 + 16 * n
    offsets, ids_blob, strs_blob = [], b"", b""
    for i_text, s_text in zip(ids, strs):
        offsets.append((len(i_text), len(ids_blob), len(s_text), len(strs_blob)))
        ids_blob += i_text + b"\x00"
        strs_blob += s_text + b"\x00"
    value_start = key_start + len(ids_blob)
    key_table = b"".join(struct.pack("<2I", length, key_start + off) for length, off, _, _ in offsets)
    value_table = b"".join(struct.pack("<2I", length, value_start + off) for _, _, length, off in offsets)
    data = struct.pack("<7I", 0x950412DE, 0, n, 7 * 4, 7 * 4 + 8 * n, 0, 0) + key_table + value_table + ids_blob + strs_blob
    MO.write_bytes(data)
    print(f"{len(good)} translations compiled to {MO.relative_to(SRC)}")
    for entry in bad:
        print("  refused (placeholders differ):", entry.msgid[:70])
    return not bad


def missing():
    entries = read_po()
    todo = [e for e in entries.values() if not all(e.msgstr)]
    for entry in todo:
        print(entry.msgid[:100])
    print(f"{len(todo)} of {len(entries)} texts have no Arabic yet")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "extract":
        extract()
    elif command == "compile":
        sys.exit(0 if compile_mo() else 1)
    elif command == "missing":
        missing()
    else:
        print(__doc__)
