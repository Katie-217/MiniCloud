"""Update one output row while preserving the hand-written progress report."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def set_status(output, status, evidence):
    path = ROOT / "TIEN_DO_OUTPUT.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    found = False
    for index, line in enumerate(lines):
        if line.startswith(f"| {output} |"):
            cells = [part.strip() for part in line.split("|")[1:-1]]
            cells[-2:] = [status, evidence.replace("|", "/")]
            lines[index] = "| " + " | ".join(cells) + " |"
            found = True
            break
    if not found:
        raise ValueError(f"Unknown output {output}")
    text = "\n".join(lines) + "\n"
    mandatory = len(re.findall(r"^\| R\d+ \|.*\| DAT \|", text, re.M))
    extensions = len(re.findall(r"^\| E\d+ \|.*\| DAT \|", text, re.M))
    text = re.sub(r"Output bắt buộc đạt: \d+/18", f"Output bắt buộc đạt: {mandatory}/18", text)
    text = re.sub(r"Mở rộng đạt: \d+/10", f"Mở rộng đạt: {extensions}/10", text)
    path.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    set_status(*sys.argv[1:])
