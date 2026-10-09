"""A typical ops script: collect commit subjects since the last tag, read the
service config, and write release notes plus a log file. Every call that
check_default_encoding.py reports is one that changes with the locale before
3.15, or with UTF-8 mode from 3.15."""
import configparser
import json
import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(filename="release.log", level=logging.INFO)


def commits_since(tag):
    out = subprocess.run(["git", "log", f"{tag}..HEAD", "--format=%s"],
                         capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


def main(tag):
    config = configparser.ConfigParser()
    config.read_string(Path("service.ini").read_text())
    template = open("templates/notes.md.tmpl").read()
    subjects = commits_since(tag)
    notes = template.format(service=config["service"]["name"], changes="\n".join(subjects))
    Path("RELEASE_NOTES.md").write_text(notes)
    with open("release.json", "w") as f:
        json.dump({"tag": tag, "changes": subjects}, f, ensure_ascii=False)
    with open("release.json", "rb") as f:  # binary: not reported
        logging.info("wrote %d bytes", len(f.read()))


if __name__ == "__main__":
    main(sys.argv[1])
