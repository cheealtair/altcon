import abc        # Abstract Base Class
class broker(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        pass

    @abc.abstractmethod
    def getRate(self, sFrom, sTo ):
        raise NotImplementedError('users must define each interface')
        pass