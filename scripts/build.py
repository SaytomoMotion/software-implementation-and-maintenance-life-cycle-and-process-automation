"""Build a deterministic standard-library Python zip application."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path


def build(output, revision="development"):
    root = Path(__file__).resolve().parents[1]
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    content = {"__main__.py": b"from motiontracker.cli import main\nraise SystemExit(main())\n",
               "build-info.json": (json.dumps({"application": "Motion Design Project Manager",
                                                "version": "1.0.0", "schema_version": 2,
                                                "source_revision": revision}, sort_keys=True) + "\n").encode()}
    for package in ("motiontracker", "tasktracker"):
        for path in (root / package).rglob("*"):
            if path.is_file() and path.suffix in {".py", ".sql"}:
                content[path.relative_to(root).as_posix()] = path.read_bytes().replace(b"\r\n", b"\n")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(content.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(digest + "  " + output.name + "\n", encoding="utf-8")
    return {"artifact": str(output), "sha256": digest, "source_revision": revision}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="dist/motiondesk.pyz")
    parser.add_argument("--revision", default="development")
    arguments = parser.parse_args()
    print(json.dumps(build(arguments.output, arguments.revision), indent=2))


if __name__ == "__main__":
    main()
