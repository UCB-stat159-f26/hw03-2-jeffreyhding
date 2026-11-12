import json
import re
import pandas as pd
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = "https://www.tennisabstract.com/jsmatches"


def _format_player_name(player_name):
    name = player_name.strip()
    if " " in name:
        return "".join(word.capitalize() for word in name.split())
    return name


def _career_url(player_name):
    player = _format_player_name(player_name)
    return f"{BASE_URL}/{player}Career.js"


def _download_career_data(player_name):
    request = Request(_career_url(player_name), headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        return response.read().decode("utf-8")


def _parse_career_js(text):
    data = text.split("=", 1)[1].strip().rstrip(";")
    return json.loads(data)


def _opponent_age_from_row(row):
    value = row[16]
    if not value:
        return float("nan")
    if value.isdigit() and len(value) == 8:
        match_date = pd.to_datetime(row[0], format="%Y%m%d")
        birth_date = pd.to_datetime(value, format="%Y%m%d")
        return (match_date - birth_date).days / 365.25
    return float(value)


def _matches_to_dataframe(matches):
    return pd.DataFrame({
        "match_date": [row[0] for row in matches],
        "tournament": [row[1] for row in matches],
        "surface": [row[2] for row in matches],
        "result": [row[4] for row in matches],
        "opponent": [row[11] for row in matches],
        "opponent_age": [_opponent_age_from_row(row) for row in matches],
    })


def _clean_match_dataframe(df):
    clean = df.copy()
    clean["match_date"] = pd.to_datetime(clean["match_date"], format="%Y%m%d")
    clean = clean[clean["result"].isin(["W", "L"])]
    return clean.reset_index(drop=True)


def _player_url(player_name):
    player = _format_player_name(player_name)
    return f"{BASE_URL}/{player}.js"


def _download_player_data(player_name):
    request = Request(_player_url(player_name), headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        return response.read().decode("utf-8")


def _extract_player_birth_date(player_data):
    match = re.search(r"var\s+dob\s*=\s*(\d{8})", player_data)
    if match is None:
        raise ValueError("Could not find player birth date")
    return pd.to_datetime(match.group(1), format="%Y%m%d")


def _add_player_age_columns(df, birth_date):
    enriched = df.copy()
    enriched["player_age"] = (
        (enriched["match_date"] - birth_date).dt.days / 365.25
    )
    enriched["age_difference"] = (
        enriched["player_age"] - enriched["opponent_age"]
    )
    return enriched



def get_player_matches(player_name):
    try:
        matches = _parse_career_js(_download_career_data(player_name))
        player_data = _download_player_data(player_name)
    except HTTPError as error:
        raise ValueError(f"Player not found: {player_name}") from None

    df = _clean_match_dataframe(_matches_to_dataframe(matches))
    birth_date = _extract_player_birth_date(player_data)
    return _add_player_age_columns(df, birth_date)
