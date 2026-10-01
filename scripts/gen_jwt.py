"""Imprime un JWT nuevo (jti unico). Uso: JWT=$(python scripts/gen_jwt.py)"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.security import create_jwt  # noqa: E402

if __name__ == "__main__":
    print(create_jwt())
