# CricQuery Parser

A lexer and recursive-descent (LL(1)) parser in Python for CricQuery, a small
language for searching cricket statistics. It prints the tokens, the parse tree
and ACCEPTED/REJECTED, reports lexical and syntax errors with line numbers, and
recovers from errors (panic mode) so the rest of the program is still checked.

```
LIST runs > 500 AND NOT wickets < 10 SHOW name , average
```

## Run

Python 3.8+ (standard library only).

```bash
git clone https://github.com/Rameen07304/CricQuery-Parser.git
cd CricQuery-Parser
python cr.py
```

Type or paste the query, then press Enter on an empty line to finish.
To run a saved test file instead:

```bash
python cr.py < tests/valid1.txt
```

Note: a blank line ends the input, so a query must not contain blank lines.
An empty query (empty-file test) is entered by pressing Enter immediately.

## Files

```
CricQuery-Parser/
├── cr.py       # lexer, parser, parse-tree printer, main
├── README.md
└── tests/      # a few sample queries (valid, invalid, edge cases)
```

## Grammar (after removing ambiguity and left recursion)

```
Q  -> LIST C SHOW F
C  -> D C'        C' -> OR D C' | epsilon
D  -> E D'        D' -> AND E D' | epsilon
E  -> NOT E | P
P  -> ( C ) | stat relop num
F  -> G F'        F' -> , G F' | epsilon
G  -> name | stat
```

Precedence: `NOT` (highest, right-assoc), `AND`, `OR` (lowest, left-assoc).

## Assumptions

- Keywords are case-sensitive: `LIST SHOW AND OR NOT`, and `name` in lower case.
- Stats: `runs wickets average matches`. Relops: `<` `>` `=`.
- Numbers are whole numbers only (no sign, no decimal point).
- Any other word or symbol (e.g. `#`, `-`, `sixes`) is a lexical error.
- Only syntax is checked, not meaning (`runs > 5 AND runs < 2` is accepted).
- One query per file.