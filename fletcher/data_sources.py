#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 22:29:18 2026

@author: joshuaweston
"""

from bokeh.models import ColumnDataSource, HTMLTemplateFormatter, Span
from bokeh.io import curdoc

import pandas as pd

full_data_source = ColumnDataSource(data=dict())
tp_source = ColumnDataSource(data=dict(SNID=[]))
fp_source = ColumnDataSource(data=dict(SNID=[]))
fn_source = ColumnDataSource(data=dict(SNID=[]))
tn_source = ColumnDataSource(data=dict(SNID=[]))
source_hist = ColumnDataSource(data=dict(left=[], right=[], success=[], fail=[]))
threshold_line = Span(location=0.5, dimension="height",
                      line_color="black", line_dash="dashed")
curve_source = ColumnDataSource(data=dict(fpr=[], fnr=[]))
marker_source = ColumnDataSource(data=dict(fpr=[0], fnr=[0]))
row_detail_source = ColumnDataSource(data=dict())
cell_formatter = HTMLTemplateFormatter(
    template="<div style='background:#ffe6e1;text-align:center;padding:2px;'><%= value %></div>"
)



