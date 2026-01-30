#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 22:16:29 2026

@author: joshuaweston
"""

from bokeh.models import Div

from config import LOGO_HEIGHT_PX

css_div = Div(text=f"""
<style>
html, body {{
    margin: 0 !important;
    padding: 0 !important;
}}
.bk-root {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}
.bk {{
    margin-top: -2px !important;
}}
.hidden-file-input {{
    display: none !important;
}}
.match-logo-height .bk-btn {{
    height: {LOGO_HEIGHT_PX}px !important;
    line-height: {LOGO_HEIGHT_PX}px !important;
    padding: 0px !important;
    background-color: #C00000 !important;
    color: white !important;
}}
.bk-data-table .slick-header-column {{
    background-color: #C00000 !important;
    color: white !important;
    font-weight: bold !important;
    text-align: center !important;
}}
</style>
""")