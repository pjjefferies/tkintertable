# -*- coding: utf-8 -*-
"""
    Import and export classes.
    Created Oct 2008
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

import os
import csv
import tkinter as tk
import Pmw
# import tkinter.filedialog


class TableImporter:
    """Provides import utility methods for the Table and Table Model classes"""

    def __init__(self):
        """Setup globals"""
        # self.separator = ','
        self.separator_list = {',': ',', ' ': 'space', '\t': 'tab',
                               'blank': ' ', ':': ':'}
        self.var_sep = tk.StringVar()
        self.var_sep.set(',')
        self.data = None
        self.datafile = None
        self.CancelButton = None
        self.importButton = None
        self.openButton = None
        self.previewarea = None
        self.textframe = None
        self.sep_choice = None
        self.ysize = None
        self.xsize = None
        self.master = None
        self.parent = None

    def import_Dialog(self, parent):
        """Allows user to set some import options"""
        self.parent = parent
        self.master = tk.Toplevel()
        self.master.title("Import Data")
        self.xsize = 450
        self.ysize = 370
        # top = self.master.winfo_toplevel()
        # rootx = top.winfo_rootx()
        # rooty = top.winfo_rooty()

        self.sep_choice = Pmw.OptionMenu(
            parent=self.master,
            labelpos='w',
            label_text='Record separator:',
            menubutton_textvariable=self.var_sep,
            items=list(self.separator_list.keys()),
            initialitem=',',
            menubutton_width=4,
            command=self.update_display)

        self.sep_choice.grid(row=0, column=0, sticky='nw', padx=2, pady=2)
        # place for text preview frame

        self.textframe = Pmw.ScrolledFrame(
            self.master,
            labelpos='n', label_text='Preview',
            usehullsize=1,
            hull_width=450,
            hull_height=300)
        self.textframe.grid(row=1, column=0, columnspan=5,
                            sticky='news', padx=2, pady=2)
        self.previewarea = tk.Text(self.textframe.interior(), bg='white',
                                   width=400, height=500)
        self.previewarea.pack(fill='both', expand=1)
        # buttons
        self.openButton = tk.Button(self.master, text='Open File',
                                    command=self.do_openFile)
        self.openButton.grid(row=3, column=0, sticky='news', padx=2, pady=2)
        self.importButton = tk.Button(self.master, text='Do Import',
                                      command=self.do_ModelImport)
        self.importButton.grid(row=3, column=1, sticky='news', padx=2, pady=2)
        self.CancelButton = tk.Button(self.master, text='Cancel',
                                      command=self.close)
        self.CancelButton.grid(row=3, column=2, sticky='news', padx=2, pady=2)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        return self.master

    def do_openFile(self):
        """ do open file """
        self.datafile = self.open_File(self.parent)
        self.update_display()
        return

    def open_File(self, parent):
        print('open_File')
        """ open file """
        savedir = os.getcwd()
        print('savedir:', savedir)
        filename = tk.filedialog.askopenfile(
            defaultextension='.csv',
            initialdir=savedir,
            initialfile='',
            filetypes=[("Data file", "*.csv"),
                       ("All files", "*.*")],
            title=('Choose data from a .csv file saved as excel ' +
                   'spreadsheet in .csv format (comma separated list)'),
            parent=parent)
        print('filename:', filename)
        if (filename and
                os.path.exists(filename.name) and
                os.path.isfile(filename.name)):
            datafile = filename.name
        return datafile

    def update_display(self, evt=None):
        """Preview loaded file"""
        sep = self.var_sep.get()[0]
        self.previewarea.delete(1.0, 'end')
        # reader = csv.reader(open(self.datafile, "rb"), delimiter=sep)
        reader = csv.reader(open(self.datafile, "r"), delimiter=sep)
        for row in reader:
            self.previewarea.insert('end', row)
            self.previewarea.insert('end', '\n')
        return

    def do_ModelImport(self):
        """imports and places the result in self.modeldata"""
        self.data = self.ImportTableModel(self.datafile)
        self.close()
        return

    def ImportTableModel(self, filename):
        """Import table data from a comma separated file and create data for
           a model. This is reusable outside the GUI dialog also."""

        if filename is None:
            return None
        if not os.path.isfile(filename):
            return None
        try:
            sep = self.var_sep.get()
        except tk.TclError:
            sep = ','
        # takes first row as field names
        # dictreader = csv.DictReader(open(filename, "rb"), delimiter=sep)
        dictreader = csv.DictReader(open(filename, "r"), delimiter=sep)
        dictdata = {}
        for count, rec in enumerate(dictreader):
            dictdata[count] = rec
        return dictdata

    def close(self):
        """ close """
        self.master.destroy()
        return


class TableExporter:
    """Provides export utility methods for the Table and
    Table Model classes"""
    def __init__(self):
        return

    def ExportTableData(self, table, sep=None):
        """Export table data to a comma separated file"""

        parent = table.parentframe
        filename = tk.filedialog.asksaveasfilename(
            parent=parent,
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv")])
        if not filename:
            return
        if sep is None:
            sep = ','
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=sep)
            model = table.getModel()
            recs = model.getAllCells()
            # take column labels as field names
            colnames = model.columnNames
            collabels = model.columnlabels
            row = []
            for col in colnames:
                row.append(collabels[col])
            writer.writerow(row)
            for row in list(recs.keys()):
                writer.writerow(recs[row])
        return
