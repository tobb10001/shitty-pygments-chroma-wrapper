# shitty-pygments-chroma-wrapper

[Pygments](https://github.com/pygments/pygments) wrapper for
[Chroma](https://github.com/alecthomas/chroma): Use chroma lexers in Pygments, when
Chroma is not an option.

## How to use

1. Have Chroma installed: `chroma` must be available in your `PATH`, before installing
   this plugin.
2. Install this plugin via `pip`:
    ```sh
    $ pip install git+https://github.com/tobb10001/shitty-pygments-chroma-wrapper
    ```
3. Check your installation with `pygments -L`. All Chroma lexers should be displayed.
4. Profit.

## How it works

`shitty-pygments-chroma-wrapper` is a Pygments plugin. During installation, it calls
`chroma --list` and parses its output in order to generate a list of all available
lexers in order to generate the entry points for Pygments.

During execution this same list is used to create one `Lexer` class per Chroma lexer,
where Pygments expects them due to the entry points. When this classes
`get_tokens_unprocessed` method is called, it invokes Chroma with the `--json` option to
let chroma generate a list of tokens. Those tokens are then mapped to Pygments tokens
and returned.
