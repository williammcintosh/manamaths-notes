#!/usr/bin/env python3
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
MM_TRACKER = WORKSPACE / "manamaths/OPERATIONS/data/lo-tracker.json"
NOTES_ROOT = WORKSPACE / "manamaths-notes"
OUTPUT = NOTES_ROOT / "OPERATIONS/data/notes-tracker.json"


def main():
    mm = json.loads(MM_TRACKER.read_text())
    objectives = mm.get("learningObjectives", [])
    rows = []
    complete = 0
    started = 0
    not_started = 0

    for lo in objectives:
        slug = lo["slug"]
        folder = NOTES_ROOT / "OBJECTIVES" / slug
        source = folder / "main.tex"
        pdf = folder / "build" / "main.pdf"

        if source.exists() and pdf.exists():
            status = "complete"
            complete += 1
        elif source.exists() or folder.exists():
            status = "started"
            started += 1
        else:
            status = "not_started"
            not_started += 1

        rows.append({
            "objectiveId": lo.get("objectiveId"),
            "canonicalTopicId": lo.get("canonicalTopicId"),
            "canonicalInternalCode": lo.get("canonicalInternalCode"),
            "canonicalSourceCode": lo.get("canonicalSourceCode"),
            "canonicalTitle": lo.get("canonicalTitle"),
            "canonicalDisplayTitle": lo.get("canonicalDisplayTitle"),
            "slug": slug,
            "notesStatus": status,
            "paths": {
                "folder": str(folder.relative_to(WORKSPACE)),
                "source": str(source.relative_to(WORKSPACE)),
                "pdf": str(pdf.relative_to(WORKSPACE)),
            },
            "evidence": {
                "folder": folder.exists(),
                "source": source.exists(),
                "pdf": pdf.exists(),
            },
        })

    payload = {
        "canonicalSource": "manamaths/OPERATIONS/data/lo-tracker.json",
        "generatedAtRepoPath": "manamaths-notes/OPERATIONS/data/notes-tracker.json",
        "notes": [
            "This tracker records which Mana Maths learning objectives have Notes modules in manamaths-notes.",
            "Notes mirror Mana Maths LOs one-to-one using the same objectiveId, code, title, and slug.",
            "Use this file to answer requests like 'pick up where we last left off'.",
            "This file is generated from the Mana Maths LO tracker plus the actual manamaths-notes filesystem state."
        ],
        "summary": {
            "totalObjectives": len(objectives),
            "notesComplete": complete,
            "notesStarted": started,
            "notesNotStarted": not_started,
        },
        "learningObjectives": rows,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
