# %% Imports
import altair as alt
import polars as pl
import re
import os

# %% Read all csv data into one dataframe
df_dict = {}

for filename in os.listdir("../output_data/haushalts_daten"):
    file = pl.read_csv(f"../output_data/haushalts_daten/{filename}", separator=";")
    df_dict[re.findall(r"(.*)(?:\.csv)", filename)[0]] = file

# %% Generate chart from combined data
schema = {
    "id": pl.Int64,
    "year": pl.String,
    "amount": pl.Int64,
    "function": pl.String,
    "title": pl.String,
}

total = pl.read_csv("../input_data/haushalt_total/hh_total.csv", schema=schema)

selection = alt.selection_point(fields=["function"])
color = alt.condition(
    selection, alt.Color("function:N").legend(None), alt.value("lightgray")
)

scatter = (
    alt.Chart(total)
    .mark_bar()
    .encode(x="year:N", y="amount:Q", color=color, tooltip="title:N")
)

legend = (
    alt.Chart(total)
    .mark_point()
    .encode(alt.Y("title:N").axis(orient="right"), color=color)
    .add_params(selection)
)

scatter | legend

# %% Alternative chart with logarithmic scale
schema = {
    "id": pl.Int64,
    "year": pl.String,
    "amount": pl.Int64,
    "function": pl.String,
    "title": pl.String,
}

total = pl.read_csv("../input_data/haushalt_total/hh_total.csv", schema=schema)

selection = alt.selection_point(fields=["function"])
color = alt.condition(
    selection, alt.Color("function:N").legend(None), alt.value("lightgray")
)

scatter = (
    alt.Chart(total)
    .mark_point()
    .encode(
        x="year:N",
        y=alt.Y("amount:Q").scale(type="log"),
        color=color,
        tooltip="title:N",
    )
)

legend = (
    alt.Chart(total)
    .mark_point()
    .encode(alt.Y("title:N").axis(orient="right"), color=color)
    .add_params(selection)
)

scatter | legend

# %% Calculate slope
