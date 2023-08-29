import json
import subprocess
import tempfile

from pygments import token as t
from pygments.lexer import Lexer

import chroma


class ChromaLexer(Lexer):
    lexer_name = "UNKNOWN"

    def get_tokens_unprocessed(self, text: str):
        with tempfile.NamedTemporaryFile("w") as f:
            f.write(text)
            f.flush()
            chroma_process = subprocess.run(
                ["chroma", "-l", self.lexer_name, "--json", f.name], capture_output=True
            )

        tokens = json.loads(chroma_process.stdout)

        index = 0
        for token in tokens:
            if token["type"] in aliases:
                token["type"] = aliases[token["type"]]
            pyg_token = lookup[token["type"]]
            if pyg_token is None:
                print("Unknown token:", token["type"])
            yield (index, pyg_token, token["value"])
            index += len(token["value"])


for lexer in chroma.get_lexers():
    clazz = type(
        lexer.name_ident(),
        (ChromaLexer,),
        {
            "lexer_name": lexer.name,
            "name": "chroma-" + lexer.name_ident(),
            "aliases": lexer.aliases,
            "filenames": lexer.filenames,
        },
    )
    locals()[lexer.name_ident()] = clazz

lookup = {
    "Background": None,
    "PreWrapper": None,
    "Line": None,
    "LineNumbers": None,
    "LineNumbersTable": None,
    "LineHighlight": None,
    "LineTable": None,
    "LineTableTD": None,
    "LineLink": None,
    "CodeLine": None,
    "Error": t.Error,
    "Other": t.Other,
    "None": None,
    "EOFType": None,
    "Keyword": t.Keyword,
    "KeywordConstant": t.Keyword.Constant,
    "KeywordDeclaration": t.Keyword.Declaration,
    "KeywordNamespace": t.Keyword.Namespace,
    "KeywordPseudo": t.Keyword.Pseudo,
    "KeywordReserved": t.Keyword.Reserved,
    "KeywordType": t.Keyword.Type,
    "Name": t.Name,
    "NameAttribute": t.Name.Attribute,
    "NameBuiltin": t.Name.Builtin,
    "NameBuiltinPseudo": t.Name.Builtin.Pseudo,
    "NameClass": t.Name.Class,
    "NameConstant": t.Name.Constant,
    "NameDecorator": t.Name.Decorator,
    "NameEntity": t.Name.Entity,
    "NameException": t.Name.Exception,
    "NameFunction": t.Name.Function,
    "NameFunctionMagic": t.Name.Function.Magic,
    "NameKeyword": t.Name.Keyword,
    "NameLabel": t.Name.Label,
    "NameNamespace": t.Name.Namespace,
    "NameOperator": t.Name.Operator,
    "NameOther": t.Name.Other,
    "NamePseudo": t.Name.Pseudo,
    "NameProperty": t.Name.Property,
    "NameTag": t.Name.Tag,
    "NameVariable": t.Name.Variable,
    "NameVariableAnonymous": t.Name.Variable.Anonymous,
    "NameVariableClass": t.Name.Variable.Class,
    "NameVariableGlobal": t.Name.Variable.Global,
    "NameVariableInstance": t.Name.Variable.Instance,
    "NameVariableMagic": t.Name.Variable.Magic,
    "Literal": t.Literal,
    "LiteralDate": t.Literal.Date,
    "LiteralOther": t.Literal.Other,
    "LiteralString": t.Literal.String,
    "LiteralStringAffix": t.Literal.String.Affix,
    "LiteralStringAtom": t.Literal.String.Atom,
    "LiteralStringBacktick": t.Literal.String.Backtick,
    "LiteralStringBoolean": t.Literal.String.Boolean,
    "LiteralStringChar": t.Literal.String.Char,
    "LiteralStringDelimiter": t.Literal.String.Delimiter,
    "LiteralStringDoc": t.Literal.String.Doc,
    "LiteralStringDouble": t.Literal.String.Double,
    "LiteralStringEscape": t.Literal.Escape,
    "LiteralStringHeredoc": t.Literal.Heredoc,
    "LiteralStringInterpol": t.Literal.Interpol,
    "LiteralStringName": t.Literal.Name,
    "LiteralStringOther": t.Literal.Otherj,
    "LiteralStringRegex": t.Literal.Regex,
    "LiteralStringSingle": t.Literal.Single,
    "LiteralStringSymbol": t.Literal.Symbol,
    "LiteralNumber": t.Literal.Number,
    "LiteralNumberBin": t.Literal.Number.Bin,
    "LiteralNumberFloat": t.Literal.Number.Float,
    "LiteralNumberHex": t.Literal.Number.Hex,
    "LiteralNumberInteger": t.Literal.Number.Integer,
    "LiteralNumberIntegerLong": t.Literal.Number.Long,
    "LiteralNumberOct": t.Literal.Number.Oct,
    "Operator": t.Operator,
    "OperatorWord": t.Operator.Word,
    "Punctuation": t.Punctuation,
    "Comment": t.Comment,
    "CommentHashbang": t.Comment.Hashbang,
    "CommentMultiline": t.Comment.Multiline,
    "CommentSingle": t.Comment.Single,
    "CommentSpecial": t.Comment.Special,
    "CommentPreproc": t.Comment.Preproc,
    "CommentPreprocFile": t.Comment.Preproc.File,
    "Generic": t.Generic,
    "GenericDeleted": t.Generic.Deleted,
    "GenericEmph": t.Generic.Emph,
    "GenericError": t.Generic.Error,
    "GenericHeading": t.Generic.Heading,
    "GenericInserted": t.Generic.Inserted,
    "GenericOutput": t.Generic.Output,
    "GenericPrompt": t.Generic.Prompt,
    "GenericStrong": t.Generic.Strong,
    "GenericSubheading": t.Generic.Subheading,
    "GenericTraceback": t.Generic.Traceback,
    "GenericUnderline": t.Generic.Unerline,
    "Text": t.Text,
    "TextWhitespace": t.Text.Whitespace,
    "TextSymbol": t.Text.Symbol,
    "TextPunctuation": t.Text.Punctuation,
}

aliases = {
    "Whitespace": "TextWhitespace",
    "Date": "LiteralDate",
    "String": "LiteralString",
    "StringAffix": "LiteralStringAffix",
    "StringBacktick": "LiteralStringBacktick",
    "StringChar": "LiteralStringChar",
    "StringDelimiter": "LiteralStringDelimiter",
    "StringDoc": "LiteralStringDoc",
    "StringDouble": "LiteralStringDouble",
    "StringEscape": "LiteralStringEscape",
    "StringHeredoc": "LiteralStringHeredoc",
    "StringInterpol": "LiteralStringInterpol",
    "StringOther": "LiteralStringOther",
    "StringRegex": "LiteralStringRegex",
    "StringSingle": "LiteralStringSingle",
    "StringSymbol": "LiteralStringSymbol",
    "Number": "LiteralNumber",
    "NumberBin": "LiteralNumberBin",
    "NumberFloat": "LiteralNumberFloat",
    "NumberHex": "LiteralNumberHex",
    "NumberInteger": "LiteralNumberInteger",
    "NumberIntegerLong": "LiteralNumberIntegerLong",
    "NumberOct": "LiteralNumberOct",
}
