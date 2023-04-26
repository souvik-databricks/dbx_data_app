# Databricks notebook source
# MAGIC %pip install fastapi uvicorn nest_asyncio databricks-cli

# COMMAND ----------

from router_service import DatabricksApp
from typing import Union

from fastapi import FastAPI


dbx_app = DatabricksApp(8099)

# COMMAND ----------



app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# COMMAND ----------

dbx_app.mount_fastapi_app(app)

# COMMAND ----------

import nest_asyncio
nest_asyncio.apply()
dbx_app.run()

# COMMAND ----------
