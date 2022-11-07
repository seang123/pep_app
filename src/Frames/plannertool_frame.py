import tkinter as tk
from tkinter import ttk
import os
import subprocess

USER = os.getlogin()

"""
- Lab date
- RA

"""

class PlannertoolFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._create_widgets()

    def _create_widgets(self):

        self.frame_pt = ttk.LabelFrame(self, text='PlannerTool')
        self.frame_pt.grid(column=0, row=0, padx=(5,5), pady=(0,0))

        self.frame_pt.ra_string = tk.StringVar(value='RA')
        ttk.Entry(self.frame_pt, textvariable = self.frame_pt.ra_string, state='readonly', width=20).grid(
            column=0, row=0, sticky=tk.W, padx=(5,5), pady=(5,5))

        self.frame_pt.date_string = tk.StringVar(value='Lab Date')
        ttk.Entry(self.frame_pt, textvariable = self.frame_pt.date_string, state='readonly', width=20).grid(
            column=0, row=1, sticky=tk.W, padx=(5,5), pady=(5,5))

        self.frame_pt.slot_string = tk.StringVar(value='MRI slot')
        ttk.Entry(self.frame_pt, textvariable = self.frame_pt.slot_string, state='readonly', width=20).grid(
            column=0, row=2, sticky=tk.W, padx=(5,5), pady=(5,5))

    def update(self):

        ra = self.parent.controller.data._ra
        lab_visit_date = self.parent.controller.data._visit_date
        mri_slot = self.parent.controller.data._mri_slot

        self.frame_pt.ra_string.set(ra)
        self.frame_pt.date_string.set(lab_visit_date)
        self.frame_pt.slot_string.set(mri_slot)



    """
    def _create_email_label(self):
        self.frame_email = ttk.LabelFrame(self, text='Email')
        self.frame_email.grid(column = 0, row=4, padx=(5, 5), pady=(20,0))

        self.frame_email.email_template = tk.StringVar(value="dertigersbrein_00@donders.ru.nl")
        ttk.Entry(self.frame_email, textvariable = self.frame_email.email_template, state='readonly', width=50).grid(
            column=0, row=0, sticky=tk.W,
            padx=(5,5), pady=(5,5))

        self.frame_email.password_template = tk.StringVar(value="hbs2031")
        ttk.Entry(self.frame_email, textvariable = self.frame_email.password_template, state='readonly', width=50).grid(
            column=0, row=1, sticky=tk.W,
            padx=(5,5), pady=(5,5))
    """
