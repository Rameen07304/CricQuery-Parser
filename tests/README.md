# Tests for the CricQuery parser

Put this `tests` folder next to `cr.py`, then from that folder run:

```bash
python tests/run_tests.py        # run all tests
python tests/run_tests.py -v     # also print expected vs actual for failures
```

The runner types each query into `cr.py` (it reads from the keyboard) and
compares the `RESULT:` section of the output with the expected file.

## Folder layout

```
tests/
  run_tests.py
  cases/
    NAME.in     the query
    NAME.out    expected result: ACCEPTED/REJECTED, then each error line
    NAME.tree   (2 tests only) expected parse tree
```

To add a test, add a `.in` and a `.out` file with the same name.

## What is covered (47 tests)

| Prefix | Count | Covers |
|--------|-------|--------|
| `v`  | 18 | Valid queries: all relops, all stats, NOT NOT, nested and NOT brackets, no spaces, tabs and extra spaces, multi-line, 0 and very large numbers, leading zeros, long AND/OR chains, 100 nested brackets, a meaningless but valid query |
| `i`  | 28 | Invalid queries: missing LIST / SHOW / relop / number / `)`, nothing after SHOW, trailing and double comma, empty and whitespace-only input, wrong order, two queries, extra tokens, operator at start, dangling OR, empty brackets |
| `i`  | (same) | Lexical errors: unknown word, `#`, `-5`, `4.5`, `<=`, lowercase `list`, uppercase `NAME`; errors on line 2 (line numbers) |
| `t`  | 1  | Parse tree: AND is grouped left to right |
| `v03`| (in v) | Parse tree: AND binds tighter than OR, NOT tighter than AND |

Expected results were worked out by hand from the language rules and the
panic-mode recovery described in the report, not copied from the program's output.
