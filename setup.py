from setuptools import setup

import chroma

entry_points = list(
    {f"chroma-{l.name_ident()} = lexers:{l.name_ident()}" for l in chroma.get_lexers()}
)

setup(
    entry_points={"pygments.lexers": entry_points},
)
