from __future__ import annotations

import sys

from .commands import DEFAULT_DB_PATH, cli, write_entry


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        exit_code = write_entry(db_path=DEFAULT_DB_PATH)
        raise SystemExit(exit_code)
    cli()


if __name__ == "__main__":
    main()
