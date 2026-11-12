import matplotlib.pyplot as plt


def plot_age_difference(df):
    player_name = df.attrs["player_name"]
    short_name = player_name.split()[0]
    min_age = int(df["player_age"].min())
    max_age = int(df["player_age"].max())

    fig, ax = plt.subplots(figsize=(12, 7))

    for result, label, color in [("W", "Won", "#70C8E9"), ("L", "Lost", "#8A4088")]:
        matches = df[df["result"] == result]
        ax.scatter(matches["player_age"], matches["age_difference"],
                   label=label, color=color, alpha=0.75, s=16)
        
    ax.axhline(0, color="gray", linewidth=1)

    ax.grid(color="lightgray", linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)

    ax.set_xlabel(f"{player_name}'s age")
    ax.set_ylabel(f"Age difference: {short_name} - opponent")
    ax.set_title(
        f"{player_name}'s Professional Matches, Age {min_age} to {max_age}",
        loc="left",
    )

    ax.legend(frameon=False)

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()

    return fig, ax
