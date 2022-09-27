import pandas as pd
import os
from collections import defaultdict
import numpy as np
import Exceptions

class Data:

    def __init__(self):
        # pep_totaal = pd.read_csv()
        # TODO
        self.projectDir = 'S:'
        self.pep_ldot = pd.read_excel('S:\code\ldot_exports\pep_ldot_koppeltabel.xlsx', sheet_name='1004', index_col=None)   #   - actual - but currently have S-drive acces issues
        self.pepDictMain, self.pepDictPseudonyms = self.create_pep_dict()

        self._pep_id = None
        self._zm_id = None
        self._ap_id = None
        self._em_id = None
        self._qu_id = None
        self._ldot = None
        self._visit = '1'

    def create_pep_dict(self):
        """ Create map{pep-id -> pseudos} and map{pseudo -> pep-id} """
        pepDictMain = {}
        pepDictPseudonyms = {}
        df = pd.read_csv(os.path.join(self.projectDir, 'code', 'pep_exports', 'PEPtotaal.csv'), header=None)
        for i, row in df.iterrows():
            pepID = row[0]
            pseudos = row[1:].tolist()

            pepDictMain[pepID] = pseudos

            for p in pseudos:
                pepDictPseudonyms[p] = pepID

        #pepDictPseudonyms_wide = defaultdict(list)
        return pepDictMain, pepDictPseudonyms

    @staticmethod
    def copy2clip(txt):
        # Copy string argument to clipboard
        cmd = 'echo ' + txt.strip() + '|clip'
        return subprocess.check_call(cmd, shell=True)

    def pep_to_ldot(self, pepid):
        """ For a given PEP-id return the matching Ldot """
        val = self.pep_ldot['REGISTRATION_ID'].loc[self.pep_ldot['PEP_ID'] == pepID].values[0]
        if val == '': raise Exception(f'No Ldot availabel for pepID: {pepid}')
        return val


    def pep_from_ldot(self, key):
        """ Get HBS PEP key from ldot """
        key = int(key)
        print('ldot:', key)
        try:
            val = self.pep_ldot[self.pep_ldot['REGISTRATION_ID'] == key]['PEP_ID'].values[0]
        except KeyError as e:
            print(f'No LDOT entry for: {key}')
        except IndexError as e:
            print(f'No PEP id entry for ldot: {key}')
        self._pep_id = val
        return val

    def update_zm_id(self):
        # TODO
        x = self.pepDictMain[self._pep_id]
        for i in x:
            if f"{self._visit}ZM" in i:
                self._zm_id = i
                return i

    def update_qu_id(self):
        # TODO
        x = self.pepDictMain[self._pep_id]
        for i in x:
            if f"QU" in i:
                self._qu_id = i
                return i

    def update_pep_id(self, pseudo):
        self._pep_id = self.pepDictPseudonyms[pseudo]

    def update_ldot(self):
        self._ldot = self.pep_to_ldot(self._pep_id)

    def update_visit(self, value):
        if not str(value) in {'', '1', '2', '3'}:
            raise Exceptions.BadVisitId('Visit input is invalid')
        self._visit = value

    def update_ap_id(self):
        x = self.pepDictMain[self._pep_id]
        for i in x:
            if f"{self._visit}AP" in i:
                self._ap_id = i
                return i

    def update_em_id(self):
        x = self.pepDictMain[self._pep_id]
        for i in x:
            if f"{self._visit}EM" in i:
                self._em_id = i
                return i
