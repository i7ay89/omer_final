class Table(object):
    def __init__(self, table_id, capacity, smoking=False, outdoor=False, bar=False, mobile=False, handicapped=False):
        self.__capacity = capacity
        self.__id = table_id
        self.__smoking = smoking
        self.__outdoor = outdoor
        self.__bar = bar
        self.__mobile = mobile
        self.__handicapped = handicapped

    @property
    def capacity(self):
        return self.__capacity

    @property
    def id(self):
        return self.__id

    @property
    def smoking(self):
        return self.__smoking

    @property
    def outdoor(self):
        return self.__outdoor

    @property
    def mobile(self):
        return self.__mobile

    @property
    def handicapped(self):
        return self.__handicapped

    def __str__(self):
        return 'Table ID: {}\nCapacity: {}\nsmoking: {}\noutdoor: {}\nbar: {}\nmobile: {}\nhandicapped: {}'.\
            format(self.__id, self.__capacity, self.__smoking,
                   self.__outdoor, self.__bar, self.__mobile, self.__handicapped)