# Databricks notebook source
# MAGIC %pip install Jinja2==3.0.3 fastapi uvicorn nest_asyncio databricks-cli gradio==3.19.1

# COMMAND ----------

from __future__ import annotations

from math import sqrt

import altair
import gradio as gr
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd

from sdk.mount import DatabricksApp
dbx_app = DatabricksApp(8098)

# COMMAND ----------

def outbreak(plot_type, r, month, countries, social_distancing):
    months = ["January", "February", "March", "April", "May"]
    m = months.index(month)
    start_day = 30 * m
    final_day = 30 * (m + 1)
    x = np.arange(start_day, final_day + 1)
    pop_count = {"USA": 350, "Canada": 40, "Mexico": 300, "UK": 120}
    if social_distancing:
        r = sqrt(r)
    df = pd.DataFrame({"day": x})
    for country in countries:
        df[country] = x ** (r) * (pop_count[country] + 1)

    if plot_type == "Matplotlib":
        fig = plt.figure()
        plt.plot(df["day"], df[countries].to_numpy())
        plt.title("Outbreak in " + month)
        plt.ylabel("Cases")
        plt.xlabel("Days since Day 0")
        plt.legend(countries)
        return fig
    elif plot_type == "Plotly":
        fig = px.line(df, x="day", y=countries)
        fig.update_layout(
            title="Outbreak in " + month,
            xaxis_title="Cases",
            yaxis_title="Days Since Day 0",
        )
        return fig
    elif plot_type == "Altair":
        df = df.melt(id_vars="day").rename(columns={"variable": "country"})
        fig = altair.Chart(df).mark_line().encode(x="day", y='value', color='country')
        return fig
    else:
        raise ValueError("A plot type must be selected")


inputs = [
    gr.Dropdown(["Matplotlib", "Plotly", "Altair"], label="Plot Type"),
    gr.Slider(1, 4, 3.2, label="R"),
    gr.Dropdown(["January", "February", "March", "April", "May"], label="Month"),
    gr.CheckboxGroup(
        ["USA", "Canada", "Mexico", "UK"], label="Countries", value=["USA", "Canada"]
    ),
    gr.Checkbox(label="Social Distancing?"),
]
outputs = gr.Plot()

demo = gr.Interface(
    fn=outbreak,
    inputs=inputs,
    outputs=outputs,
    examples=[
        ["Matplotlib", 2, "March", ["Mexico", "UK"], True],
        ["Altair", 2, "March", ["Mexico", "Canada"], True],
        ["Plotly", 3.6, "February", ["Canada", "Mexico", "UK"], False],
    ],
    cache_examples=False,
    allow_flagging="never"
)


# COMMAND ----------

dbx_app.mount_gradio_app(gr.routes.App.create_app(demo))

# COMMAND ----------

import nest_asyncio
nest_asyncio.apply()
dbx_app.run()

# COMMAND ----------


