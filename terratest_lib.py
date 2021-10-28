# Terratest
# Zawiera metody do odczytywania danych z plików wytowrzonych przy pomocy sondy geologicznej Terratest
import json
from datetime import datetime

from PyQt5 import QtCore


class TerratestRead(object):
    """Dane z badania przy użyciu sondy terratest"""

    def __init__(self, path):
        file = open(path, 'rb')
        self.__data = file.read()
        file.close()

        self.__name = None
        self.__serial_number = None
        self.__hammer_weight = None
        self.__calibration_date = None
        self.__test_datetime = None
        self.__latitude = None
        self.__longitude = None

        self.__s1 = None
        self.__v1max = None
        self.__s1max = None

        self.__s2 = None
        self.__v2max = None
        self.__s2max = None

        self.__s3 = None
        self.__v3max = None
        self.__s3max = None

        self.__average_s = None
        self.__average_v = None
        self.__evd = None
        self.__s_v = None

    @property
    def name(self):
        if self.__name is None:
            self.__name = ""
            for i in range(172, 193):
                self.__name += chr(self.__data[i])

            return self.__name
        else:
            return self.__name

    @property
    def serial_number(self):
        if self.__serial_number is None:
            self.__serial_number = ""
            for i in range(2, 14):
                self.__serial_number += chr(self.__data[i])

            return self.__serial_number
        else:
            return self.__serial_number

    @property
    def hammer_height(self):
        if self.__hammer_weight is None:
            self.__hammer_weight = self.__data[14]

            return self.__hammer_weight
        else:
            return self.__hammer_weight

    @property
    def calibration_date(self):
        if self.__calibration_date is None:
            date = str(self.__data[15]) + " " + str(self.__data[16]) + " " + str(self.__data[17])
            self.__calibration_date = datetime.strptime(date, '%d %m %y')

            return self.__calibration_date
        else:
            return self.__calibration_date

    @property
    def test_datetime(self):
        if self.__test_datetime is None:
            a = (hex(self.__data[19]))
            test_year = a[2:]
            a = (hex(self.__data[20]))
            test_mounth = a[2:]
            a = (hex(self.__data[21]))
            test_day = a[2:]
            a = (hex(self.__data[22]))
            test_hour = a[2:]
            a = (hex(self.__data[23]))
            test_minute = a[2:]
            a = (hex(self.__data[24]))
            test_seconds = a[2:]

            date_time = str(test_year) + "/" + str(test_mounth) + "/" + str(test_day) + " " + str(
                test_hour) + ":" + str(test_minute) + ":" + str(test_seconds)
            self.__test_datetime = datetime.strptime(date_time, '%y/%m/%d %H:%M:%S')

            return self.__test_datetime
        else:
            return self.__test_datetime

    @property
    def latitude(self):
        if self.__latitude is None:
            self.__latitude = ""
            for i in range(26, 36):
                self.__latitude += chr(self.__data[i])

            return self.__latitude
        else:
            return self.__latitude

    @property
    def longitude(self):
        if self.__longitude is None:
            self.__longitude = ""
            for i in range(36, 47):
                self.__longitude += chr(self.__data[i])

            return self.__longitude
        else:
            return self.__longitude

    @property
    def s1(self):
        if self.__s1 is None:
            self.__s1 = []
            for i in range(47, 167):
                self.__s1.append(self.__data[i] / 200)

            return self.__s1
        else:
            return self.__s1

    @property
    def v1max(self):
        if self.__v1max is None:
            self.__v1max = float((self.__data[167] * 16 * 16 + self.__data[168]) / 10000)

            return self.__v1max
        else:
            return self.__v1max

    @property
    def s1max(self):
        if self.__s1max is None:
            self.__s1max = float((self.__data[169] * 16 * 16 + self.__data[170]) / 1000)

            return self.__s1max
        else:
            return self.__s1max

    @property
    def s2(self):
        if self.__s2 is None:
            self.__s2 = []
            for i in range(256, 376):
                self.__s2.append(self.__data[i] / 200)

            return self.__s2
        else:
            return self.__s2

    @property
    def v2max(self):
        if self.__v2max is None:
            self.__v2max = float((self.__data[376] * 16 * 16 + self.__data[377]) / 10000)

            return self.__v2max
        else:
            return self.__v2max

    @property
    def s2max(self):
        if self.__s2max is None:
            self.__s2max = float((self.__data[378] * 16 * 16 + self.__data[379]) / 1000)

            return self.__s2max
        else:
            return self.__s2max

    @property
    def s3(self):
        if self.__s3 is None:
            self.__s3 = []
            for i in range(384, 504):
                self.__s3.append(self.__data[i] / 200)

            return self.__s3
        else:
            return self.__s3

    @property
    def v3max(self):
        if self.__v3max is None:
            self.__v3max = float((self.__data[504] * 16 * 16 + self.__data[505]) / 10000)

            return self.__v3max
        else:
            return self.__v3max

    @property
    def s3max(self):
        if self.__s3max is None:
            self.__s3max = float((self.__data[506] * 16 * 16 + self.__data[507]) / 1000)

            return self.__s3max
        else:
            return self.__s3max

    @property
    def average_s(self):
        if self.__average_s is None:
            self.__average_s = round((self.s1max + self.s2max + self.s3max) / 3, 3)

            return self.__average_s
        else:
            return self.__average_s

    @property
    def evd(self):
        if self.__evd is None:
            self.__evd = round(22.5 / self.average_s, 3)

            return self.__evd
        else:
            return self.__evd

    @property
    def average_v(self):
        if self.__average_v is None:
            self.__average_v = round((self.v1max + self.v2max + self.v3max) / 3, 3)

            return self.__average_v
        else:
            return self.__average_v

    @property
    def s_v(self):
        return round(self.average_s / self.average_v, 3)

    def coordinates_g(self):
        latitude = self.latitude
        longitude = self.longitude

        len_lati = len(latitude)
        deg_lati = latitude[:2]
        min_lati = latitude[2:(len_lati - 1)]

        len_long = len(longitude)
        deg_long = longitude[:3]
        min_long = longitude[3:(len_long - 1)]

        latitude_g = float(deg_lati) + (float(min_lati) / 60)
        longitude_g = float(deg_long) + (float(min_long) / 60)

        # Dodanie znaków ujemnych przed współrzędnymi dla odpowiednich półkul
        if latitude[(len_long - 2):] == 'S':
            latitude_g = latitude_g * (-1)
        if longitude[(len_long - 1):] == 'W':
            longitude_g = longitude_g * (-1)

        return latitude_g, longitude_g

    def atr_for_layer(self):
        cords = self.coordinates_g()
        data = [
            self.name,
            self.serial_number,
            QtCore.QDate.fromString(self.calibration_date.strftime("%d.%m.%Y"), "dd.MM.yyyy"),
            QtCore.QDateTime.fromString(self.test_datetime.strftime("%d.%m.%Y %H:%M:%S"),
                                        "dd.MM.yyyy hh:mm:ss"),
            cords[0],
            cords[1],
            json.dumps(self.s1),
            self.v1max,
            self.s1max,
            json.dumps(self.s2),
            self.v2max,
            self.s2max,
            json.dumps(self.s3),
            self.v3max,
            self.s3max,
            self.evd,
            self.average_s,
            self.s_v
        ]

        return data


class TerratestCalculate(object):
    SAND_FINE = 'piasek drobny'
    SAND_MEDIUM = 'piasek średni'
    SAND_COARSE = 'piasek gruby'
    MESS = 'pospółka'
    GRAVEL = 'żwir'

    GRANULARITY_CONTINUOUS = 'ciągłe'
    GRANULARITY_DISCONTINUOUS = 'nieciągłe'

    ID_GDDKIA = 'Według GDDKiA'
    ID_PISARCZYK_FINE = 'Według Pisarczyka - drobnoziarnisty'
    ID_PISARCZYK_COARSE = 'Według Pisarczyka - gruboziarnisty'

    SOILS = [
        SAND_FINE,
        SAND_MEDIUM,
        SAND_COARSE,
        MESS,
        GRAVEL
    ]

    GRANULARITIES = [
        GRANULARITY_CONTINUOUS,
        GRANULARITY_DISCONTINUOUS
    ]

    ID_METHOD = [
        ID_GDDKIA,
        ID_PISARCZYK_FINE,
        ID_PISARCZYK_COARSE
    ]

    @staticmethod
    def calculate_is(granularity, soil, evd):
        p1 = 0
        p2 = 0
        if granularity == TerratestCalculate.GRANULARITY_CONTINUOUS:
            if soil == TerratestCalculate.SAND_FINE:
                p1 = 0.0016
                p2 = 0.93
            elif soil == TerratestCalculate.SAND_MEDIUM:
                p1 = 0.0015
                p2 = 0.93
            elif soil == TerratestCalculate.SAND_COARSE:
                p1 = 0.0015
                p2 = 0.93
            elif soil == TerratestCalculate.MESS:
                p1 = 0.0013
                p2 = 0.93
            elif soil == TerratestCalculate.GRAVEL:
                p1 = 0.0012
                p2 = 0.92
        elif granularity == TerratestCalculate.GRANULARITY_DISCONTINUOUS:
            if soil == TerratestCalculate.SAND_FINE:
                p1 = 0.0013
                p2 = 0.94
            elif soil == TerratestCalculate.SAND_MEDIUM:
                p1 = 0.0013
                p2 = 0.93
            elif soil == TerratestCalculate.SAND_COARSE:
                p1 = 0.0013
                p2 = 0.94
            elif soil == TerratestCalculate.MESS:
                p1 = 0.0013
                p2 = 0.93
            elif soil == TerratestCalculate.GRAVEL:
                p1 = 0.0011
                p2 = 0.93

        return p1 * evd + p2

    @staticmethod
    def calculate_e2(granularity, soil, evd):
        p1 = 0
        p2 = 0

        if granularity == TerratestCalculate.GRANULARITY_CONTINUOUS:
            if soil == TerratestCalculate.SAND_FINE:
                p1 = 2.06
                p2 = -9.2
            elif soil == TerratestCalculate.SAND_MEDIUM:
                p1 = 1.91
                p2 = 9.17
            elif soil == TerratestCalculate.SAND_COARSE:
                p1 = 2.03
                p2 = -8.35
            elif soil == TerratestCalculate.MESS:
                p1 = 1.7
                p2 = 10.56
            elif soil == TerratestCalculate.GRAVEL:
                p1 = 1.86
                p2 = 2.08
        elif granularity == TerratestCalculate.GRANULARITY_DISCONTINUOUS:
            if soil == TerratestCalculate.SAND_FINE:
                p1 = 1.57
                p2 = 5.91
            elif soil == TerratestCalculate.SAND_MEDIUM:
                p1 = 2.54
                p2 = -2.86
            elif soil == TerratestCalculate.SAND_COARSE:
                p1 = 2.19
                p2 = -5.07
            elif soil == TerratestCalculate.MESS:
                p1 = 1.85
                p2 = 3.54
            elif soil == TerratestCalculate.GRAVEL:
                p1 = 1.57
                p2 = 5.91

        return p1 * evd + p2

    @staticmethod
    def calculate_id(granularity, soil, evd, id_type):
        is_value = TerratestCalculate.calculate_is(granularity, soil, evd)

        result = 0

        if id_type == TerratestCalculate.ID_GDDKIA and is_value != 0:
            result = 5.50575 - 4.70115 / is_value
        elif id_type == TerratestCalculate.ID_PISARCZYK_FINE:
            result = (is_value - 0.855) / 0.165
        elif id_type == TerratestCalculate.ID_PISARCZYK_COARSE:
            result = (is_value - 0.78) / 0.33

        return result
