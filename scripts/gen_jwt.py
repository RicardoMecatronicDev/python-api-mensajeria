"""Imprime uno o varios JWT nuevos (cada uno con jti unico).

Uso:
  JWT=$(python scripts/gen_jwt.py)                 # 1 token, 5 minutos
  python scripts/gen_jwt.py --count 20 --days 30   # 20 tokens, 30 dias
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.security import JWT_TTL_SEC, create_jwt  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera JWT unicos")
    parser.add_argument("--count", type=int, default=1, help="cantidad de tokens")
    parser.add_argument("--days", type=float, default=None, help="duracion en dias")
    args = parser.parse_args()
    ttl = int(args.days * 24 * 3600) if args.days else JWT_TTL_SEC
    for _ in range(args.count):
        print(create_jwt(ttl=ttl))


if __name__ == "__main__":
    main()
