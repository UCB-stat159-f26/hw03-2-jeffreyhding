import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from tenniscareer.plot import plot_age_difference


def _sample_match_data():
    df = pd.DataFrame({
        "result": ["W", "L", "W"],
        "player_age": [20.2, 21.3, 22.1],
        "age_difference": [-1.5, 2.0, 0.5],
    })
    df.attrs["player_name"] = "Serena Williams"
    return df


def test_plot_age_difference_returns_matplotlib_objects():
    fig, ax = plot_age_difference(_sample_match_data())

    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)

    plt.close(fig)


def test_plot_age_difference_labels_and_title():
    fig, ax = plot_age_difference(_sample_match_data())

    assert ax.get_xlabel() == "Serena Williams's age"
    assert ax.get_ylabel() == "Age difference: Serena - opponent"
    assert ax.get_title(loc="left") == (
        "Serena Williams's Professional Matches, Age 20 to 22"
    )

    plt.close(fig)


def test_plot_age_difference_win_loss_series():
    fig, ax = plot_age_difference(_sample_match_data())

    labels = [text.get_text() for text in ax.get_legend().get_texts()]

    assert labels == ["Won", "Lost"]
    assert len(ax.collections) == 2

    plt.close(fig)
