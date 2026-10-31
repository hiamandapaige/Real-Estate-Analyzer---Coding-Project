# Real Estate Deal Analyzer

A tool that collects home listings, estimates what each property is worth
using similar nearby homes, and flags listings priced below that estimate.
I'm building it to learn Python and to help investors spot deals quickly.

## Setup

1. Create and turn on the virtual environment:

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Create the database:

   ```
   python3 -m app.db
   ```

## Project structure

- `app/`: the project's code
- `data/`: listings and the database (not saved to Git)
- `tests/`: code that checks the code
