import re
from dataclasses import dataclass, field
from typing import List

REG = re.compile(r'\W|^(?=\d)')

@dataclass
class ChromaLexer:
    name: str
    aliases: List[str] = field(default_factory=list)
    filenames: List[str] = field(default_factory=list)
    mimetypes: List[str] = field(default_factory=list)

    def name_ident(self):
        return REG.sub("_", self.name)
