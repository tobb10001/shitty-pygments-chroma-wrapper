import subprocess
from typing import List, Sequence

from .models import ChromaLexer

def _removeprefix(s: str, prefix: str) -> str:
    # backport to be compatible with python 3.8
    if not s.startswith(prefix):
        return s
    return s[len(prefix):]

def get_lexers() -> Sequence[ChromaLexer]:
    chroma_list = subprocess.run(["chroma", "--list"], capture_output=True)

    raw = chroma_list.stdout.decode().split("\n")

    # looks like this:
    # lexers:
    #  L1
    #    aliases: a1, a2
    #    filenames: *.a1, *.a2
    #    mimetypes: mime/type
    #  L2
    #    ...
    #
    # styles: ...

    # remove styles and newline above it
    # remove the very first line as well
    i = 0
    while not raw[i].startswith("style"):
        i += 1
    raw = raw[1 : i - 1]

    # long lines have a break
    unbroken: List[str] = []
    for i in range(len(raw) - 1):
        if not raw[i+1].startswith(" "):
            unbroken[i] += " " + raw[i+1]
        else:
            unbroken.append(raw[i])

    lexers: List[ChromaLexer] = []
    for line in unbroken:
        if not line.startswith("   "):
            lexers.append(ChromaLexer(line.strip()))
            continue
        elif line.startswith("    aliases: "):
            lexers[-1].aliases = _removeprefix(line, "    aliases: ").split()
        elif line.startswith("    filenames: "):
            lexers[-1].filenames = _removeprefix(line, "    filenames: ").split()
        elif line.startswith("    mimetypes: "):
            lexers[-1].mimetypes = _removeprefix(line, "    mimetypes: ").split()
        else:
            raise Exception("Can't read this line: " + line)

    return lexers
