class KeyStoneException(Exception):
    def __init__(self):
        self.__message = 'Error on acquiring keystone token.'
        super(KeyStoneException, self).__init__(self.__message)