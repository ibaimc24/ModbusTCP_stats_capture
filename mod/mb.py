import dpkt

class Modbus:

    def __init__(self,pkt,ts):
        self.__raw__ = pkt
        self.__ts__ = ts
        self.__size__ = len(pkt)
        self.__update__()

    def __update__(self):
        self.__code__ = self.__raw__[7]


    def get_code(self):
        return self.__code__

    def get_size(self):
        return self.__size__




