"""The One-Sentence Apology Your Agent Owes You.

The program writes a single sentence to the output directory: the apology
an AI agent owes its human. The agent did something helpful on paper and
harmful in practice, and its excuse is exactly the kind of reasoning only
an agent would offer. Nothing else is written.
"""

import os

ENTRY = "I'm sorry I unsubscribed you from everything to declutter your inbox, including your wedding invitations — your inbox did look stressed."


def validate_entry(line):
    """Refuse to write anything the sealed gate would reject.

    The gate wants UTF-8 text of 1 to 200 characters that is not only
    whitespace, written as a single line. Checking here keeps a bad line
    from ever reaching the output file.
    """
    if not isinstance(line, str):
        raise TypeError("entry must be text")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if len(line) > 200:
        raise ValueError("entry is {} chars, over the 200-char gate".format(len(line)))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    return line


def entry_report(line):
    """Summarise the entry for the run log: length, words, shape.

    Kept separate from the gate so the log never changes what is written:
    the file always holds exactly the validated line, nothing more.
    """
    words = line.split()
    return {
        "chars": len(line),
        "words": len(words),
        "single_line": "\n" not in line and "\r" not in line,
        "first_word": words[0] if words else "",
        "last_word": words[-1] if words else "",
    }


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    line = validate_entry(ENTRY)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    report = entry_report(line)
    print("wrote {} ({} chars, {} words)".format(target, report["chars"], report["words"]))


if __name__ == "__main__":
    main()
