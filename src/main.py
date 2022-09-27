import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import numpy as np
import Exceptions
from Data import Data
from Control import Control

# https://www.pythontutorial.net/tkinter/

# Configure the size of cells in a column, weight indicates their width relative to each other
# root.columnconfigure(0, weight=1) # column 0 has size 1
# root.columnconfigure(1, weight=3) # column 1 is 3x the size of col 0
# padding=(left, top, right, bottom)


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

    def process(self, widget, name):
        """ Update the variables using the given widgets input value
        :param
            widget - a tk.Entry widget
            name - the name of the variable
        """
        content = widget.get()
        self.controller.update(content, name)
        self.update_all()

    def _create_pep_entry(self):
        """ PEP id entry """
        ttk.Label(self.frame_left, text='PEP:', padding=(5, 5, 5, 5)).grid(column=0, row=0, sticky=tk.W)
        self.frame_left.var = tk.StringVar(value='HB') # Store variable in frame_left for it to show in the entry widget
        self.text_variables['_pep_id'] = self.frame_left.var
        pep_id_entry = ttk.Entry(self.frame_left, width=30, textvariable=self.frame_left.var)
        pep_id_entry.focus()
        pep_id_entry.grid(column=1, row=0, stick=tk.E)

        # pep_id_entry.bind('<Return>', process)
        pep_id_entry.bind('<Return>',
                         lambda event, widget=pep_id_entry, name='pep': self.process(widget, name))

    def _create_zm_entry(self):
        ttk.Label(self.frame_left, text = 'ZM:', padding=(5, 5, 5, 5)).grid(column=0, row=1, sticky=tk.W)
        self.frame_left.zm_id_text = tk.StringVar(value='HB')
        self.text_variables['_zm_id'] = self.frame_left.zm_id_text
        zm_id_entry = ttk.Entry(self.frame_left, width=30, textvariable=self.frame_left.zm_id_text)
        zm_id_entry.grid(column=1, row=1, stick=tk.E)

        zm_id_entry.bind('<Return>',
                         lambda event, widget=zm_id_entry, name='zm': self.process(widget, name))

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
        """ Create the GUI """
        self.title('PEP id\'s')
        self.geometry('600x400+50+50')  # width*height+x+y
        print(self.winfo_screenwidth())

        self._create_pep_entry()
        self._create_zm_entry()
        self._create_visit_entry()


if __name__ == '__main__':
    app = App()
    app.mainloop()