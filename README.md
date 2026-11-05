# Reading Tracker

A simple CLI app to track books across three shelves: want, reading, done.

## Run it
    py tracker.py

## Design
Every book moves through want -> reading -> done. All books live in one JSON list. Shelves are just filters on the shelf field. Progress % is computed from page / pages, never stored.

## Roadmap
- [ ] Input validation
- [ ] Ratings and reviews
- [ ] Yearly reading goal and stats
- [ ] Recommendations
- [ ] Streamlit UI
