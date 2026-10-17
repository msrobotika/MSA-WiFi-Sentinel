"""Verify and install a WiFi Sentinel release without erasing the whole flash."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True)
    parser.add_argument("--mac", help="optional expected target MAC")
    parser.add_argument("--confirm-backup-made", action="store_true", required=True)
    parser.add_argument("--bin-dir", type=Path, default=Path(__file__).resolve().parents[1] / "bin")
    args = parser.parse_args()

    manifest = json.loads((args.bin_dir / "SHA256.json").read_text(encoding="utf-8"))
    for name, item in manifest.items():
        data = (args.bin_dir / name).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise SystemExit(f"Integrity check failed: {name}; nothing was written")

    base = [sys.executable, "-m", "esptool", "--port", args.port, "--baud", "115200"]
    probe = subprocess.run(base + ["chip-id"], capture_output=True, text=True, timeout=45)
    identity = (probe.stdout + probe.stderr).lower()
    if probe.returncode or "esp32-d0wd" not in identity:
        raise SystemExit("Supported ESP32-D0WD target was not confirmed; nothing was written")
    if args.mac and args.mac.lower() not in identity:
        raise SystemExit("Expected MAC was not confirmed; nothing was written")

    subprocess.run(
        base[:-1]
        + ["230400", "write-flash"]
        + [part for name, item in manifest.items() for part in (item["offset"], str(args.bin_dir / name))],
        check=True,
        timeout=180,
    )


if __name__ == "__main__":
    main()
