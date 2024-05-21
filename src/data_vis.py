# %% Imports

import altair as alt
import polars as pl

# %%
# Set viewer

alt.renderers.enable("mimetype")


# %%
# Display supp values as individual entries

schema = {
    "id": pl.Int64,
    "year": pl.String,
    "amount": pl.Int64,
    "function": pl.String,
    "title": pl.String,
    "supp": pl.Boolean,
    "supp_vals": pl.Int64,
}

total = pl.read_csv(
    "../output_data/haushalts_daten/hh_total.csv", schema=schema, separator=";"
)

optimized_df = pl.DataFrame(
    {"year": [], "amount": [], "function": [], "title": [], "supp": []},
    schema={
        "year": pl.String,
        "amount": pl.Int64,
        "function": pl.String,
        "title": pl.String,
        "supp": pl.Boolean,
    },
)
for entry in total.iter_rows(named=True):
    new_entry = pl.DataFrame(
        {
            "year": [entry["year"]],
            "amount": [entry["amount"]],
            "function": [entry["function"]],
            "title": [entry["title"]],
            "supp": [False],
        }
    )
    if entry["supp"] is True:
        supp_vals = {
            "year": [entry["year"]],
            "amount": [entry["supp_vals"]],
            "function": [entry["function"]],
            "title": [entry["title"]],
            "supp": [True],
        }
        new_entry = pl.concat([new_entry, pl.DataFrame(supp_vals)])
    optimized_df = pl.concat([optimized_df, new_entry])

# %%
# Generate bar chart from combined data

selection = alt.selection_point(fields=["function"])

color = alt.condition(
    selection, alt.Color("function:N").legend(None), alt.value("lightgray")
)

scatter = (
    alt.Chart(optimized_df)
    .mark_bar()
    .encode(x="year:N", y="amount:Q", color=color, tooltip="title:N")
)

legend = (
    alt.Chart(optimized_df)
    .mark_point()
    .encode(alt.Y("title:N").axis(orient="right"), color=color)
    .add_params(selection)
)

scatter | legend

# %%
# Visualize supplementary budgets individually

supp_color = alt.Color("function:N").legend(None)
legend_color = alt.Color("function:N").legend(None)

scatter = (
    alt.Chart(optimized_df)
    .mark_bar()
    .encode(x="year:N", y="amount:Q", color=supp_color, tooltip="title:N")
).transform_filter(alt.FieldEqualPredicate(field="supp", equal=True))

legend = (
    alt.Chart(optimized_df)
    .mark_point()
    .encode(alt.Y("title:N").axis(orient="right"), color=legend_color)
)

scatter | legend

# %%
# Show integrated supp vals

supp_color = alt.condition(
    alt.FieldEqualPredicate(field="supp", equal=True),
    alt.Color("function:N").legend(None),
    alt.value("lightgray"),
)
legend_color = alt.Color("function:N").legend(None)

scatter = (
    alt.Chart(optimized_df)
    .mark_bar()
    .encode(x="year:N", y="amount:Q", color=supp_color, tooltip="title:N")
)

legend = (
    alt.Chart(optimized_df)
    .mark_point()
    .encode(alt.Y("title:N").axis(orient="right"), color=legend_color)
)

scatter | legend

# %%
# Get summed up table
new_total = total.clone()

for entry in new_total.iter_rows(named=True):
    if entry["supp"] is True:
        inclusive_val = entry["amount"] + entry["supp_vals"]
        new_total[entry["id"] - 1, "amount"] = inclusive_val

# %%
# Alternative chart with logarithmic scale

selection = alt.selection_point(fields=["function"])
color = alt.condition(
    selection, alt.Color("function:N").legend(None), alt.value("lightgray")
)

scatter = (
    alt.Chart(new_total)
    .mark_point()
    .encode(
        x="year:N",
        y=alt.Y("amount:Q").scale(type="log"),
        color=color,
        tooltip="title:N",
    )
)

legend = (
    alt.Chart(new_total)
    .mark_point()
    .encode(alt.Y("title:N").axis(orient="right"), color=color)
    .add_params(selection)
)

scatter | legend
# %%
# Calculate slope

slope_series = []
sorted_total = new_total.sort("year")
sorted_total = sorted_total.sort("function")

curr_func = None
old_amount = None
for entry in sorted_total.iter_rows(named=True):
    if curr_func == entry["function"]:
        slope_series.append(entry["amount"] / old_amount)
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
