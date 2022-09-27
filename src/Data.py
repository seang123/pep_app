
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

