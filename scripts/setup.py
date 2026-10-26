"""Create local configuration without overwriting existing credentials."""
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parents[1]

def main():
    target = ROOT / ".env"
    if target.exists():
        print("Existing .env preserved.")
        return
    lines = []
    for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator and value == "CHANGE_ME":
            value = secrets.token_urlsafe(24)
        lines.append(key + separator + value)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Created .env with random local passwords; values were not printed.")

if __name__ == "__main__":
    main()
