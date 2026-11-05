import json
from datetime import date
from pathlib import Path

DB = Path("books.json")

def load():
    return json.loads(DB.read_text()) if DB.exists() else []

def save(books):
    DB.write_text(json.dumps(books, indent=2))

def find(books, book_id):
    return next((b for b in books if b["id"] == book_id), None)

def show(books, shelf=None):
    for b in books:
        if shelf and b["shelf"] != shelf:
            continue
        pct = round(100 * b["page"] / b["pages"]) if b["pages"] else 0
        print(f'[{b["id"]}] {b["title"]} - {b["author"]} ({b["shelf"]}, {pct}%)')

def main():
    books = load()
    while True:
        cmd = input("\n(add/list/start/update/finish/quit) > ").strip().lower()
        if cmd == "quit":
            break
        elif cmd == "add":
            books.append({
                "id": max((b["id"] for b in books), default=0) + 1,
                "title": input("title: "),
                "author": input("author: "),
                "pages": int(input("pages: ")),
                "page": 0,
                "shelf": "want",
                "started": None,
                "finished": None,
            })
        elif cmd == "list":
            show(books, input("shelf (want/reading/done, blank=all): ").strip() or None)
        elif cmd in ("start", "update", "finish"):
            b = find(books, int(input("id: ")))
            if not b:
                print("not found")
                continue
            if cmd == "start":
                b["shelf"], b["started"] = "reading", str(date.today())
            elif cmd == "update":
                b["page"] = min(int(input("current page: ")), b["pages"])
            else:
                b["shelf"], b["page"], b["finished"] = "done", b["pages"], str(date.today())
        save(books)

if __name__ == "__main__":
    main()
