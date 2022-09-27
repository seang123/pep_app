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
            print(k, '--', self.controller.data.__dict__[k])
            v.set(self.controller.data.__dict__[k])
        self.update_template_labels()

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

    def _create_qu_entry(self):
        ttk.Label(self.frame_left, text='QU:', padding = (5, 5, 5, 5)).grid(column = 0, row=2, sticky= tk.W)
        self.frame_left.qu_id_text = tk.StringVar(value='HB1QU')
        self.text_variables['_qu_id'] = self.frame_left.qu_id_text
        qu_id_entry = ttk.Entry(self.frame_left, width=30, textvariable=self.frame_left.qu_id_text)
        qu_id_entry.grid(column=1, row=2, stick=tk.E)

        qu_id_entry.bind('<Return>',
                         lambda event, widget=qu_id_entry, name='qu': self.process(widget, name))


    def _create_visit_entry(self):
        ttk.Label(self.frame_right, text='Visit:', padding=(5, 5, 5, 5)).grid(column=0, row=0, stick=tk.W)
        self.frame_right.visit_id_text = tk.StringVar(value='1')
        self.text_variables['_visit'] = self.frame_right.visit_id_text
        visit_entry = ttk.Entry(self.frame_right, width=10, textvariable=self.frame_right.visit_id_text)
        visit_entry.grid(column=1, row=0, sticky=tk.E)

        def process(event=None):
            content = visit_entry.get()
            self.controller.visit = content
            self.controller.update_visit(content)
        visit_entry.bind('<Return>', process)
        visit_entry.bind('<FocusOut>', process, add='+')
        visit_entry.bind('<KeyRelease>', process, add='+')  # <Leave>

    def _create_ldot_entry(self):
        ttk.Label(self.frame_right, text='LDot:', padding=(5, 5, 5, 5)).grid(column=0, row=1, stick=tk.W)
        self.frame_right.ldot_id_text = tk.StringVar()
        self.text_variables['_ldot'] = self.frame_right.ldot_id_text
        ldot_entry = ttk.Entry(self.frame_right, width=10, textvariable=self.frame_right.ldot_id_text)
        ldot_entry.grid(column=1, row=1, sticky=tk.E)

        ldot_entry.bind('<Return>',
                        lambda event, widget=ldot_entry, name='ldot': self.process(widget, name))



    def _create_file_name_templates(self):
        """ Create the labels for the file name templates  """
        """
        sub-HB3AP8008980_pre-3_wrb_apl (-evs)
        sub-HB3EM7817982_pre-3_wrb_emp_01.zip
        sub-HB3ZM9133849_pre-3_wrb_zmx_1.zip 
        sub-HB3ZM9133849_pre-3_wrb_zmx_raw.zip
        """

        self.frame_templates = ttk.LabelFrame(self, text='File templates')
        self.frame_templates.grid(column=0, row=3, padx=(5,0), pady=(20,0))

        ap_id = str(self.controller.data._ap_id)
        em_id = str(self.controller.data._em_id)
        zm_id = str(self.controller.data._zm_id)
        visit = str(self.controller.data._visit)

        self.frame_templates.ap_template = tk.StringVar(value=f"sub-{ap_id}_pre_{visit}_wrb_apl (-evs)")
        ttk.Entry(self.frame_templates, textvariable = self.frame_templates.ap_template, state='readonly', width=50).grid(
            column=0, row=0, sticky=tk.W,
            padx=(5,5), pady=(5,5))

        self.frame_templates.em_template = tk.StringVar(value=f"sub-{em_id}_pre_{visit}_wrb_emp_01.zip")
        ttk.Entry(self.frame_templates, textvariable = self.frame_templates.em_template, state='readonly', width=50).grid(
            column=0, row=1, sticky=tk.W,
            padx=(5,5), pady=(5,5))

        self.frame_templates.zm_template = tk.StringVar(value = f"sub-{zm_id}_pre_{visit}_wrb_zm_1.zip")
        ttk.Entry(self.frame_templates, textvariable = self.frame_templates.zm_template, state='readonly', width=50).grid(
            column=0, row=2, sticky=tk.W,
            padx=(5, 5),pady=(5,5))

    def update_template_labels(self):

        ap_id = str(self.controller.data._ap_id)
        em_id = str(self.controller.data._em_id)
        zm_id = str(self.controller.data._zm_id)
        visit = str(self.controller.data._visit)

        self.frame_templates.ap_template.set(f"sub-{ap_id}_pre_{visit}_wrb_apl (-evs)")
        self.frame_templates.em_template.set(f"sub-{em_id}_pre_{visit}_wrb_emp_01.zip")
        self.frame_templates.zm_template.set(f"sub-{zm_id}_pre_{visit}_wrb_zm_1.zip")


    def create_labels(self):
        """ Create the GUI """
        self.title('PEP id\'s')
        self.geometry('600x400+50+50')  # width*height+x+y
        print(self.winfo_screenwidth())

        self._create_pep_entry()
        self._create_zm_entry()
        self._create_qu_entry()
        #self._create_ap_entry()
        #self._create_em_entry()
        self._create_visit_entry()
        self._create_ldot_entry()
        self._create_file_name_templates()


if __name__ == '__main__':
    app = App()
    app.mainloop()