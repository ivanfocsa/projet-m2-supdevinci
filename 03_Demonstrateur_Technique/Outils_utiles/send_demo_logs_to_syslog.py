from __future__ import annotations

import argparse
import socket
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_DIR = ROOT / "Demo_Logs"


def iter_log_lines(log_dir: Path, selected: list[str]) -> list[tuple[Path, str]]:
    files = [log_dir / name for name in selected] if selected else sorted(log_dir.glob("*.log"))
    events: list[tuple[Path, str]] = []
    for path in files:
        if not path.exists():
            raise FileNotFoundError(f"Log introuvable: {path}")
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line:
                events.append((path, line))
    return events


def send_udp(host: str, port: int, events: list[tuple[Path, str]], delay: float) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for _, line in events:
            sock.sendto(line.encode("utf-8"), (host, port))
            if delay:
                time.sleep(delay)


def send_tcp(host: str, port: int, events: list[tuple[Path, str]], delay: float) -> None:
    with socket.create_connection((host, port), timeout=5) as sock:
        for _, line in events:
            sock.sendall((line + "\n").encode("utf-8"))
            if delay:
                time.sleep(delay)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rejoue les logs de demonstration Daylight vers un collecteur syslog Wazuh."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Adresse Wazuh/syslog cible.")
    parser.add_argument("--port", type=int, default=514, help="Port syslog cible.")
    parser.add_argument("--protocol", choices=("udp", "tcp"), default="udp", help="Transport syslog.")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR, help="Dossier contenant les fichiers .log.")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Fichier log precis a rejouer, ex: --file pfsense.log. Repetable.",
    )
    parser.add_argument("--delay", type=float, default=0.05, help="Delai en secondes entre deux lignes.")
    parser.add_argument("--dry-run", action="store_true", help="Affiche les lignes sans les envoyer.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    log_dir = args.log_dir.resolve()
    events = iter_log_lines(log_dir, args.file)

    print("=== Rejeu logs demo Daylight / Cyber Trust ===")
    print(f"Dossier logs : {log_dir}")
    print(f"Cible        : {args.protocol.upper()} {args.host}:{args.port}")
    print(f"Evenements   : {len(events)}")

    if args.dry_run:
        print("")
        print("Mode dry-run, aucun envoi reseau.")
        for path, line in events:
            print(f"[{path.name}] {line}")
        return 0

    if args.protocol == "udp":
        send_udp(args.host, args.port, events, args.delay)
    else:
        send_tcp(args.host, args.port, events, args.delay)

    print("Envoi termine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
