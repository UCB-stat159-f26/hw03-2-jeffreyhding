# tenniscareer

`tenniscareer` is a Python package for retrieving professional tennis players' career match data from [Tennis Abstract](https://www.tennisabstract.com/) and visualizing the age difference between a player and their opponents throughout their career.


## Installation

Install the package directly from GitHub:

~~~bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-jeffreyhding.git
~~~


## Usage

The package provides two public functions:

- `get_player_matches()` retrieves and processes a player's career match data.
- `plot_age_difference()` plots match outcomes by the player's age and age difference from their opponent.


### Example Use Cases

**1. Serena Williams**

~~~python
from tenniscareer import get_player_matches, plot_age_difference

serena = get_player_matches("Serena Williams")
plot_age_difference(serena)
~~~

Player names can also be provided in other formats:

~~~python
serena = get_player_matches("serena williams")
serena = get_player_matches("SerenaWilliams")
~~~

**2. Rafael Nadal**

~~~python
nadal = get_player_matches("Rafael Nadal")
plot_age_difference(nadal)
~~~


### Invalid Players

If Tennis Abstract does not contain career data for the requested player, `get_player_matches()` raises a `ValueError`:

~~~python
get_player_matches("Richaun Holmes")
~~~

~~~text
ValueError: Player not found: Richaun Holmes
~~~


## Match Data

`get_player_matches()` returns a `pandas` DataFrame with the following columns:

- `match_date`: date of the match
- `tournament`: tournament name
- `surface`: playing surface
- `result`: win (`W`) or loss (`L`)
- `opponent`: opponent name
- `opponent_age`: opponent's age at the time of the match
- `player_age`: selected player's age at the time of the match
- `age_difference`: selected player's age minus opponent's age


## Tests

The test suite uses static mock Tennis Abstract data rather than making live web requests.

Run the tests with:

~~~bash
pytest tenniscareer
~~~
