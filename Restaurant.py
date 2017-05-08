from Table import Table


class Restaurant(object):
    def __init__(self, opening_hour, closing_hour, tables=[]):
        self.__opening_hour = self.__parse_hour(opening_hour)
        self.__closing_hour = self.__parse_hour(closing_hour)
        self.__tables = tables       # type: list[Table]

    def __parse_hour(self, time):
        splitted = time.split(':')
        if len(splitted) != 2:
            return None
        hour = int(splitted[0])
        minute = int(splitted[1])

        return hour, minute

    def __validate_hours(self):
        if self.__closing_hour[0] > self.__opening_hour[0]:
            return False
        elif self.__closing_hour[0] == self.__opening_hour[0] and self.__opening_hour[1] < self.__closing_hour[1]:
            return False
        return True

    def add_table(self, table):
        self.__tables.append(table)
