import json
import os
from datetime import date
from pathlib import Path

DB = Path(__file__).parent / "books.json"


def load():
    if not DB.exists():
        return []
    try:
        return json.loads(DB.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        backup = DB.with_suffix(".json.corrupt")
        os.replace(DB, backup)
        print(f"books.json was corrupted. Moved to {backup.name}, starting fresh.")
        return []


def save(books):
    tmp = DB.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, DB)


def ask_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Enter a whole number.")
            continue
        if min_val is not None and value < min_val:
            print(f"Must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Must be at most {max_val}.")
            continue
        return value


def ask_str(prompt):
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Can't be empty.")


def ask_shelf(prompt):
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("", "want", "reading", "done"):
            return raw or None
        print("Pick want, reading, done, or leave blank.")


def progress_pct(b):
    return round(100 * b["page"] / b["pages"]) if b["pages"] > 0 else 0


def find(books, book_id):
    return next((b for b in books if b["id"] == book_id), None)


def show(books, shelf=None):
    for b in books:
        if shelf and b["shelf"] != shelf:
            continue
        print(f'[{b["id"]}] {b["title"]} - {b["author"]} ({b["shelf"]}, {progress_pct(b)}%)')


def main():
    books = load()
    while True:
        cmd = input("\n(add/list/start/update/finish/quit) > ").strip().lower()
        if cmd == "quit":
            break
        elif cmd == "add":
            books.append({
                "id": max((b["id"] for b in books), default=0) + 1,
                "title": ask_str("title: "),
                "author": ask_str("author: "),
                "pages": ask_int("pages: ", min_val=1),
                "page": 0,
                "shelf": "want",
                "started": None,
                "finished": None,
            })
        elif cmd == "list":
            show(books, ask_shelf("shelf (want/reading/done, blank=all): "))
        elif cmd in ("start", "update", "finish"):
            b = find(books, ask_int("id: "))
            if not b:
                print("not found")
                continue
            if cmd == "start":
                b["shelf"], b["started"] = "reading", str(date.today())
            elif cmd == "update":
                b["page"] = ask_int("current page: ", min_val=0, max_val=b["pages"])
            else:
                b["shelf"], b["page"], b["finished"] = "done", b["pages"], str(date.today())
        else:
            print("Unknown command.")
            continue
        save(books)


if __name__ == "__main__":
    main()
    