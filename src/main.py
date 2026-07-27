import wfdb
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.ticker import scale_range
from matplotlib.widgets import Slider
from wfdb.io import record

range_slider : Slider = None
dist_slider : Slider = None
view_range = 0
dist = 0
fig : plt.subplot = None
record : record = None

def main():
    global record
    record = open_record("C:/Users/zach/Downloads/EEG1_8")
    plot_record(record)

def open_record(filename):
    record = wfdb.rdrecord(filename)
    #print(type(record))
    return record

def record_to_array(record):
    expandedSignal : np.ndarray = record.p_signal
    #print(str(expandedSignal.size) + "\n" + str(expandedSignal))
    return expandedSignal

def plot_record(record):
    global range_slider, dist_slider, fig, view_range, dist
    figure : plt.figure = wfdb.plot_wfdb(record=record, title='WFDB', return_fig=True, )

    fig, ax = plt.subplots()
    fig = figure
    fig.subplots_adjust(bottom=0.40, left=0.20)

    #ax.ticklabel_format(style='plain', axis='y', useOffset=False)
    #ax.plot(ax, record.p_signal * 100)

    ax_range = fig.add_axes((0.25, 0.1, 0.65, 0.03))
    ax_dist = fig.add_axes((0.25, 0.15, 0.65, 0.03))

    view_range = record.sig_len
    dist = record.sig_len/2
    range_slider = Slider(ax_range, "range",0, record.sig_len, valinit=record.sig_len, valstep=1)
    dist_slider = Slider(ax_dist, "position",0, record.sig_len, valinit=record.sig_len/2, valstep=1)

    range_slider.on_changed(sld_update)
    dist_slider.on_changed(sld_update)
    plt.show()

def sld_update(val):
    global view_range, dist, range_slider, dist_slider, fig, record
    view_range = range_slider.val
    dist = dist_slider.val
    record = trim_record(record, view_range, dist)
    fig.canvas.draw_idle()

def trim_record(record,view_range,view_position):
    #convert time to sample number
    start_sample = int(view_position - view_range/2)
    end_sample = int(view_position + view_range/2)

    #print(start_sample, end_sample)
    expandedSignal : np.ndarray = record_to_array(record)
    record.p_signal = expandedSignal[start_sample:end_sample]
    #print(record.p_signal)
    return record

main()