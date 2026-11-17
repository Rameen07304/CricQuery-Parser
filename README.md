# CricQuery Parser (Assignment 2 – Compiler Construction)

**Name:** Rameen Fatima  **Roll no.:** F23BSCS031  **Section:** C
**Submitted to:** Mam Huma  **Topic:** Group 2 – CricQuery

A lexer and a recursive-descent (top-down, LL(1)) parser for CricQuery, a small
language for searching a table of cricket statistics.

```
LIST runs > 500 AND NOT wickets < 10 SHOW name , average
```

## Files

| File | Purpose |
|------|---------|
| `cr.py` | Source code: lexer, `Parser` class, parse-tree printer, main program |
| `cc_ass2.docx` | Report: grammar fixing, parser design, FIRST/FOLLOW, parse table, tests |
| `README.md` | This file |

## Requirements

- Python 3.8 or later
- Standard library only (no packages to install)

## How to run

```bash
python cr.py <input_file>
```

For example, if the query is saved in `query.txt`:

```bash
python cr.py query.txt
```

> Adjust this section if your `main` reads input differently (for example from
> standard input or a built-in list of tests).

## What the program prints

For each program the output has four parts:

1. **Token list**: each token as `(type, text, line number)`.
2. **Parse tree**: start symbol `Q` at the root, non-terminals as inner nodes,
   matched tokens as leaves.
3. **Result**: `ACCEPTED` (no lexical and no syntax errors) or `REJECTED`.
4. **Errors**: every lexical error and syntax error, each with its line number.

Example messages:

```
Lexical error at line 2: unexpected '#'
Syntax error at line 1: found 'SHOW', expected number.
```

The end of input is shown as `$`.

## Grammar used (after removing ambiguity and left recursion)

```
(1)  Q  -> LIST C SHOW F          (9)  E  -> P
(2)  C  -> D C'                   (10) P  -> ( C )
(3)  C' -> OR D C'                (11) P  -> stat relop num
(4)  C' -> epsilon                (12) F  -> G F'
(5)  D  -> E D'                   (13) F' -> , G F'
(6)  D' -> AND E D'               (14) F' -> epsilon
(7)  D' -> epsilon                (15) G  -> name
(8)  E  -> NOT E                  (16) G  -> stat
```

Precedence (highest to lowest): `NOT` (right-associative), `AND` (left), `OR` (left).

Each non-terminal has one function in the code:

| Non-terminal | Function |
|--------------|----------|
| Q | `parse_query()` |
| C, C' | `parse_condition()` |
| D, D' | `parse_and()` |
| E, P | `parse_not()` |
| F, F' | `parse_fields()` |
| G | `parse_field()` |

## Error recovery

Panic mode. On an error the parser records it and calls `skip()`, which discards
tokens until a synchronising token (taken from the FOLLOW sets) and then carries
on, so all errors in a program are reported in one run. A missing `LIST`, relop,
number or `)` is reported and parsing continues as if the symbol had been there.
The lexer reports an unexpected symbol, skips it, and continues.

## Assumptions

- Keywords are **case-sensitive**: `LIST SHOW AND OR NOT` are upper case and
  `name` is lower case. `list` or `Runs` is not recognised.
- Statistics are exactly `runs`, `wickets`, `average`, `matches`.
- Relational operators are only `<`, `>` and `=` (no `<=`, `>=`, `!=`).
- Numbers are whole numbers (digits only): no sign and no decimal point, so
  `-5` and `4.5` give lexical errors.
- Any other word (for example `sixes`) or symbol (`#`, `$`, `-`, `.`) is an
  unexpected symbol.
- Whitespace is optional between tokens, so `runs>500` works.
- Only syntax is checked, not meaning: `runs > 5 AND runs < 2` is accepted.
- One query per program. Tokens after the end of the query are reported as a
  syntax error.
- One mistake can sometimes cause follow-on error messages; the first message
  of a run is the most reliable.