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
