#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row


from css import css_div

from config import *
from data_sources import *
from buttons import *
from detail import *
from plots import *
from tables import *



left_panel = column(slider, metrics_div, hist_plot, fnr_plot_with_button)
layout = column(css_div, logos_row, file_input, 
                row(left_panel, tables_left, row_detail_container, spacing=HORIZONTAL_SPACE_PX))


curdoc().add_root(layout)
curdoc().title = "Fletcher Dashboard"

slider.on_change("value", lambda attr, old, new: update_histogram_and_metrics())
