from Data import Data
import pandas as pd
import os

class Control:
    def __init__(self):
        """ Handle any file reading/writing,
            storing of variables, etc.
        """

        self.data = Data()

    def update_visit(self, value):
        self.data.update_visit(value)

    def update(self, value, variable):
        """
        If a pseudo is changed, first update the PEP id to reflect this change, then update all pseudos
        :param value:
        :param variable:
        :return:
        """
        if variable == 'pep':
            self.data._pep_id = value
            if self.data._visit:
                self.data.update_zm_id()
                self.data.update_qu_id()
                self.data.update_ap_id()
                self.data.update_em_id()
        elif variable == 'zm':
            self.data._zm_id = value
            self.data.update_visit(value[2])
            self.data.update_pep_id(value)
            if self.data._visit:
                self.data.update_qu_id()
                self.data.update_ap_id()
                self.data.update_em_id()
        elif variable == 'qu':
            self.data._qu_id = value
            self.data.update_pep_id(value)
            if self.data._visit:
                self.data.update_zm_id()
                self.data.update_ap_id()
                self.data.update_em_id()
        elif variable == 'ldot':
            self.data.pep_from_ldot(value)
            if self.data._visit:
                self.data.update_qu_id()
                self.data.update_zm_id()
                self.data.update_ap_id()
                self.data.update_em_id()
