"""Test runner for the CricQuery parser (cr.py).

Usage (from the project folder):
    python tests/run_tests.py            # tests ../cr.py
    python tests/run_tests.py -v         # also show the actual output of failures
    python tests/run_tests.py path/to/other_parser.py

How it works
------------
cr.py reads its query from the keyboard (stdin), so every test feeds a file to
it exactly like typing the query. For each case in tests/cases/:

    NAME.in     the query that is typed in
    NAME.out    expected RESULT section: first line ACCEPTED or REJECTED,
                then every expected error message, one per line, in order
    NAME.tree   (optional) expected PARSE TREE section, checked exactly

A test passes only if the real output matches the .out (and .tree) file.
Exit code is 0 when all tests pass, 1 otherwise.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = HERE / "cases"


def run_parser(script, query_text):
    proc = subprocess.run(
        [sys.executable, str(script)],
        input=query_text,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return proc.stdout, proc.stderr, proc.returncode


def section(output, start, end=None):
    """Lines after the line 'start:' up to the line 'end:' (or the end)."""
    lines = output.splitlines()
    if start not in lines:
        return None
    i = lines.index(start) + 1
    j = lines.index(end) if end and end in lines else len(lines)
    return [l.rstrip() for l in lines[i:j]]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv
    script = Path(args[0]).resolve() if args else HERE.parent / "cr.py"
    if not script.exists():
        print(f"Cannot find {script}")
        return 1

    names = sorted(p.stem for p in CASES.glob("*.in"))
    failed = []
    for name in names:
        query = (CASES / f"{name}.in").read_text()
        expected = (CASES / f"{name}.out").read_text().splitlines()
        tree_file = CASES / f"{name}.tree"

        try:
            out, err, code = run_parser(script, query)
        except subprocess.TimeoutExpired:
            failed.append((name, "timed out (infinite loop?)", ""))
            print(f"FAIL  {name}  (timeout)")
            continue

        problems = []
        if code != 0:
            problems.append(f"program crashed (exit {code}): {err.strip().splitlines()[-1] if err.strip() else ''}")
        actual = section(out, "RESULT:")
        if actual is None:
            problems.append("no RESULT: section in output")
        elif actual != expected:
            problems.append("result/errors differ")
        if tree_file.exists():
            actual_tree = section(out, "PARSE TREE:", "RESULT:")
            if actual_tree is not None:
                actual_tree = [l for l in actual_tree if l.strip() != ""]
            if actual_tree != tree_file.read_text().splitlines():
                problems.append("parse tree differs")

        if problems:
            failed.append((name, "; ".join(problems), out))
            print(f"FAIL  {name}  ({'; '.join(problems)})")
            if verbose:
                print("  expected:", expected)
                print("  actual:  ", actual)
        else:
            print(f"pass  {name}")

    total = len(names)
    print(f"\n{total - len(failed)}/{total} tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
