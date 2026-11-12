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


## Assignment Reflection

This project showed me the difference between doing a one-off data analysis and creating a package that generalizes analysis scripts into something reusable. Based on the assignment description alone, I knew I would be able to reuse code from Homework 2 (the Serena Williams plot), but it was clear that much of it would need to be modified.

In the process of creating the `tenniscareer` package, generalizing the scripts was a big hurdle, not only due to the forewarned differences between male and female player data, but also simply for retrieving the necessary data for each player in the first place. For example, inspecting the Tennis Abstract site HTML led me to a secondary `.js` file which contained player metadata including the player's date of birth. This gave me a consistent source for the selected player's birth date regardless of whether the career data came from the male or female format, so I did not need separate logic for each case. Finding and using this additional data source made the final code simpler and more general, but required much more effort than hardcoding the site paths as I did in Homework 2.

The project was good practice for reproducibility and version control. After being marked down points for bundling unrelated changes in a previous assignment, I tried to focus on keeping my commits contained to specific changes. However, I decided not to use branches and pull requests as I did in previous assignments, as I felt their benefits were not as strong in solo work. I actually found this useful several times when I had to return to previous commits to fix an error, since keeping the work on a single branch made it easier to amend and rebase recent commits without having to reconcile additional branch or merge history.
