# Databricks notebook source
# MAGIC %pip install Jinja2==3.0.3 fastapi uvicorn nest_asyncio databricks-cli shiny

# COMMAND ----------

# MAGIC %pip install typing-extensions --upgrade

# COMMAND ----------

from __future__ import annotations

from shiny import App, render, ui

from sdk.mount import DatabricksApp
dbx_app = DatabricksApp(8099)

# COMMAND ----------

app_ui = ui.page_fluid(
    ui.h2("Hello Shiny!"),
    ui.input_slider("n", "N", 0, 100, 20),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app = App(app_ui, server)

# COMMAND ----------

dbx_app.mount_gradio_app(app)

# COMMAND ----------

import nest_asyncio
nest_asyncio.apply()
dbx_app.run()

# COMMAND ----------


