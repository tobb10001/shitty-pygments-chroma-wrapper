import sys

from setuptools import setup

from shitty_pygments_chroma_wrapper import chroma

entry_points = list(
    {
        f"chroma-{l.name_ident()} = shitty_pygments_chroma_wrapper:{l.name_ident()}"
        for l in chroma.get_lexers()
    }
)

setup(
    entry_points={"pygments.lexers": entry_points},
)
