import os
from pathlib import Path


def mask(v):
    if v is None:
        return None
    v = str(v)
    if len(v) <= 8:
        return v[0:1] + "***"
    return v[:4] + "..." + v[-4:]


def main():
    ak = os.getenv("ANTHROPIC_API_KEY")
    aut = os.getenv("ANTHROPIC_AUTH_TOKEN")
    print("ANTHROPIC_API_KEY set:", ak is not None)
    print("ANTHROPIC_API_KEY masked:", mask(ak))
    print("ANTHROPIC_AUTH_TOKEN set:", aut is not None)
    print("ANTHROPIC_AUTH_TOKEN masked:", mask(aut))

    p = Path("c:/Users/yysun/Documents/MCP_Course/.env")
    print(".env exists at project root:", p.exists())
    if p.exists():
        print("\nFirst 20 lines of .env (masked values):")
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
            if i >= 20:
                break
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                print(f"{k.strip()}={mask(v.strip())}")
            else:
                print(line)

    # Additional diagnostics to help debug authentication issues (no secrets printed)
    print('\n--- Diagnostic checks (no secret shown) ---')
    def diag(name, val):
        if val is None:
            print(f"{name}: not set")
            return
        s = str(val)
        print(f"{name}: set -> masked={mask(s)}, length={len(s)}, startswith_sk={s.startswith('sk-')}, has_quotes={s.startswith(('"', "'")) or s.endswith(('"', "'"))}, has_whitespace={s.strip() != s}")

    diag('ANTHROPIC_API_KEY (env)', ak)
    diag('ANTHROPIC_AUTH_TOKEN (env)', aut)


if __name__ == "__main__":
    main()
