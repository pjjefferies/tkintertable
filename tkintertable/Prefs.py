# -*- coding: utf-8 -*-
"""
    Manages preferences for Table class.

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
import pickle


class Preferences:
    """
    Class to store preferences
    """
    def __init__(self, program, defaults):
        """Find and load the preferences file"""
        # filename = '.' + program + '_preferences'
        filename = program + '_preferences'
        dirs = self.get_dirs()
        dirs = ['.']
        self.noprefs = False
        try:
            for ldir in dirs:
                fname = os.path.join(ldir, filename)
                if os.path.isfile(fname):
                    self.load_prefs(fname)
                    self.save_prefs()
                    return
                else:
                    self.noprefs = True
            if self.noprefs:
                raise ValueError
        except ValueError:
            # If we didn't find a file then set to default and save
            print('Did not find preferences!!!')
            self.prefs = defaults.copy()
            self.pref_file = os.path.join(dirs[0], filename)
            self.prefs['_prefdir'] = dirs[0]
            self.prefs['_preffile'] = self.pref_file
            self.save_prefs()

            # Defaults savedir?

            if 'HOMEPATH' in os.environ:
                self.prefs['datadir'] = os.environ['HOMEPATH']
            if 'HOME' in os.environ:
                self.prefs['datadir'] = os.environ['HOME']

            # Use 'my documents' if available
            if hasattr(self.prefs, 'datadir'):
                mydocs = os.path.join(self.prefs['datadir'], 'My Documents')
                if os.path.isdir(mydocs):
                    self.prefs['datadir'] = mydocs
        # Always save
        self.save_prefs()

    def __del__(self):
        # Make sure we save the file when killed
        self.save_prefs()

    def set(self, key, value):
        """ Set a key """
        self.prefs[key] = value
        self.save_prefs()

    def get(self, key):
        """ get a key """
        try:
            return self.prefs[key]
        except KeyError:
            raise NameError('No such key')
        # if key in self.prefs:
        #     return self.prefs[key]
        # else:
        #     raise NameError('No such key')
        # return

    def delete(self, key):
        """ delete a key """
        try:
            del self.prefs[key]
        except KeyError:
            raise ValueError('Error.')
        # if key in self.prefs:
        #     del self.prefs[key]
        # else:
        #     raise ValueError('Error.')
        self.save_prefs()

    def get_dirs(self):
        """ Compile a prioritised list of all dirs """
        dirs = []
        keys = ['HOME', 'HOMEPATH', 'HOMEDRIVE']
        # import os
        # import sys
        for key in keys:
            if key in os.environ:
                dirs.append(os.environ[key])

        if 'HOMEPATH' in os.environ:
            # windows
            dirs.append(os.environ['HOMEPATH'])

        # Drives
        possible_dirs = ["C:\\", "D:\\", "/"]
        for pdir in possible_dirs:
            if os.path.isdir(pdir):
                dirs.append(pdir)
        #
        # Check that all dirs are real
        #
        rdirs = []
        for dirname in dirs:
            if os.path.isdir(dirname):
                rdirs.append(dirname)
        return rdirs

    def load_prefs(self, filename):
        """ Load prefs """
        self.pref_file = filename
        print("loading prefs from ", self.pref_file)
        try:
            fdesc = open(filename)
            self.prefs = pickle.load(fdesc)
            fdesc.close()
        except (FileNotFoundError, TypeError):
            fdesc.close()
            fdesc = open(filename, 'rb')
            self.prefs = pickle.load(fdesc)
            fdesc.close()

    def save_prefs(self):
        """ Save prefs """
        # import pickle
        try:
            fdesc = open(self.pref_file, 'wb')
            # pickle.dump(self.prefs.decode('utf-8'), fdesc)
            pickle.dump(self.prefs, fdesc)
            fdesc.close()
        except FileNotFoundError:
            print('could not save')
            # return
        # import sys
        # if sys.version_info >= (3, 0):
        # pickle.dump(self.prefs.decode('utf-8'), fdesc)
        # else:
        # pickle.dump(self.prefs,fd)
        # fd.close()
