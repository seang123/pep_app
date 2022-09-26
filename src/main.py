import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import numpy as np

# Configure the size of cells in a column, weight indicates their width relative to each other
# root.columnconfigure(0, weight=1) # column 0 has size 1
# root.columnconfigure(1, weight=3) # column 1 is 3x the size of col 0


class BadVisitId(Exception):
    pass


class Data:

    def __init__(self):
        # pep_totaal = pd.read_csv()
        # TODO
        pass

    def get_zm_id(self, pep_id, visit):
        # TODO
        return pep_id + '--zm_id' + '--visit_1'

    def get_qu_id(self, pep_id):
        # TODO
        return pep_id + '--qu_id'

    def get_pep_id(self, pseudo):
        # return pepDictPseudonym[pseudo]
        return 'HB' + str(np.random.randint(1111111, 9999999))


class Control:
    def __init__(self):
        """ Handle any file reading/writing,
            storing of variables, etc.
        """
        self._pep_id = None
        self._zm_id = None
        self._qu_id = None
        self._ldot = None
        self._visit = None

        self.data = Data()

    def update_visit(self, value):
        if not str(value) in {'1', '2', '3'}:
            raise BadVisitId('Visit input is invalid')
        self._visit = value

    def update(self, value, variable):
        if variable == 'pep':
            self._pep_id = value
            if self._visit:
                self._zm_id = self.data.get_zm_id(self._pep_id, self._visit)
                self._qu_id = self.data.get_qu_id(self._pep_id)
        elif variable == 'zm':
            self._zm_id = value
            if self._visit:
                self._pep_id = self.data.get_pep_id(value)
                self._qu_id = self.data.get_qu_id(self._pep_id)
        elif variable == 'qu':
            self._qu_id = value
            if self._visit:
                self._pep_id = self.data.get_pep_id(value)
                self._zm_id = self.data.get_zm_id(self._pep_id, self._visit)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.controller = Control()

        self.text_variables = {}

        self.frame_left = ttk.Frame(self)
        self.frame_left.grid(column=0, row=1)
        self.frame_right = ttk.Frame(self)
        self.frame_right.grid(column=1, row=1)

        self.create_labels()

    def run(self):
        self.mainloop()

    def update_all(self):
        """ When an Entry is made, update all fields to match the new entry """
        print(self.controller.__dict__)
        for k, v in self.text_variables.items():
            print(k, '--', self.controller.__dict__[k])
            v.set(self.controller.__dict__[k])

    def _create_pep_entry(self):
        """ PEP id entry """
        # padding=(left, top, right, bottom)
        ttk.Label(self.frame_left, text='PEP:', padding=(5, 5, 5, 5)).grid(column=0, row=0, sticky=tk.W)
        self.frame_left.var = tk.StringVar(value='HB') # Store variable in frame_left for it to show in the entry widget
        self.text_variables['_pep_id'] = self.frame_left.var
        pep_id_entry = ttk.Entry(self.frame_left, width=30, textvariable=self.frame_left.var)
        pep_id_entry.focus()
        pep_id_entry.grid(column=1, row=0, stick=tk.E)

        def process(event=None):
            content = pep_id_entry.get()
            print(content)
            self.controller.update(content, 'pep')
            self.update_all()

        pep_id_entry.bind('<Return>', process)

    def _create_zm_entry(self):
        ttk.Label(self.frame_left, text = 'ZM:', padding=(5, 5, 5, 5)).grid(column=0, row=1, sticky=tk.W)
        self.frame_left.zm_id_text = tk.StringVar(value='HB')
        self.text_variables['_zm_id'] = self.frame_left.zm_id_text
        zm_id_entry = ttk.Entry(self.frame_left, width=30, textvariable=self.frame_left.zm_id_text)
        zm_id_entry.grid(column=1, row=1, stick=tk.E)

        def process(event=None):
            content = zm_id_entry.get()
            self.controller.zm_id = content
            self.controller.update(content, 'zm')
            self.update_all()
        zm_id_entry.bind('<Return>', process)

    def _create_visit_entry(self):
        ttk.Label(self.frame_right, text='Visit:', padding=(5, 5, 5, 5)).grid(column=0, row=0, stick=tk.W)
        self.frame_right.visit_id_text = tk.StringVar(value='')
        visit_entry = ttk.Entry(self.frame_right, width=10, textvariable=self.frame_right.visit_id_text)
        visit_entry.grid(column=1, row=0, sticky=tk.E)

        def process(event=None):
            content = visit_entry.get()
            print('Visit set to:', content)
            self.controller.visit = content
            self.controller.update_visit(content)
        visit_entry.bind('<Return>', process)
        visit_entry.bind('<FocusOut>', process, add='+')
        visit_entry.bind('<KeyRelease>', process, add='+')  # <Leave>

    def create_labels(self):
        # Call at init to create the GUI
        self.title('PEP id\'s')
        self.geometry('600x400+50+50')  # width*height+x+y
        print(self.winfo_screenwidth())
        # ttk.Label(self, text = 'PEP id\'s').grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self._create_pep_entry()
        self._create_zm_entry()
        self._create_visit_entry()


if __name__ == '__main__':
    app = App()
    app.mainloop()