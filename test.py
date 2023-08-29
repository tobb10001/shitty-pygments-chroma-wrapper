import chroma

def test_ident_name():
    lexers = chroma.get_lexers()

    for l in lexers:
        assert l.name_ident().isidentifier(), f"{l.name_ident()} is not an identifier."
