# -*- coding: utf-8 -*-
"""
    Table Testing module.
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

    Testing general functionality of tables
"""

import random
import string
import tkinter as tk
from Tables import TableCanvas
from TableModels import TableModel


class App:
    """ tkinter wrapper for tests """
    def __init__(self, master):
        self.main = tk.Frame(master)
        self.main.pack(fill='both', expand=1)
        master.geometry('600x400+200+100')


def createRandomStrings(l, n):
    """create list of l random strings, each of length n"""
    names = []
    for _ in range(l):
        val = ''.join(random.choice(string.ascii_lowercase) for x in range(n))
        names.append(val)
    return names


def createData(rows=20, cols=5):
    """Creare random dict for test data"""

    data = {}
    names = createRandomStrings(rows, 16)
    colnames = createRandomStrings(cols, 5)
    for n in names:
        data[n] = {}
        data[n]['label'] = n
    for c in range(0, cols):
        colname = colnames[c]
        vals = [round(random.normalvariate(100, 50), 2)
                for i in range(0, len(names))]
        vals = sorted(vals)
        for i, n in enumerate(names):
            data[n][colname] = vals[i]
    return data


def createTable(model):
    """ create table """
    t = tk.Toplevel()
    app = App(t)
    master = app.main
    table = TableCanvas(master, model, rowheaderwidth=50)
    table.createTableFrame()
    return table


def test1(root):
    """Setup a table and populate it with data"""
    app = App(root)
    master = app.main
    model = TableModel()
    data = createData(40)
    # import after model created
    # print data
    model.importDict(data)
    table = TableCanvas(master, model,
                        cellwidth=60, cellbackgr='#e3f698',
                        thefont=('Arial', 12), rowheight=18, rowheaderwidth=30,
                        rowselectedcolor='yellow', editable=True)
    table.createTableFrame()
    # table.sortTable(columnName='label')
    # remove cols
    model.deleteColumns([0])
    model.deleteRows(list(range(0, 2)))
    # table.redrawTable()
    # add rows and cols
    table.addRow(1, label='aaazzz')
    table.addRow(label='bbb')
    table.addRow(**{'label': 'www'})
    table.addColumn('col6')
    model.data[1]['col6'] = 'TEST'
    # table.redrawTable()
    # change col labels
    model.columnlabels['col6'] = 'new label'
    # set and get selections
    table.setSelectedRow(2)
    table.setSelectedCol(1)
    table.setSelectedCells(1, 80, 2, 4)
    # print table.getSelectionValues()
    # table.plotSelected(graphtype='XY')
    # save data
    # table.addRows(50000)
    model.save('test.table')
    # load new data
    table.load('test.table')
    # root.after(2000, root.quit)
    return


def test2():
    """Multuple tables in one window"""
    t = tk.Toplevel()
    app = App(t)
    master = app.main
    c = 0
    r = 1
    for _ in range(12):
        model = TableModel()
        data = createData(50)
        model.importDict(data)
        fr = tk.Frame(master)
        if c % 3 == 0:
            c = 0
            r += 1
        fr.grid(row=r, column=c, sticky='nws')
        table = TableCanvas(fr, model, width=250, height=150, rowheaderwidth=0)
        table.createTableFrame()
        c += 1
    return


def test3():
    """Drawing large tables"""
    data = createData(10000)
    model = TableModel()
    model.importDict(data)
    createTable(model)
    return


def test4():
    """Filtering/searching"""
    model = TableModel()
    data = createData(100)
    model.importDict(data)
    model.addColumn('comment')
    for i in model.reclist:
        val = random.sample(['a', 'b', 'c'], 1)[0]
        model.data[i]['comment'] = val
    # searchterms = [('label', 'aa', 'contains', 'AND'),
    #                ('label', 'bb', 'contains', 'OR')]
    searchterms = [('comment', 'a', '!=', 'AND'),
                   ('comment', 'b', '!=', 'AND')]
    vals = model.getColumnData(columnIndex=0, filters=searchterms)
    # model.getColumns(model.columnNames, filters=searchterms)
    # model.getDict(model.columnNames, filters=searchterms)
    print('{0:0d} found'.format(len(vals)))
    # createTable(model)
    return


def test5():
    """frame placement"""
    import Pmw
    t = tk.Toplevel()
    app = App(t)
    master = app.main
    w = Pmw.Group(master,
                  tag_text='Show/Hide')
    w.pack(fill='both')
    f = tk.Frame(master)
    f.pack(fill='both')
    table = TableCanvas(w)
    table.createTableFrame()
    return


def GUITests():
    """Run standard tests"""
    root = tk.Tk()
    test1(root)
    test2()
    test3()
    test4()
    # test5()
    print('GUI tests done')
    return root


def main():
    root = GUITests()
    root.mainloop()
    # loadSaveTest()

if __name__ == '__main__':
    main()
