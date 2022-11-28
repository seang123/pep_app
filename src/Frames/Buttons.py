import tkinter as tk
from tkinter import ttk
import os
import subprocess
from Utils import emp_duration

USER = os.getlogin()

class ButtonFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._create_widgets()

    def _create_widgets(self):
        """ Create the button widgets """
        self.empatica_duration_button()
        self._create_zip_button()
        self.open_participant_button()
        self.empatica_rename_button()


    def open_participant_button(self):
        """ Open participant S:\hbs\sub-xxx folder """
        def open_participant_folder():
            os.startfile(f'S:\hbs\sub-{self.parent.controller.data._pep_id}\pre-{self.parent.controller.data._visit}\wrb')
        ttk.Button(self, text='Open', command = open_participant_folder).grid(column=0, row=0, sticky=tk.W)#.pack(side = tk.RIGHT)


    def empatica_duration_button(self):
        """ Empatica duration button
        Computes the duration of the recorded empatica data using the downloaded data
        Data must be in a specific folder -- see emp_duration.py
        """
        def compute_duration():
            duration = emp_duration.compute_duration()
            print('Empatica duration:', duration, '(hours)')
        ttk.Button(self, text='Emp dur', command = compute_duration).grid(column=0, row=2, sticky=tk.W)

    def empatica_rename_button(self):
        """ Rename empatica files """
        def rename():
            em_id = self.parent.controller.data._em_id
            lab_visit = self.parent.controller.data._visit
            emp_duration.rename_files(em_id, lab_visit)
        ttk.Button(self, text='Emp name', command = rename).grid(column=0, row=3, sticky=tk.W)

    def _create_zip_button(self):
        def zip_files():
            """ Zip files function
            Calls an external python script
            """
            zm_id = self.parent.controller.data._zm_id
            visit = self.parent.controller.data._visit
            subprocess.Popen(['cd', f'C:\\Users\\{USER}\\Desktop\\ZMax_temporary', '&&', 'zip_files.py', '--zm_id', str(zm_id), '--lab_visit', str(visit)], shell=True)
        ttk.Button(self, text='Zip ZMax', command = zip_files).grid(column=0, row=1, sticky=tk.W)


