#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 22:18:35 2026

@author: joshuaweston
"""
from PIL import Image

LOGO_PATH = "fletch/static/fletcher.png"
LOGO_WIDTH_PX = 200
TABLE_WIDTH_PX = 250
TABLE_HEIGHT_PX = 300
PLOT_WIDTH_PX = 400
PLOT_HEIGHT_PX = 250
HORIZONTAL_SPACE_PX = 20
ROW_SPACING_PX = 5
ONE_ROW_HEIGHT = 30
HEADER_HEIGHT = 25
DETAIL_WIDTH_PX = TABLE_WIDTH_PX * 2
DETAIL_HEIGHT_PX = TABLE_WIDTH_PX * 2
FIXED_IMAGE_WIDTH = DETAIL_WIDTH_PX
FIXED_IMAGE_HEIGHT = DETAIL_HEIGHT_PX

img = Image.open('static/fletcher.png')
orig_w, orig_h = img.size
LOGO_HEIGHT_PX = int(orig_h * (LOGO_WIDTH_PX / orig_w))
