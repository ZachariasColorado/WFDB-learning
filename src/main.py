import datetime
import re
from array import ArrayType
from enum import auto

import wfdb
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import rc_params
from matplotlib.ticker import scale_range, MultipleLocator
from matplotlib.transforms import Bbox
from matplotlib.widgets import Slider, TextBox
from numpy.ma.bench import timer
from wfdb.io import record

range_sld : Slider = None
dist_sld : Slider = None
range_txt : TextBox = None
dist_txt : TextBox = None
start_times = []
time_texts = []

parent_figure : plt.Figure = None;

def main():
    global parent_figure, dist_txt, records
    #load records and store them in global
    record, record_start = open_record("C:/Users/zach/Downloads/EEG1_8")
    record2, record2_start = open_record("../Fw_ Clinical Insights Manager Demo Export Data Examples/Resp_16")
    record3, record3_start = open_record("C:/Users/zach/Downloads/EEG1_8")

    #create UI and plot all records
    parent_figure, range_slider, dist_slider = init_figure(record)
    plot_record(record, parent_figure.subfigs[0], record_start)
    plot_record(record2, parent_figure.subfigs[0], record2_start)
    plot_record(record3, parent_figure.subfigs[0], record3_start)
    plt.show()
    startTime = datetime.datetime.now()

def open_record(filename):
    global start_times
    #open with wfdb library to extract data
    record = wfdb.rdrecord(filename)
    #open with python to extract datetime
    headerfile = open(filename+".hea", "r")
    header = headerfile.read()
    pattern = r"\d+\/\d+\/\d+ \d+:\d+:\d+.\d+"
    matches = re.findall(pattern, header)
    print("potential match: " + matches[0])

    pattern = matches[0].split(" ")
    date_info = pattern[0].split("/")
    time_info = pattern[1].split(":")

    start_time = datetime.datetime(int(date_info[2]), int(date_info[0]), int(date_info[1]), int(time_info[0]),int(time_info[1]), int(time_info[2].split(".")[0]))
    print(start_time)
    start_times.append(start_time)

    #TODO use start time for x axis labeling

    #print(type(record))
    return record, start_time

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
    global parent_figure, range_txt, dist_txt, start_times, time_texts
    graph_fig = parent_figure.subfigs[0]
    axs = graph_fig.get_axes()
    dist = float(dist_txt.text)
    range = float(range_txt.text)/2
    for ax in axs:
        time_offset = datetime.timedelta(seconds=(dist-range))
        ax.set_xlim(dist-range, dist+range)
        time_texts[axs.index(ax)].set_text(start_times[axs.index(ax)]+time_offset)
        #print()

def plot_record(record : wfdb.Record, fig : plt.Figure, start_time : datetime.datetime):
    #recordfig : plt.Figure = wfdb.plot_wfdb(record=record, title='WFDB', return_fig=True, figsize=(10,10))
    #ax1 = recordfig.get_axes()
    global time_texts

    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    t = np.arange(0, record.sig_len/record.fs, 1.0 / record.fs)
    s = record.p_signal[: , 0 ]
    ax.plot(t, s*1000)
    if(len(fig.get_axes()) == 1):
        ax.set_xlabel("Time (s)")
    ax.set_ylabel("(uv)")
    ax.grid(True, which="both", axis="both", )
    ax.set_xlim(0, record.fs/12)
    ax.set_ylim(-100, 200)
    ax.set_aspect('auto', anchor="N", adjustable=None)
    ax.set_title(record.record_name, fontsize = 7)

    ax.minorticks_on()
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(MultipleLocator(1.0/6.0))

    #set up grid
    gridx = np.arange(0, record.sig_len/record.fs, 1.0)
    ax.grid(True, which="major", axis="both", linestyle="-", linewidth=1.0)
    ax.grid(True, which="minor", axis="both", linestyle=":", linewidth=0.5)

    text = ax.text(0.05, 0.95, start_time, transform=ax.transAxes, fontsize=14,
            verticalalignment='top')

    time_texts.append(text)

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