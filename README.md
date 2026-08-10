# Chess_analyser


![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

A Python tool that pulls chess games from the Chess.com and Lichess public APIs, normalizes them into a shared schema, and stores them in a local database for analysis (and eventually ML).

## Table of contents

- [Why](#why)
- [Features](#features)
- [Project structure](#project-structure)
- [Data sources](#data-sources)
- [Setup](#setup)
- [Usage](#usage)
- [Data model](#data-model)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Why

Chess.com and Lichess both expose free public APIs with rich per-game data (players, ratings, time control, opening, full PGN, results). This project ingests that data into one consistent format so it can be queried, analyzed, and eventually used as training data for models (e.g. predicting outcomes from opening + rating, spotting blunder patterns, opening trend analysis).

## Features

- [ ] Fetch a player's game archive from the Chess.com Published-Data API
- [ ] Fetch a player's games from the Lichess API
- [ ] Normalize both sources into a shared `Game` / `Player` schema
- [ ] Store games in SQLite (via SQLAlchemy)
- [ ] Parse PGN move data with `python-chess` (openings, material swings, move counts)
- [ ] CLI to track a list of usernames and backfill / incrementally update
- [ ] Basic analysis layer (pandas stats, simple sklearn model)

## Project structure

chess-tracker/
├── clients/
│ ├── chesscom.py # Chess.com API client
│ └── lichess.py # Lichess API client
├── models.py # SQLAlchemy models: Player, Game, Opening
├── ingest.py # fetch -> normalize -> store
├── db.py # engine/session setup
├── analysis/ # notebooks/scripts for stats and ML
├── main.py # CLI entrypoint
├── requirements.txt
└── README.md

## Data sources

- [Chess.com Published-Data API](https://www.chess.com/news/view/published-data-api) — no auth required
- [Lichess API](https://lichess.org/api) — no auth required for public data; supports PGN and NDJSON export

## Setup

```bash
git clone https://github.com/<your-username>/chess-tracker.git
cd chess-tracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py track <username> --source chesscom
python main.py track <username> --source lichess
python main.py sync
```

*(CLI is still being built — this section will be updated as commands land.)*

## Data model

Both APIs return different shapes; games are normalized into a common schema roughly like:

| Field         | Description                                  |
|---------------|-----------------------------------------------|
| `id`          | Unique game ID                                |
| `source`      | `chesscom` or `lichess`                       |
| `white_id` / `black_id` | Player references                  |
| `result`      | `1-0`, `0-1`, `1/2-1/2`                        |
| `time_control`| `bullet`, `blitz`, `rapid`, `classical`       |
| `eco`         | ECO opening code                              |
| `opening_name`| Human-readable opening name                   |
| `date`        | Date/time played                              |
| `pgn`         | Full move list in PGN format                  |

## Roadmap

1. Chess.com client → fetch and print one player's monthly archive
2. SQLite storage via SQLAlchemy
3. Lichess client, normalized into the same schema
4. `python-chess` parsing for openings, move counts, material swings
5. CLI for tracking/backfilling multiple usernames
6. Analysis layer: pandas stats, simple sklearn model

## Contributing

This is currently a personal/learning project, but issues and suggestions are welcome. If you'd like to contribute:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Open a pull request

## License

MIT — see [LICENSE](LICENSE) for details.
