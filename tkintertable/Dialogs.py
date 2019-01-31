# -*- coding: utf-8 -*-
"""
    Table Dialog classes.
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

import tkinter as tk
# import types
# import tkinter.simpledialog
# import tkinter.filedialog
# import tkinter.messagebox


class RecordViewDialog(tk.simpledialog.Dialog):
    """Dialog for viewing and editing table records"""

    def __init__(self, parent, title=None, table=None, row=None):
        if table is not None:
            self.table = table
            self.model = table.getModel()
            self.row = row
            self.recdata = self.model.getRecordAtRow(row)
            self.recname = self.model.getRecName(row)
        else:
            return
        tk.simpledialog.Dialog.__init__(self, parent, title)
        self.result = None
        self.results = None

    def body(self, master):
        """Show all record fields in entry fields or labels"""
        # model = self.model
        cols = list(self.recdata.keys())
        self.editable = []
        self.fieldnames = {}
        self.fieldvars = {}
        self.fieldvars['Name'] = tk.StringVar()
        self.fieldvars['Name'].set(self.recname)
        tk.Label(master, text='Rec Name:').grid(row=0, column=0,
                                                padx=2, pady=2,
                                                sticky='news')
        tk.Entry(master, textvariable=self.fieldvars['Name'],
                 relief='groove', bg='yellow').grid(row=0, column=1,
                                                    padx=2, pady=2,
                                                    sticky='news')
        # i=1
        for i, col in enumerate(cols, 1):
            self.fieldvars[col] = tk.StringVar()
            if col in self.recdata:
                val = self.recdata[col]
                self.fieldvars[col].set(val)
            self.fieldnames[col] = tk.Label(master, text=col).grid(
                row=i, column=0, padx=2, pady=2, sticky='news')
            ent = tk.Entry(master, textvariable=self.fieldvars[col],
                           relief='groove', bg='white')
            ent.grid(row=i, column=1, padx=2, pady=2, sticky='news')
            if not isinstance(self.recdata[col], bytes):
                ent.config(state='disabled')
            else:
                self.editable.append(col)
        top = self.winfo_toplevel()
        top.columnconfigure(1, weight=1)
        return

    def apply(self):
        """apply"""
        cols = self.table.cols
        model = self.model
        absrow = self.table.get_AbsoluteRow(self.row)
        newname = self.fieldvars['Name'].get()
        if newname != self.recname:
            model.setRecName(newname, absrow)

        for col in range(cols):
            colname = model.getColumnName(col)
            if colname not in self.editable:
                continue
            if colname not in self.fieldvars:
                continue
            val = self.fieldvars[colname].get()
            model.setValueAt(val, absrow, col)
            # print 'changed field', colname

        self.table.redrawTable()
        return


class MultipleValDialog(tk.simpledialog.Dialog):
    """Simple dialog to get multiple values"""

    def __init__(self, parent, title=None, initialvalues=None,
                 labels=None, types=None):
        if labels is not None and types is not None:
            self.initialvalues = initialvalues
            self.labels = labels
            self.types = types
        tk.simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        # r = 0
        self.vrs = []
        self.entries = []
        for i in range(len(self.labels)):
            tk.Label(
                master,
                # text=self.labels[i]).grid(row=r, column=0, sticky='news')
                text=self.labels[i]).grid(row=i, column=0, sticky='news')
            if self.types[i] == 'int':
                self.vrs.append(tk.IntVar())
            else:
                self.vrs.append(tk.StringVar())
            if self.types[i] == 'password':
                show = '*'
            else:
                show = None

            if self.types[i] == 'list':
                button = tk.Menubutton(master,
                                       textvariable=self.vrs[i],
                                       relief='raised')
                menu = tk.Menu(button, tearoff=False)
                button['menu'] = menu
                choices = self.initialvalues[i]
                for choice in choices:
                    menu.add_radiobutton(label=choice,
                                         variable=self.vrs[i],
                                         value=choice,
                                         indicatoron=True)
                self.entries.append(button)
                self.vrs[i].set(self.initialvalues[i][0])
            else:
                self.vrs[i].set(self.initialvalues[i])
                self.entries.append(tk.Entry(master, textvariable=self.vrs[i],
                                             show=show, bg='white'))
            # self.entries[i].grid(row=r, column=1, padx=2, pady=2,
            self.entries[i].grid(row=i, column=1, padx=2, pady=2,
                                 sticky='news')
            # r += 1
        return self.entries[0]  # initial focus

    def apply(self):
        self.result = True
        self.results = []
        for i in range(len(self.labels)):
            self.results.append(self.vrs[i].get())
