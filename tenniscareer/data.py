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
