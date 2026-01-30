#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 23:07:58 2026

@author: joshuaweston
"""

from config import *
from data_sources import *
from buttons import *
from plots import *

from bokeh.models import (
    Div, Button,
    DataTable, TableColumn,
    TextInput
)

from bokeh.layouts import column, row
from bokeh.io import curdoc

# ==================== ROW DETAIL ======================
row_detail_table = DataTable(source=row_detail_source,
                             columns=[TableColumn(field="Placeholder", title="", formatter=cell_formatter)],
                             width=DETAIL_WIDTH_PX, height=ONE_ROW_HEIGHT + HEADER_HEIGHT,
                             row_height=ONE_ROW_HEIGHT, index_position=None)

row_detail_title = Div(width=DETAIL_WIDTH_PX,
                       style={"text-align": "center", "font-weight": "bold", "margin-bottom": "2px"})

image_div = Div(width=FIXED_IMAGE_WIDTH, height=FIXED_IMAGE_HEIGHT)

toggle_btn = Button(label="UNKNOWN", button_type="default", width=int(FIXED_IMAGE_WIDTH/4))
add_note_btn = Button(label="ADD TAG", button_type="primary", width=int(FIXED_IMAGE_WIDTH/4))
note_input = TextInput(value="", placeholder="Add Tag Here...", width=int(FIXED_IMAGE_WIDTH/2))

def add_note():
    idx = getattr(curdoc(), "current_row_idx", None)
    if idx is None:
        return
    note_text = note_input.value.strip()
    if not note_text:
        return
    data = dict(full_data_source.data)
    if "Notes" not in data:
        data["Notes"] = [""] * len(data["SNID"])
    current_note = data["Notes"][idx]
    data["Notes"][idx] = f"{current_note}; {note_text}" if current_note else note_text
    full_data_source.data = data
    note_input.value = ""

add_note_btn.on_click(add_note)
note_row = row(toggle_btn, add_note_btn, note_input, spacing=5)
row_detail_container = column(row_detail_title, row_detail_table, image_div, note_row, spacing=ROW_SPACING_PX)

# ==================== UPDATE FUNCTIONS ======================
def update_row_detail(idx):
    data = full_data_source.data
    snid = list(data["SNID"])[idx]
    target_val = list(data["target"])[idx]

    if target_val == 1:
        toggle_btn.label = "POSITIVE"
        toggle_btn.button_type = "success"
        row_detail_title.text = f"SNID: {snid} (POSITIVE)"
    else:
        toggle_btn.label = "NEGATIVE"
        toggle_btn.button_type = "danger"
        row_detail_title.text = f"SNID: {snid} (NEGATIVE)"

    extra_cols = getattr(curdoc(), "columns_first_table", [])
    if not extra_cols:
        row_detail_source.data = {"Placeholder": [""]}
        row_detail_table.columns = [TableColumn(field="Placeholder", title="", formatter=cell_formatter)]
    else:
        row_detail_source.data = {c: [data[c][idx]] for c in extra_cols}
        row_detail_table.columns = [TableColumn(field=c, title=c, formatter=cell_formatter) for c in extra_cols]

    image_div.text = f'<img src="fletch/static/im/{snid}.png" style="width:100%; height:100%; object-fit:contain;">'


def toggle_target():
    idx = getattr(curdoc(), "current_row_idx", None)
    if idx is None:
        return
    data = dict(full_data_source.data)
    data["target"][idx] = 1 - data["target"][idx]
    full_data_source.data = data
    update_row_detail(idx)
    update_histogram_and_metrics()

toggle_btn.on_click(toggle_target)

# ==================== ROW CALLBACK ===================
def make_row_callback(source):
    def cb(attr, old, new):
        if not new: return
        idx = new[0]
        snid = source.data["SNID"][idx]
        all_snids = list(full_data_source.data["SNID"])
        curdoc().current_row_idx = all_snids.index(snid)
        update_row_detail(curdoc().current_row_idx)
        source.selected.indices = []
    return cb

for s in (tp_source, fp_source, fn_source, tn_source):
    s.selected.on_change("indices", make_row_callback(s))
