from Data import Data

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
            raise Exceptions.BadVisitId('Visit input is invalid')
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
