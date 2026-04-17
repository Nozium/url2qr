#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

import pyqrcode


def safe_filename_from_url(url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return f"qr_{digest}.png"


def render_terminal_qr(url: str) -> None:
    qr = pyqrcode.create(url)
    # quiet_zone=1 くらいの方が端末で見やすい
    print(qr.terminal(quiet_zone=1), end="")


def save_png(url: str, output_path: Path, scale: int = 6) -> Path:
    qr = pyqrcode.create(url)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    qr.png(str(output_path), scale=scale)
    return output_path.resolve()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a URL into a QR code, render in terminal, and save as PNG."
    )
    parser.add_argument("url", help="URL to encode as QR")
    parser.add_argument(
        "-o",
        "--output",
        help="Output PNG path. Default: ./qrcodes/<hash>.png",
        default=None,
    )
    parser.add_argument(
        "--no-terminal",
        action="store_true",
        help="Do not render QR in terminal",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=6,
        help="PNG scale factor (default: 6)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    url = args.url.strip()
    if not url:
        print("Error: URL is empty.", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("qrcodes") / safe_filename_from_url(url)

    try:
        if not args.no_terminal:
            render_terminal_qr(url)
            print()

        saved_path = save_png(url, output_path=output_path, scale=args.scale)
        print(f"PNG: file://{saved_path}")
        return 0

    except Exception as e:
        print(f"Error: failed to generate QR code: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
