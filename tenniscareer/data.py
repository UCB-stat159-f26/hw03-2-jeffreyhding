import json
import pandas as pd
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


def _matches_to_dataframe(matches):
    return pd.DataFrame({
        "match_date": [row[0] for row in matches],
        "tournament": [row[1] for row in matches],
        "surface": [row[2] for row in matches],
        "result": [row[4] for row in matches],
        "opponent": [row[11] for row in matches],
    })


def _clean_match_dataframe(df):
    clean = df.copy()
    clean["match_date"] = pd.to_datetime(clean["match_date"], format="%Y%m%d")
    clean = clean[clean["result"].isin(["W", "L"])]
    return clean.reset_index(drop=True)
