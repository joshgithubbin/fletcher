#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 22:45:34 2026

@author: joshuaweston
"""

from config import *
from data_sources import *


import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row

from bokeh.models import Label, Button, Slider, Div


slider = Slider(start=0, end=1, value=0.5, step=0.01,
                title="Decision Threshold", width=PLOT_WIDTH_PX)
metrics_div = Div(width=PLOT_WIDTH_PX)

# ==================== HISTOGRAM ============================
hist_plot = figure(
    title="Model Score Distribution",
    x_axis_label="Model Score",
    y_axis_label="Frequency",
    y_axis_type="log",
    width=PLOT_WIDTH_PX,
    height=PLOT_HEIGHT_PX
)
hist_plot.quad(top="success", bottom=1e-1, left="left", right="right",
               source=source_hist, fill_color="green", fill_alpha=0.6, legend_label="Successful")
hist_plot.quad(top="fail", bottom=1e-1, left="left", right="right",
               source=source_hist, fill_color="red", fill_alpha=0.6, legend_label="Unsuccessful")
hist_plot.add_layout(threshold_line)
hist_plot.legend.location = "top_right"


# ==================== FNR VS FPR ============================

fnr_fpr_plot = figure(
    title="False Negative Rate vs False Positive Rate",
    x_axis_label="False Positive Rate",
    y_axis_label="False Negative Rate",
    width=PLOT_WIDTH_PX,
    height=PLOT_HEIGHT_PX
)
fnr_fpr_plot.line("fpr", "fnr", source=curve_source, line_width=3, color="#16085c")
fnr_fpr_plot.circle("fpr", "fnr", source=marker_source, size=10, color="#C00000")
auc_label = Label(x=0.95, y=0.05, x_units="data", y_units="data",
                  text="AUC: N/A", text_align="right",
                  text_font_style="bold", text_color="#16085c")
fnr_fpr_plot.add_layout(auc_label)


# ==================== TOGGLE AND UPDATES ============================

# Toggle plot button
toggle_plot_btn = Button(label="Toggle Plot", button_type="warning", width=int(FIXED_IMAGE_WIDTH/4))
curdoc().pr_plot_state = "FNR_FPR"

def update_curve_plot():
    df = pd.DataFrame(full_data_source.data)
    if df.empty:
        auc_label.visible = False
        marker_source.data = dict(fpr=[0], fnr=[0])
        return

    y_true = df["target"].values
    y_prob = df["y_prob"].values
    thresholds = np.linspace(0, 1, 200)

    fpr_vals, fnr_vals = [], []
    precision_vals, recall_vals = [], []

    for t in thresholds:
        y_pred = (y_prob >= t).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        fn = np.sum((y_pred == 0) & (y_true == 1))
        tn = np.sum((y_pred == 0) & (y_true == 0))

        fpr_vals.append(fp / max(1, fp + tn))
        fnr_vals.append(fn / max(1, fn + tp))
        precision_vals.append(tp / max(1, tp + fp))
        recall_vals.append(tp / max(1, tp + fn))

    t = slider.value
    y_pred_t = (y_prob >= t).astype(int)

    tp_total = np.sum(y_true == 1)
    tn_total = np.sum(y_true == 0)

    if curdoc().pr_plot_state == "FNR_FPR":
        # Show AUC
        auc_label.visible = True
        fnr_fpr_plot.title.text = "False Negative Rate vs False Positive Rate"
        fnr_fpr_plot.xaxis.axis_label = "False Positive Rate"
        fnr_fpr_plot.yaxis.axis_label = "False Negative Rate"
        curve_source.data = dict(fpr=fpr_vals, fnr=fnr_vals)

        # Marker on FNR/FPR curve
        marker_source.data = dict(
            fpr=[np.sum((y_pred_t == 1) & (y_true == 0)) / max(1, tn_total)],
            fnr=[np.sum((y_pred_t == 0) & (y_true == 1)) / max(1, tp_total)]
        )

        # Compute AUC
        tpr_vals = [1 - fnr for fnr in fnr_vals]
        fpr_sorted, tpr_sorted = zip(*sorted(zip(fpr_vals, tpr_vals)))
        auc_value = sum((fpr_sorted[i] - fpr_sorted[i-1]) * 0.5 * (tpr_sorted[i] + tpr_sorted[i-1])
                        for i in range(1, len(fpr_sorted)))
        auc_label.text = f"AUC: {auc_value:.3f}"

    else:  # Precision vs Recall
        # Hide AUC
        auc_label.visible = False
        fnr_fpr_plot.title.text = "Precision vs Recall"
        fnr_fpr_plot.xaxis.axis_label = "Recall"
        fnr_fpr_plot.yaxis.axis_label = "Precision"
        curve_source.data = dict(fpr=recall_vals, fnr=precision_vals)

        # Marker on Precision-Recall curve
        tp = np.sum((y_pred_t == 1) & (y_true == 1))
        fp = np.sum((y_pred_t == 1) & (y_true == 0))
        fn = np.sum((y_pred_t == 0) & (y_true == 1))
        precision_t = tp / max(1, tp + fp)
        recall_t = tp / max(1, tp + fn)
        marker_source.data = dict(fpr=[recall_t], fnr=[precision_t])
        

def update_histogram_and_metrics():
    df = pd.DataFrame(full_data_source.data)
    if df.empty:
        return

    y_true = df["target"].values
    y_prob = df["y_prob"].values
    t = slider.value
    y_pred = (y_prob >= t).astype(int)

    # Histogram
    bins = np.linspace(0, 1, 30)
    h1, edges = np.histogram(y_prob[y_true == 1], bins=bins)
    h0, _ = np.histogram(y_prob[y_true == 0], bins=bins)
    source_hist.data = dict(left=edges[:-1], right=edges[1:], success=h1, fail=h0)

    # Metrics
    tp = np.sum((y_pred == 1) & (y_true == 1))
    fp = np.sum((y_pred == 1) & (y_true == 0))
    fn = np.sum((y_pred == 0) & (y_true == 1))
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    metrics_div.text = (
        f"<b>Threshold:</b> {t:.2f} | "
        f"<b>FPR:</b> {(y_pred[y_true == 0].mean() * 100):.2f}% | "
        f"<b>MDR:</b> {((1 - y_pred[y_true == 1]).mean() * 100):.2f}% | "
        f"<b>F1:</b> {f1:.3f}"
    )

    # Update TP/FP/FN/TN tables
    tp_source.data = dict(SNID=df[(y_pred == 1) & (df["target"] == 1)]["SNID"].tolist())
    fp_source.data = dict(SNID=df[(y_pred == 1) & (df["target"] == 0)]["SNID"].tolist())
    fn_source.data = dict(SNID=df[(y_pred == 0) & (df["target"] == 1)]["SNID"].tolist())
    tn_source.data = dict(SNID=df[(y_pred == 0) & (df["target"] == 0)]["SNID"].tolist())

    # ===================== UPDATE THRESHOLD LINE & MARKER =====================
    threshold_line.location = t  # move the vertical dashed line on the histogram

    # Update marker on FNR/FPR or Precision-Recall curve
    tp_total = np.sum(y_true == 1)
    tn_total = np.sum(y_true == 0)
    marker_source.data = dict(
        fpr=[np.sum((y_pred == 1) & (y_true == 0)) / max(1, tn_total)],
        fnr=[np.sum((y_pred == 0) & (y_true == 1)) / max(1, tp_total)]
    )

    update_curve_plot()  # also redraw curve and AUC
    
    
toggle_plot_btn.on_click(lambda: (
    setattr(curdoc(), "pr_plot_state", 
            "PRECISION_RECALL" if curdoc().pr_plot_state == "FNR_FPR" else "FNR_FPR"),
    update_curve_plot()
))

fnr_plot_with_button = column(fnr_fpr_plot, toggle_plot_btn, spacing=5)

