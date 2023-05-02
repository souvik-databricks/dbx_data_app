# Databricks notebook source
# MAGIC %pip uninstall -y streamlit
# MAGIC %pip install -U streamlit Jinja2==3.0.3 fastapi uvicorn nest_asyncio

# COMMAND ----------

import streamlit
from pathlib import Path
import subprocess


# Putting it here to be transparent its how our jetty proxy accepts websocket connections
# this websocket limitation only has 64kb worth of data over wire really big limitaton
#  If a websocket is closed because a too large message was sent (currently set to default 64 KB for binary and 20 MB for text), we log the message size extracted from the error message and mark it as a failure. Because we have no way to determine what type of message was originally sent, we record it as a new metric. Note that both pairs of connections close, so for one failure, one metric will be logged as source and one as target.
# it sporadically restarts client connection (this is the streamlit behavior due to connection closing from the proxy)
def streamlit_patch_websockets_v2():
  p = Path(streamlit.__file__)
  _dir = (p.parent)
  process = subprocess.run(f"find {_dir} -type f -exec sed -i -e 's/\"stream\"/\"ws\"/g' {{}} \;", capture_output=True, shell=True)
  return process.stdout.decode()
streamlit_patch_websockets_v2()

# COMMAND ----------

from sdk.mount import DatabricksApp
dbx_app = DatabricksApp(8090)

# COMMAND ----------

import os
# streamlit code is in the streamlit_script.py
dbx_app.mount_streamlit_app(script_path=os.getcwd()+"/streamlit_script.py")

# COMMAND ----------

dbx_app.run()

# COMMAND ----------


