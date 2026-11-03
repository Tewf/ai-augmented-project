"""A reference solution of the llms.txt task, used only to check that the judge's tests accept a correct answer."""
import re

_LINK = re.compile(r"^- \[([^\]]*)\]\(([^)]*)\)(.*)$")


def llms_links(text):
    out = []
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = _LINK.match(line)
        if m:
            rest = m.group(3)
            out.append((m.group(1), m.group(2), rest[1:].strip() if rest.startswith(":") else ""))
    return out
