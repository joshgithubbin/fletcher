#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 23:12:47 2026

@author: joshuaweston
"""

from data_sources import *
from config import *
from bokeh.models import DataTable, TableColumn
from bokeh.layouts import column, row



def make_table(source, title):
    return DataTable(source=source, columns=[TableColumn(field="SNID", title=title, formatter=cell_formatter)],
                     width=TABLE_WIDTH_PX, height=TABLE_HEIGHT_PX)

tp_table = make_table(tp_source, "True Positives")
fp_table = make_table(fp_source, "False Positives")
fn_table = make_table(fn_source, "False Negatives")
tn_table = make_table(tn_source, "True Negatives")

tables_left = column(row(tp_table, fp_table), row(fn_table, tn_table), spacing=ROW_SPACING_PX)