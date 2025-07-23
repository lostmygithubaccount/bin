#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "==3.13"
# dependencies = [
#     "ibis-framework[duckdb,sqlite]",
#     "ipython",
#     "pandas",
#     "plotly",
#     "polars",
#     "rich",
#     "typer",
# ]
#
# ///

# imports
import os
from importlib import reload  # noqa

import ibis
import IPython
from rich import console

# Ibis configuration
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 40
ibis.options.repr.interactive.max_columns = None

# rich configuration
console = console.Console()
print = console.print

# path configuration
lakedir = os.getenv("LAKE", os.path.join(os.path.expanduser("~"), "lake"))
metadata_db = os.path.join(lakedir, "metadata.sqlite")
data_dir = os.path.join(lakedir, "data")
os.makedirs(data_dir, exist_ok=True)

# print banner
banner = """
▓█████▄ ▓█████ ██▒   █▓
▒██▀ ██▌▓█   ▀▓██░   █▒
░██   █▌▒███   ▓██  █▒░
░▓█▄   ▌▒▓█  ▄  ▒██ █░░
░▒████▓ ░▒████▒  ▒▀█░  
 ▒▒▓  ▒ ░░ ▒░ ░  ░ ▐░  
 ░ ▒  ▒  ░ ░  ░  ░ ░░  
 ░ ░  ░    ░       ░░  
   ░       ░  ░     ░  
 ░                 ░
 """.strip()
console.print(banner, style="bold purple")

# create Ibis connections
metacon = ibis.sqlite.connect(metadata_db)
con = ibis.duckdb.connect()
init_sql = f"""
install ducklake;
install sqlite;

create secret (
    type ducklake,
    metadata_path 'sqlite:{metadata_db}',
    data_path '{data_dir}'
);

attach 'sqlite:{metadata_db}' as metadata;
attach 'ducklake:' as data;

use data;
""".strip()
con.raw_sql(init_sql)
ibis.set_backend(con)

# create IPython shell
IPython.embed(
    banner1="",
    banner2="",
    display_banner=False,
    exit_msg="",
    colors="linux",
    theming="monokai",
)
