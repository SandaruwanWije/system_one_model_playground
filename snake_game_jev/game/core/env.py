import os
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def load_dotenv(path=None):
    env_path = Path(path) if path else ENV_PATH
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if key and value:
                os.environ.setdefault(key, value)


def save_env_value(key, value, path=None):
    env_path = Path(path) if path else ENV_PATH
    lines = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()

    prefix = f"{key}="
    updated = False
    next_lines = []
    for line in lines:
        if line.startswith(prefix) or line.startswith(f"#{prefix}"):
            next_lines.append(f"{key}={value}")
            updated = True
        else:
            next_lines.append(line)
    if not updated:
        if next_lines and next_lines[-1].strip():
            next_lines.append("")
        next_lines.append(f"{key}={value}")

    env_path.write_text("\n".join(next_lines) + "\n", encoding="utf-8")
