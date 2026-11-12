import pandas as pd
import pytest

from tenniscareer.data import (
    _clean_match_dataframe,
    _format_player_name,
    _matches_to_dataframe,
    _opponent_age_from_row,
    _parse_career_js,
    _extract_player_birth_date,
    _player_url,
)

from .mock_data import (
    FEMALE_JS,
    MALE_JS,
    NADAL_PLAYER_JS,
    SERENA_PLAYER_JS,
)


def test_format_player_name():
    assert _format_player_name("serena williams") == "SerenaWilliams"
    assert _format_player_name("Serena Williams") == "SerenaWilliams"
    assert _format_player_name("SerenaWilliams") == "SerenaWilliams"


def test_parse_female_career_js():
    matches = _parse_career_js(FEMALE_JS)
    assert len(matches) == 3
    assert len(matches[0]) == 27
    assert matches[0][11] == "Anne Miller"


def test_parse_male_career_js():
    matches = _parse_career_js(MALE_JS)
    assert len(matches) == 3
    assert len(matches[0]) == 47
    assert matches[0][11] == "Guillermo Platel"


def test_extract_shared_match_fields():
    matches = _parse_career_js(MALE_JS)
    df = _matches_to_dataframe(matches)

    assert list(df.columns) == [
        "match_date", "tournament", "surface", "result", "opponent",
        "opponent_age"
    ]
    assert df.loc[2, "result"] == "W"
    assert df.loc[2, "opponent"] == "Israel Matos Gil"


def test_clean_match_dataframe():
    matches = _parse_career_js(MALE_JS)
    df = _clean_match_dataframe(_matches_to_dataframe(matches))

    assert pd.api.types.is_datetime64_any_dtype(df["match_date"])
    assert set(df["result"]) == {"W", "L"}
    assert list(df.index) == [0, 1, 2]


def test_female_opponent_age_from_birth_date():
    matches = _parse_career_js(FEMALE_JS)
    age = _opponent_age_from_row(matches[0])
    assert age == pytest.approx(18.7762, abs=0.001)


def test_male_opponent_age_from_age_field():
    matches = _parse_career_js(MALE_JS)
    age = _opponent_age_from_row(matches[0])
    assert age == pytest.approx(22.2642, abs=0.001)


def test_player_metadata_url():
    assert _player_url("Serena Williams").endswith("/SerenaWilliams.js")
    assert _player_url("Rafael Nadal").endswith("/RafaelNadal.js")


def test_extract_player_birth_date():
    assert _extract_player_birth_date(SERENA_PLAYER_JS) == pd.Timestamp("1981-09-26")
    assert _extract_player_birth_date(NADAL_PLAYER_JS) == pd.Timestamp("1986-06-03")


def test_missing_player_birth_date():
    with pytest.raises(ValueError, match="Could not find player birth date"):
        _extract_player_birth_date("var fullname = 'Unknown Player';")
