# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:25:52 2020

@author: Magnolia
"""

import os
import glob
import numpy as np
import pandas as pd
# from datetime import datetime
# import dateutil.parser as date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import matplotlib.dates as mdates

class paths:
    def __init__(self, machine):
        if machine == 'iThink':
            p = r'C:\Users\meroo'
        if machine == 'Magnolia':
            p = r'C:\Users\Magnolia'
        self.pan = p + r'\OneDrive - UMBC\Research\Data\Pandora\Pandonia\Use'
        self.air = p + r'\OneDrive - UMBC\Research\Data\AirNow\USE'
        self.fig = p + r'\OneDrive - UMBC\Research\Figures\Preliminary'
        self.sav = p + r'\OneDrive - UMBC\Research\Data\Processed'
        self.current = os.getcwd()

class pandonia:
    def flt_by_date(df, date1, date2):
        if df.dropna().empty: print('Input dataframe is empty'); return
        mask = (df[0] >= date1) & (df[0] <= date2)
        uL = df.loc[mask]
        if uL.dropna().empty: print('Specified dates are not found \n',
                                    f'Dataframe only provides {df[0].iloc[0]} to {df[0].iloc[-1]}'); return
        return uL

    def flt(df, column, val_1, val_2):
        if df.dropna().empty: print('Input dataframe is empty'); return
        mask = (df[column] >= val_1) & (df[column] <= val_2)
        uL = df.loc[mask]
        if uL.dropna().empty: print('Specified dates are not found \n'); return
        return uL

    def plot(dataframe, flt='on', title=None, savpath=None):
        ### Description ###
        # dataframe -> enter pandas data frame
        # start     -> enter starting date (or datetime) as string
        # stop      -> ente stoping date (or datetime) as string
        # fig

        ### Output => dateframe with
        uL = dataframe
        uL[7].replace(-999, np.nan)

        if flt == 'on':
            uL.loc[uL[11] >= 12, [7, 8, 3, 4]] = np.nan
            uL.loc[uL[22] >= 1, [7, 8, 3, 4]] = np.nan

        if not title:
            uL1 = uL[0].iloc[0].strftime('%Y%m%dT%H%M')
            uL2 = uL[0].iloc[-1].strftime('%Y%m%dT%H%M')
            title=f'{uL1}_{uL2}'

        fig, (ax1, ax3) = plt.subplots(2, 1)
        color = 'blue'
        ax1.plot(uL[0], uL[8], '.', markersize=1, color='b')
        ax1.set_title(f"{title}")
        ax1.set_ylabel('Uncertainty (DU)', color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()

        color = 'red'
        ax2.plot(uL[0], uL[7], '.', markersize=1, color=color, label='Data')
        ax2.set_ylabel('Total Column (DU)', color=color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("(%Hh)"))
        ax2.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        color = 'tab:blue'
        ax3.plot(uL[0], uL[3],'.', markersize=1, color=color)
        ax3.set_xlabel('Datetime UTC')
        ax3.set_ylabel('SZA (degrees)', color=color)
        ax3.tick_params(axis='y', labelcolor=color)

        ax4 = ax3.twinx()

        color = 'green'
        ax4.plot(uL[0], uL[4],'.', markersize=1, color=color)
        ax4.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax4.set_ylabel('SAA (degrees)', color=color)
        ax4.tick_params(axis='y', labelcolor=color)
        ax3.grid(True)
        if savpath: fig.savefig(f"{savpath}\QuickPlot_{title}.png", dpi=600)
        if not savpath: fig.savefig(f"QuickPlot_{title}.png", dpi=600)
        plt.show()
        return uL

    def plot_by_date(dataframe, start, stop, flt='off', title=None):
        ### Description ###
        # dataframe -> enter pandas data frame
        # start     -> enter starting date (or datetime) as string
        # stop      -> ente stoping date (or datetime) as string
        # fig

        ### Output => dateframe with

        uL = pandonia.flt_by_date(dataframe, start, stop); uL = uL.reset_index()

        uL[7].replace(-999, np.nan)

        if flt == 'on':
            uL.loc[uL[11] >= 12, [7, 8, 3, 4]] = np.nan
            uL.loc[uL[22] >= 1, [7, 8, 3, 4]] = np.nan

        pandonia.plot(uL, title)
        return uL

    def importing(Path, par=None, date_start=None, date_stop=None):
        uL = {}
        uL_head = {}
        print(f'Importing from {Path} \n')
        for filename in glob.glob(os.path.join(Path, '*.txt')):
            """Search for the given string in file and return lines containing that string,
            along with line numbers"""
            nlines = 0
            cells = []
            # Open the file in read only mode
            with open(filename, 'r') as f:
                for line in f:   # Read all lines in the file one by one
                    nlines += 1
                    if '---' in line:
                        cells.append(nlines-1)    # If yes, then add the line number
                f.close()
            with open(os.path.join(Path, filename), 'r') as f: # open in readonly mode
                uL_head["{} Head".format(filename.split('\\')[-1])] = pd.read_csv(f, sep="\n",
                                                                              header=None, nrows=cells[1], low_memory=False)
                f.close()
            with open(os.path.join(Path, filename), 'r') as f:
                uL[filename.split('\\')[-1]] = pd.read_csv(f, sep=" ", parse_dates=[0], header=None, skiprows=cells[1]+1, low_memory=False)
                print(filename.split('\\')[-1], '\t -> Loaded')
                f.close()
        name = list(uL.keys())
        if par != None:
            if 'filter_by_date' in par and date_start !=None:
                if date_start & date_stop:
                    for i in name:
                        uL[i] = pandonia.flt_by_date(uL[i], date_start, date_stop)
            if 'plot' in par:
                if 'filter_on' in par: flt='on'
                for i in name:
                    uL[i] = pandonia.plot(uL[i], flt=flt)

        return uL, uL_head, name

def string_in_txt(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))

    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results
