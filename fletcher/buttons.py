#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 22:37:13 2026

@author: joshuaweston
"""

from bokeh.models import (
    Div, Button, FileInput, CustomJS
)
from bokeh.layouts import column, row
from bokeh.io import curdoc

from data_sources import *
from config import *
from plots import *

import pandas as pd
from io import StringIO
import base64



file_input = FileInput(accept=".csv", width=100)

load_button = Button(label="Load CSV", width=100)
save_button = Button(label="Save CSV", width=100, button_type="success")
help_button = Button(label="Help", width=100, button_type="primary")

# JS to trigger file input
load_button.js_on_click(CustomJS(code="""
document.querySelector('input[type=file]').click();
"""))

def file_input_callback(attr, old, new):
    df = pd.read_csv(StringIO(base64.b64decode(new).decode()))
    extra_cols = [c for c in df.columns if c not in {"SNID","target","y_prob"}][:6]
    curdoc().columns_first_table = extra_cols
    df["Raw target"] = df["target"]
    if "Notes" not in df.columns:
        df["Notes"] = [""]*len(df)
    full_data_source.data = df.to_dict("list")
    update_histogram_and_metrics()

file_input.on_change("value", file_input_callback)
file_input.css_classes.append("hidden-file-input")

# JS to open help link
help_button.js_on_click(CustomJS(code="""
window.open("https://github.com/joshgithubbin/Sherlock-DDF/wiki", "_blank");
"""))

save_button.js_on_click(CustomJS(args=dict(source=full_data_source), code="""
const data = source.data;
const columns = Object.keys(data);
const raw_index = columns.indexOf("Raw target");
if(raw_index >= 0){columns.push(columns.splice(raw_index,1)[0]);}
const nrows = data[columns[0]].length;
let csv = columns.join(",") + "\\n";
for(let i=0;i<nrows;i++){
    let row=[];
    for(let j=0;j<columns.length;j++){
        let val = data[columns[j]][i];
        if(typeof val==="string" && val.includes(",")){val='"'+val.replace(/"/g,'""')+'"';}
        row.push(val);
    }
    csv += row.join(",") + "\\n";
}
const blob = new Blob([csv],{type:"text/csv;charset=utf-8;"});
const url = URL.createObjectURL(blob);
const a = document.createElement("a");
a.href = url;
a.download = "fletch_data.csv";
a.click();
URL.revokeObjectURL(url);
"""))

logo_div = Div(
    text=f'<img src="{LOGO_PATH}" width="{LOGO_WIDTH_PX}" style="display:block;">',
    width=LOGO_WIDTH_PX,
    height=LOGO_HEIGHT_PX
)

for b in (load_button, save_button, help_button):
    b.css_classes.append("match-logo-height")

button_wrapper = row(load_button, save_button, help_button, height=LOGO_HEIGHT_PX)

logos_row = row(logo_div, Div(width=HORIZONTAL_SPACE_PX), button_wrapper)