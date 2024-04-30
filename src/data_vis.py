# %% Imports
import altair as alt
import polars as pl
import re
import os

# %%
# Read all csv data into one dataframe
df_dict = {}

for filename in os.listdir("../output_data/haushalts_daten/nach_hauptfunktion"):
    file = pl.read_csv(
        f"../output_data/haushalts_daten//nach_hauptfunktion{filename}", separator=";"
    )
    df_dict[re.findall(r"(.*)(?:\.csv)", filename)[0]] = file

# %%
# Generate bar chart from combined data
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

# %%
# Alternative chart with logarithmic scale
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

# %%
# Calculate slope
slope_series = []
sorted_total = total.sort("function")

curr_func = None
old_amount = None
for entry in sorted_total.rows(named=True):
    if curr_func == entry["function"]:
        slope_series.append(old_amount / entry["amount"])
        old_amount = entry["amount"]
    else:
        curr_func = entry["function"]
        old_amount = entry["amount"]

sorted_total = sorted_total.filter(pl.col("year") != "2014").with_columns(
    pl.Series(slope_series).alias("slope")
)
# %%
# Visualize slope

selection = alt.selection_point(fields=["function"])
color = alt.condition(
    selection, alt.Color("function:N").legend(None), alt.value("lightgray")
)
scatter = (
    alt.Chart(sorted_total)
    .mark_line()
    .encode(
        x="year:N",
        y="slope:Q",
        color=color,
        tooltip="title:N",
        opacity=alt.condition(selection, alt.value(0.8), alt.value(0.3)),
    )
)

legend = (
    alt.Chart(sorted_total)
    .mark_point()
    .encode(
        alt.Y("title:N").axis(orient="right"),
        color=color,
    )
    .add_params(selection)
)
scatter | legend
# %%
