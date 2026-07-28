import datetime
from enum import auto

import wfdb
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.ticker import scale_range
from matplotlib.transforms import Bbox
from matplotlib.widgets import Slider, TextBox
from numpy.ma.bench import timer
from wfdb.io import record

range_sld : Slider = None
dist_sld : Slider = None
range_txt : TextBox = None
dist_txt : TextBox = None

parent_figure : plt.Figure = None;

def main():
    global parent_figure, dist_txt
    record : wfdb.Record = open_record("C:/Users/zach/Downloads/EEG1_8")
    record2 : wfdb.Record = open_record("../Fw_ Clinical Insights Manager Demo Export Data Examples/Resp_16")
    parent_figure, range_slider, dist_slider = init_figure(record)
    plot_record(record, parent_figure.subfigs[0])
    plot_record(record2, parent_figure.subfigs[0])
    plt.show()
    startTime = datetime.datetime.now()

def open_record(filename):
    record = wfdb.rdrecord(filename)
    #print(type(record))
    return record

'''
init_figure
takes: record - the record the sliders should have the length of
'''
def init_figure(record: wfdb.Record):
    global range_sld, dist_sld, range_txt, dist_txt
    #create figure and cut it in 2 in a  4:1 ratio
    parent_figure = plt.figure()
    subfigs = parent_figure.subfigures(2,1, hspace=0.05, height_ratios=[4,1])

    #add 2 slider axes to the bottom part
    sld_fig = subfigs[1]
    ax_range = sld_fig.add_axes((0.2, 0.2, 0.5, 0.5))
    ax_dist = sld_fig.add_axes((0.2, 0.5, 0.5, 0.5))
    ax_rangetext = sld_fig.add_axes((0.8, 0.2, 0.1, 0.25))
    ax_disttext = sld_fig.add_axes((0.8, 0.5, 0.1, 0.25))
    range_slider = Slider(ax_range, "range", 0, record.sig_len/record.fs, valinit=10, valstep=1)
    dist_slider = Slider(ax_dist, "position", 0, record.sig_len/record.fs, valinit=5, valstep=1)
    range_slider.on_changed(update_range_sld)
    dist_slider.on_changed(update_position_sld)

    #add 2 text inputs for slider values
    range_text = TextBox(ax_rangetext, "")
    dist_text = TextBox(ax_disttext, "")
    range_text.set_val(10)
    dist_text.set_val(5)
    range_text.on_submit(update_range_txt)
    dist_text.on_submit(update_position_txt)

    range_sld = range_slider
    dist_sld = dist_slider
    range_txt = range_text
    dist_txt = dist_text

    return parent_figure, range_slider, dist_slider

def update_range_sld(val):
    global parent_figure, range_txt, range_sld
    if(val == range_txt.text):
        return
    range_txt.set_val(val)
    parent_figure.canvas.draw_idle()

def update_position_sld(val):
    global parent_figure, dist_txt, dist_sld
    if(val == dist_txt.text):
        return
    dist_txt.set_val(val)
    parent_figure.canvas.draw_idle()

def update_range_txt(val):
    global parent_figure, range_sld, range_txt
    update_view()
    if(val == range_sld.val):
        return
    range_sld.set_val(float(val))
    parent_figure.canvas.draw_idle()

def update_position_txt(val):
    global parent_figure, dist_sld, dist_txt
    update_view()
    if(val == dist_sld.val):
        return
    dist_txt.set_val(float(val))
    parent_figure.canvas.draw_idle()

def update_view():
    global parent_figure, range_txt, dist_txt
    graph_fig = parent_figure.subfigs[0]
    axs = graph_fig.get_axes()
    dist = float(dist_txt.text)
    range = float(range_txt.text)/2
    for ax in axs:
        ax.set_xlim(dist-range, dist+range)

def plot_record(record : wfdb.Record, fig : plt.Figure):
    #recordfig : plt.Figure = wfdb.plot_wfdb(record=record, title='WFDB', return_fig=True, figsize=(10,10))
    #ax1 = recordfig.get_axes()

    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    t = np.arange(0, record.sig_len/record.fs, 1.0 / record.fs)
    s = record.p_signal[: , 0 ]
    ax.plot(t, s*1000)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("(uv)")
    #ax.set_yticks(t)
    ax.grid(True, which="both", axis="both", )
    ax.set_xlim(0, record.fs/12)
    ax.set_ylim(-100, 200)
    ax.set_aspect('auto', anchor="N", adjustable=None)

    #set position based on number of graphs
    pos = ax.get_position()
    height = (len(fig.get_axes())-1)/5

    ax.set_position([pos.x0, pos.y0 + height, pos.width, pos.height/6])

    #fig.subplots_adjust(bottom=0.40, left=0.20)

    print(len(fig.get_axes()))


    #print(recordfig.get_axes()[0])
    #ax = recordfig.get_axes()[0]

    #ax.ticklabel_format(style='plain', axis='y', useOffset=False)
    #ax.plot(ax, record.p_signal * 100)
    #ax.set_xlim(20,180)
    #plt.show()


main()