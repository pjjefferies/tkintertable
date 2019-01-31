# -*- coding: utf-8 -*-
"""
    Module for basic plotting inside the TableCanvas. Uses matplotlib.
    Created August 2008
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

# import sys
# import os
import math
import copy
import tkinter as tk
# import numpy as np
import matplotlib
# from matplotlib.font_manager import FontProperties
import pylab
matplotlib.use('TkAgg')


class pylabPlotter(object):
    """An interface to matplotlib for general plotting and stats,
    using tk backend"""

    colors = ['#0049B4', '#C90B11', '#437C17', '#AFC7C7', '#E9AB17', '#7F525D',
              '#F6358A', '#52D017', '#FFFC17', '#F76541', '#F62217']
    linestyles = ['-', '--']
    shapes = ['o', '-', '--', ':', '.', 'p', '^', '<', 's', '+', 'x', 'D',
              '1', '4', 'h']
    legend_positions = ['best', 'upper left', 'upper center', 'upper right',
                        'center left', 'center', 'center right',
                        'lower left', 'lower center', 'lower right']

    graphtypes = ['XY', 'hist', 'bar', 'pie']
    fonts = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']

    def __init__(self):
        # Setup variables
        self.shape = 'o'
        self.grid = 0
        self.xscale = 0
        self.yscale = 0
        self.showlegend = 0
        self.legendloc = 'best'
        self.legendlines = []
        self.legendnames = []
        self.graphtype = 'XY'
        self.datacolors = self.colors
        self.dpi = 300
        self.linewidth = 1.5
        self.font = 'sans-serif'
        self.fontsize = 12
        try:
            self.setupPlotVars()
        except (AttributeError, tk.TclError):
            print('no tk running')
        self.currdata = None
        # self.format = None  #data format
        self.plottitle = ''
        self.plotxlabel = ''
        self.plotylabel = ''
        self.plotprefswin = None
        self.format = None
        self.dataseriesvars = None

    def plotXY(self, x, y, title='', xlabel=None, ylabel=None, shape=None,
               clr=None, lw=1):
        """Do x-y plot of 2 lists"""
        if shape is None:
            shape = self.shape
        if clr is None:
            clr = 'b'
        if self.xscale == 1:
            if self.yscale == 1:
                line, = pylab.loglog(x, y, shape, color=clr, linewidth=lw)
            else:
                line, = pylab.semilogx(x, y, shape, color=clr, linewidth=lw)
        elif self.yscale == 1:
            line, = pylab.semilogy(x, y, shape, color=clr, linewidth=lw)
        else:
            line, = pylab.plot(x, y, shape, color=clr, linewidth=lw)
        return line

    def doHistogram(self, data, bins=10):
        """Do a pylab histogram of 1 or more lists"""
        if len(data) == 1:
            ydim = 1
        else:
            ydim = 2
        dim = int(math.ceil(len(data)/2.0))
        # i = 1
        # fig = pylab.figure()
        for i, r in enumerate(data, 1):
            if len(r) == 0:
                continue
            ax = pylab.subplot(ydim, dim, i)
            print(r)
            for j, _ in enumerate(r):
                r[j] = float(r[j])
            pylab.hist(r, bins=bins)
        return ax

    def doBarChart(self, x, y, clr):
        """Do a pylab bar chart"""
        # xloc = range(len(x))
        for i, _ in enumerate(x):
            x[i] = float(x[i])
            y[i] = float(y[i])
        plotfig = pylab.bar(x, y, color=clr, alpha=0.6)
        return plotfig

    def doPieChart(self, data):
        """Do a pylab bar chart"""
        if len(data) == 1:
            ydim = 1
        else:
            ydim = 2
        dim = int(math.ceil(len(data)/2.0))
        # i=1
        for i, r in enumerate(data, 1):
            if len(r) == 0:
                continue
            # fig = pylab.subplot(ydim, dim, i)
            pylab.subplot(ydim, dim, i)
            print(r)
            for j, _ in enumerate(r):
                r[j] = float(r[j])
            pylab.pie(r)
            # i=i+1
        return

    def setData(self, data):
        """Set the current plot data, useful for re-plotting without re-calling
           explicit functions from the parent"""
        self.currdata = data
        return

    def hasData(self):
        """Is there some plot data?"""
        return self.currdata is not None and len(self.currdata) > 0
        # if self.currdata is not None and len(self.currdata) > 0:
        #    return True
        # else:
        #    return False

    def setDataSeries(self, names=None, start=1):
        """Set the series names, for use in legend"""
        self.dataseriesvars = []
        for i in range(start, len(names)):
            s = tk.StringVar()
            s.set(names[i])
            self.dataseriesvars.append(s)
        # print self.dataseriesvars
        return

    def setFormat(self, a_format):
        """Set current data format of currdata"""
        self.format = a_format
        return

    def plotCurrent(self, data=None, graphtype='bar', show=True,
                    guiopts=False, title=None):
        """Re-do the plot with the current options and data"""
        if guiopts:
            self.applyOptions()
        if title is not None:
            self.setTitle(title)
        self.clear()
        currfig = pylab.figure(1)

        if data is None:
            try:
                data = self.currdata
            except AttributeError:
                print('no data to plot')
                return
        else:
            self.setData(data)

        seriesnames = []
        legendlines = []
        for d in self.dataseriesvars:
            seriesnames.append(d.get())

        self.graphtype = graphtype
        # do an X-Y plot, with the first list as X xals
        if self.graphtype == 'bar' or len(data) == 1:
            i = 0
            pdata = copy.deepcopy(data)
            if len(pdata) > 1:
                x = pdata[0]
                pdata.remove(x)
                for y in pdata:
                    if i >= len(self.colors):
                        i = 0
                    c = self.colors[i]
                    self.doBarChart(x, y, clr=c)
                    i += 1
            else:
                y = pdata[0]
                x = list(range(len(y)))
                self.doBarChart(x, y, clr='b')

        elif self.graphtype == 'XY':
            pdata = copy.deepcopy(data)
            x = pdata[0]
            pdata.remove(x)
            i = 0
            for y in pdata:
                if i >= len(self.colors):
                    i = 0
                c = self.colors[i]
                line = self.plotXY(x, y, clr=c, lw=self.linewidth)
                legendlines.append(line)
                i += 1

        elif self.graphtype == 'hist':
            self.doHistogram(data)
        elif self.graphtype == 'pie':
            self.doPieChart(data)

        pylab.title(self.plottitle)
        pylab.xlabel(self.plotxlabel)
        pylab.ylabel(self.plotylabel)
        # create legend data
        if self.showlegend == 1:
            print(legendlines)
            pylab.legend(legendlines, seriesnames, loc=self.legendloc)
        if self.grid == 1:
            pylab.grid(True)

        if show:
            self.show()
        return currfig

    def clear(self):
        """clear plot"""
        pylab.clf()
        self.legendlines = []
        self.legendnames = []
        return

    def show(self):
        """ Show """
        pylab.show()
        return

    def saveCurrent(self, filename=None):
        """ Save Current """
        # import tk.filedialog
        # import os
        filename = tk.filedialog.asksaveasfilename(parent=self.plotprefswin,
                                                   defaultextension='.png',
                                                   filetypes=[("Png file",
                                                               "*.png"),
                                                              ("All files",
                                                               "*.*")])
        if not filename:
            return
        fig = self.plotCurrent(show=False)
        fig.savefig(filename, dpi=self.dpi)
        return

    def setTitle(self, title=None):
        """ Set Title """
        self.plottitle = title

    def setxlabel(self, label=None):
        """ Set X Label """
        self.plotxlabel = label

    def setylabel(self, label=None):
        """ Set Y Label """
        self.plotylabel = label

    def setOptions(self, shape=None, grid=None, xscale=None, yscale=None,
                   showlegend=None, legendloc=None, linewidth=None,
                   graphtype=None, font=None, fontsize=None):
        """Set the options before plotting"""
        if shape is not None:
            self.shape = shape
        if grid is not None:
            self.grid = grid
        if xscale is not None:
            self.xscale = xscale
        if yscale is not None:
            self.yscale = yscale
        if showlegend is not None:
            self.showlegend = showlegend
        if legendloc is not None:
            self.legendloc = legendloc
        if linewidth is not None:
            self.linewidth = linewidth
        if graphtype is not None:
            self.graphtype = graphtype
        if font is not None:
            self.font = font
        if fontsize is not None:
            self.fontsize = fontsize
        pylab.rc("font", family=self.font, size=self.fontsize)

    def setupPlotVars(self):
        """Plot Vars """
        self.pltgrid = tk.IntVar()
        self.pltlegend = tk.IntVar()
        self.pltsymbol = tk.StringVar()
        self.pltsymbol.set(self.shape)
        self.legendlocvar = tk.StringVar()
        self.legendlocvar.set(self.legendloc)
        self.xscalevar = tk.IntVar()
        self.yscalevar = tk.IntVar()
        self.xscalevar.set(0)
        self.yscalevar.set(0)
        self.graphtypevar = tk.StringVar()
        self.graphtypevar.set(self.graphtype)
        self.linewidthvar = tk.DoubleVar()
        self.linewidthvar.set(self.linewidth)
        self.fontvar = tk.StringVar()
        self.fontvar.set(self.font)
        self.fontsizevar = tk.DoubleVar()
        self.fontsizevar.set(self.fontsize)
        # plot specific
        self.plottitlevar = tk.StringVar()
        self.plottitlevar.set('')
        self.plotxlabelvar = tk.StringVar()
        self.plotxlabelvar.set('')
        self.plotylabelvar = tk.StringVar()
        self.plotylabelvar.set('')
        self.dataseriesvars = []

    def applyOptions(self):
        """Apply the gui option vars to the plotter options"""
        self.setOptions(shape=self.pltsymbol.get(), grid=self.pltgrid.get(),
                        xscale=self.xscalevar.get(),
                        yscale=self.yscalevar.get(),
                        showlegend=self.pltlegend.get(),
                        legendloc=self.legendlocvar.get(),
                        linewidth=self.linewidthvar.get(),
                        graphtype=self.graphtypevar.get(),
                        font=self.fontvar.get(),
                        fontsize=self.fontsizevar.get())
        self.setTitle(self.plottitlevar.get())
        self.setxlabel(self.plotxlabelvar.get())
        self.setylabel(self.plotylabelvar.get())

    def plotSetup(self, data=None):
        """Plot options dialog"""

        if data is not None:
            self.setData(data)
        self.plotprefswin = tk.Toplevel()
        self.plotprefswin.geometry('+300+450')
        self.plotprefswin.title('Plot Preferences')
        row = 0
        frame1 = tk.LabelFrame(self.plotprefswin, text='General')
        frame1.grid(row=row, column=0, sticky='news', padx=2, pady=2)

        def close_prefsdialog():
            """ Close Prefs Dialog """
            self.plotprefswin.destroy()

        def choosecolor(x):
            """Choose color for data series"""
            d = x[0]
            c = x[1]
            print('passed', 'd', d, 'c', c)
            import tkinter.colorchooser as tk_colorchooser
            colour, colour_string = (
                tk_colorchooser.askcolor(c, parent=self.plotprefswin))
            if colour is not None:
                self.datacolors[d] = str(colour_string)
                cbuttons[d].configure(bg=colour_string)
            return

        tk.Checkbutton(frame1, text="Grid lines", variable=self.pltgrid,
                       onvalue=1, offvalue=0).grid(row=0, column=0,
                                                   columnspan=2, sticky='news')
        tk.Checkbutton(frame1, text="Legend", variable=self.pltlegend,
                       onvalue=1, offvalue=0).grid(row=1, column=0,
                                                   columnspan=2, sticky='news')

        tk.Label(frame1, text='Symbol:').grid(row=2, column=0, padx=2, pady=2)
        symbolbutton = tk.Menubutton(frame1, textvariable=self.pltsymbol,
                                     relief='groove', width=16, bg='lightblue')
        symbol_menu = tk.Menu(symbolbutton, tearoff=False)
        symbolbutton['menu'] = symbol_menu
        for text in self.shapes:
            symbol_menu.add_radiobutton(label=text,
                                        variable=self.pltsymbol,
                                        value=text,
                                        indicatoron=True)
        symbolbutton.grid(row=2, column=1, sticky='news', padx=2, pady=2)
        row += 1

        tk.Label(frame1, text='Legend pos:').grid(row=3, column=0,
                                                  padx=2, pady=2)
        legendposbutton = tk.Menubutton(frame1, textvariable=self.legendlocvar,
                                        relief='groove', width=16,
                                        bg='lightblue')
        legendpos_menu = tk.Menu(legendposbutton, tearoff=False)
        legendposbutton['menu'] = legendpos_menu
        # i = 0
        for i, p in enumerate(self.legend_positions):
            legendpos_menu.add_radiobutton(label=p,
                                           variable=self.legendlocvar,
                                           value=p,
                                           indicatoron=True)
            # i += 1
        legendposbutton.grid(row=3, column=1, sticky='news', padx=2, pady=2)

        tk.Label(frame1, text='Font:').grid(row=4, column=0, padx=2, pady=2)
        fontbutton = tk.Menubutton(frame1, textvariable=self.fontvar,
                                   width=16, bg='lightblue')
        font_menu = tk.Menu(fontbutton, tearoff=False)
        fontbutton['menu'] = font_menu
        for f in self.fonts:
            font_menu.add_radiobutton(label=f,
                                      variable=self.fontvar,
                                      value=f,
                                      indicatoron=True)
        fontbutton.grid(row=4, column=1, sticky='news', padx=2, pady=2)
        row += 1
        tk.Label(frame1, text='Font size:').grid(row=5, column=0,
                                                 padx=2, pady=2)
        tk.Scale(frame1, from_=8, to=26, resolution=0.5, orient='horizontal',
                 relief='groove', variable=self.fontsizevar).grid(row=5,
                                                                  column=1,
                                                                  padx=2,
                                                                  pady=2)

        tk.Label(frame1, text='linewidth:').grid(row=6, column=0,
                                                 padx=2, pady=2)
        tk.Scale(frame1, from_=1, to=10, resolution=0.5, orient='horizontal',
                 relief='groove', variable=self.linewidthvar).grid(row=6,
                                                                   column=1,
                                                                   padx=2,
                                                                   pady=2)
        row = 0
        scalesframe = tk.LabelFrame(self.plotprefswin, text="Axes Scales")
        scales = {0: 'norm', 1: 'log'}
        for i in range(2):
            tk.Radiobutton(scalesframe, text='x-' + scales[i],
                           variable=self.xscalevar, value=i).grid(row=0,
                                                                  column=i,
                                                                  pady=2)
            tk.Radiobutton(scalesframe, text='y-' + scales[i],
                           variable=self.yscalevar, value=i).grid(row=1,
                                                                  column=i,
                                                                  pady=2)
        scalesframe.grid(row=row, column=1, sticky='news', padx=2, pady=2)

        row += 1
        frame = tk.LabelFrame(self.plotprefswin, text='Graph type')
        frame.grid(row=row, column=0, columnspan=2, sticky='news',
                   padx=2, pady=2)
        for i in range(len(self.graphtypes)):
            tk.Radiobutton(frame, text=self.graphtypes[i],
                           variable=self.graphtypevar,
                           value=self.graphtypes[i]).grid(row=0, column=i,
                                                          pady=2)

        row += 1
        labelsframe = tk.LabelFrame(self.plotprefswin, text='Labels')
        labelsframe.grid(row=row, column=0, columnspan=2, sticky='news',
                         padx=2, pady=2)
        tk.Label(labelsframe, text='Title:').grid(row=0, column=0,
                                                  padx=2, pady=2)
        tk.Entry(labelsframe, textvariable=self.plottitlevar, bg='white',
                 relief='groove').grid(row=0, column=1, padx=2, pady=2)
        tk.Label(labelsframe, text='X-axis label:').grid(row=1, column=0,
                                                         padx=2, pady=2)
        tk.Entry(labelsframe, textvariable=self.plotxlabelvar, bg='white',
                 relief='groove').grid(row=1, column=1, padx=2, pady=2)
        tk.Label(labelsframe, text='Y-axis label:').grid(row=2, column=0,
                                                         padx=2, pady=2)
        tk.Entry(labelsframe, textvariable=self.plotylabelvar, bg='white',
                 relief='groove').grid(row=2, column=1, padx=2, pady=2)
        print(self.currdata)
        if self.currdata is not None:
            # print self.dataseriesvars
            row += 1
            seriesframe = tk.LabelFrame(self.plotprefswin,
                                        text='Data Series Labels')
            seriesframe.grid(row=row, column=0, columnspan=2, sticky='news',
                             padx=2, pady=2)
            # self.dataseriesvars=[]
            if len(self.dataseriesvars) == 0:
                self.setDataSeries(list(range(len(self.currdata))))
            r = 1
            sr = 1
            cl = 0
            for s in self.dataseriesvars:
                tk.Label(seriesframe, text='Series ' + str(r)).grid(
                    row=r, column=cl, padx=2, pady=2)
                tk.Entry(seriesframe, textvariable=s, bg='white',
                         relief='groove').grid(row=r, column=cl + 1,
                                               padx=2, pady=2)
                r += 1
                if r > 8:
                    r = 1
                    cl += 2
            row += 1
            cbuttons = {}
            frame = tk.LabelFrame(self.plotprefswin, text="Dataset Colors")
            r = 1
            cl = 0
            sr = 1
            ci = 0
            for d, _ in enumerate(self.dataseriesvars):
                if d >= len(self.datacolors):
                    self.datacolors.append(self.colors[ci])
                    ci += 1
                c = self.datacolors[d]
                # action = lambda x = (d, c): choosecolor(x)
                cbuttons[d] = tk.Button(
                    frame, text='Series ' + str(sr), bg=c,
                    command=lambda x=(d, c): choosecolor(x))
                cbuttons[d].grid(row=r, column=cl, sticky='news',
                                 padx=2, pady=2)
                r += 1
                sr += 1
                if r > 8:
                    r = 1
                    cl += 1
            frame.grid(row=row, column=0, columnspan=2, sticky='news',
                       padx=2, pady=2)

        row += 1
        frame = tk.Frame(self.plotprefswin)
        frame.grid(row=row, column=0, columnspan=2, sticky='news',
                   padx=2, pady=2)
        replotb = tk.Button(
            frame, text="Replot",
            command=lambda: self.plotCurrent(graphtype=self.graphtype,
                                             guiopts=True),
            relief='groove', bg='#99ccff')
        replotb.pack(side='left', fill='x', padx=2, pady=2)
        b = tk.Button(frame, text="Apply", command=self.applyOptions,
                      relief='groove', bg='#99ccff')
        b.pack(side='left', fill='x', padx=2, pady=2)
        b = tk.Button(frame, text='Save', command=self.saveCurrent,
                      relief='groove', bg='#99ccff')
        b.pack(side='left', fill='x', padx=2, pady=2)
        c = tk.Button(frame, text='Close', command=close_prefsdialog,
                      relief='groove', bg='#99ccff')
        c.pack(side='left', fill='x', padx=2, pady=2)
        if self.currdata is None:
            replotb.configure(state='disabled')

        self.plotprefswin.focus_set()
        self.plotprefswin.grab_set()
