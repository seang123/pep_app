import tkinter as tk
from tkinter import ttk
import os
import subprocess
from Utils import emp_duration

class ButtonFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._create_widgets()


    def open_participant_folder(self):
        os.startfile(f'S:\hbs\sub-{self.parent.controller.data._pep_id}')


    def open_participant_button(self):
        ttk.Button(self, text='Open', command = self.open_participant_folder).grid(column=0, row=0, sticky=tk.W)#.pack(side = tk.RIGHT)


    def empatica_duration_button(self):
        def compute_duration():
            print('Computing emp duration')
            #out = subprocess.check_output(['cd', 'C:\\Users\\seagie\\Desktop\\Empatica_temporary', '&&', 'emp_duration.py'], shell=True)
            duration = emp_duration.compute_duration()
            print('Empatica duration:', duration, '(hours)')
        ttk.Button(self, text='Emp dur', command = compute_duration).grid(column=0, row=2, sticky=tk.W)


    def zip_files(self):
        """ Zip files function
        Calls an external python script
        """
        zm_id = self.parent.controller.data._zm_id
        visit = self.parent.controller.data._visit
        subprocess.Popen(['cd', 'C:\\Users\\seagie\\Desktop\\ZMax_temporary', '&&', 'zip_files.py', '--zm_id', str(zm_id), '--lab_visit', str(visit)], shell=True)


    def _create_zip_button(self):
        ttk.Button(self, text='Zip ZMax', command = self.zip_files).grid(column=0, row=1, sticky=tk.W)


    def _create_widgets(self):
        """ Create the button widgets """
        self.empatica_duration_button()
        self._create_zip_button()
        self.open_participant_button()
