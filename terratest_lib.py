#Terratest
#Zawiera metody do odczytywania danych z plików wytowrzonych przy pomocy sondy geologicznej Terratest

import numpy


class Terratest(object):
    """Dane z badania przy użyciu sondy terratest"""
    def __init__(self, path):
        file = open(path, 'rb')
        self.data = file.read()
        file.close()

        self.hammer_weight = ""
        self.serial_number = ""
        self.calibration_day = ""
        self.calibration_mounth = ""
        self.calibration_year = ""

        self.test_name = ""

        self.test_year = ""
        self.test_mounth = ""
        self.test_day = ""
        self.test_hour = ""
        self.test_minute = ""
        self.test_secound = ""
        self.test_weekday = ""

        self.latitude = ""
        self.longitude = ""

        self.s1 = []
        self.v1max = ""
        self.s1max = ""

        self.s2 = []
        self.v2max = ""
        self.s2max = ""

        self.s3 = []
        self.v3max = ""
        self.s3max = ""

        self.average_s = ""
        self.evd = ""
        self.s_v = ""

    def hammer(self):
        if self.serial_number:
            return self.serial_number, self.hammer_weight, self.calibration_day, self.calibration_mounth, self.calibration_year
        else:
            for i in range(2, 14):
                self.serial_number += chr(self.data[i])

            self.hammer_weight = self.data[14]
            self.calibration_day = self.data[15]
            self.calibration_mounth = self.data[16]
            self.calibration_year = self.data[17]

            return self.serial_number, self.hammer_weight, self.calibration_day, self.calibration_mounth, self.calibration_year

    def name(self):
        if self.test_name:
            return self.test_name
        else:
            for i in range(172, 193):
                self.test_name += chr(self.data[i])
            return self.test_name

    def test(self):
        if self.test_year:
            return self.test_year, self.test_mounth, self.test_day, self.test_hour, self.test_minute, self.test_secound, self.test_weekday
        else:
            a = (hex(self.data[19]))
            self.test_year = a[2:]
            a = (hex(self.data[20]))
            self.test_mounth = a[2:]
            a = (hex(self.data[21]))
            self.test_day = a[2:]
            a = (hex(self.data[22]))
            self.test_hour = a[2:]
            a = (hex(self.data[23]))
            self.test_minute = a[2:]
            a = (hex(self.data[24]))
            self.test_secound = a[2:]
            a = (hex(self.data[25]))
            self.test_weekday = a[2:]

            return self.test_year, self.test_mounth, self.test_day, self.test_hour, self.test_minute, self.test_secound, self.test_weekday

    def coordinates(self):
        if self.latitude:
            return self.latitude, self.longitude
        else:
            for i in range(26, 36):
                self.latitude += chr(self.data[i])
            for i in range(36, 47):
                self.longitude += chr(self.data[i])
            return self.latitude, self.longitude

    def coordinates_g(self):
        latitude, longitude = self.coordinates()

        len_lati = len(latitude)
        deg_lati = latitude[:2]
        min_lati = latitude[2:(len_lati - 1)]

        len_long = len(longitude)
        deg_long = longitude[:3]
        min_long = longitude[3:(len_long - 1)]

        latitude_g = float(deg_lati) + (float(min_lati)/60)
        longitude_g = float(deg_long) + (float(min_long) / 60)

        # Dodanie znaków ujemnych przed współrzędnymi dla odpowiednich półkul
        if latitude[(len_long - 2):] == 'S':
            latitude_g = latitude_g * (-1)
        if longitude[(len_long - 1):] == 'W':
            longitude_g = longitude_g * (-1)

        return latitude_g, longitude_g

    def drop1(self):
        if self.s1:
            return self.s1, self.v1max, self.s1max
        else:
            for i in range(47, 167):
                self.s1.append(self.data[i]/200)
                self.v1max = float((self.data[167] * 16 * 16 + self.data[168]) / 10000)
                self.s1max = float((self.data[169] * 16 * 16 + self.data[170]) / 1000)
            return self.s1, self.v1max, self.s1max

    def drop2(self):
        if self.s2:
            return self.s2, self.v2max, self.s2max
        else:
            for i in range(256, 376):
                self.s2.append(self.data[i]/200)
                self.v2max = float((self.data[376] * 16 * 16 + self.data[377]) / 10000)
                self.s2max = float((self.data[378] * 16 * 16 + self.data[379]) / 1000)
            return self.s2, self.v2max, self.s2max

    def drop3(self):
        if self.s3:
            return self.s3, self.v3max, self.s3max
        else:
            for i in range(384, 504):
                self.s3.append(self.data[i]/200)
            self.v3max = float((self.data[504]*16*16 + self.data[505])/10000)
            self.s3max = float((self.data[506]*16*16 + self.data[507])/1000)
            return self.s3, self.v3max, self.s3max

    def plotdata(self):
        self.drop1()
        self.drop2()
        self.drop3()

        s1 = self.s1
        s2 = self.s2
        s3 = self.s3

        for i in range(len(s1)):
            s1[i] = s1[i] * (-1)

        for i in range(len(s2)):
            s2[i] = s2[i] * (-1)

        for i in range(len(s1)):
            s3[i] = s3[i] * (-1)

        step = numpy.arange(0, 24, 0.2)

        return s1, s2, s3, step

    def other(self):
        if self.evd:
            return self.average_s, self.evd, self.s_v
        elif self.s1max and self.s2max and self.s3max:
            self.average_s = round((self.s1max + self.s2max + self.s3max) / 3, 3)
            average_v = round((self.v1max + self.v2max + self.v3max) / 3, 3)
            self.s_v = round(self.average_s / average_v, 3)
            self.evd = round(22.5 / self.average_s, 3)
            return self.average_s, self.evd, self.s_v
        else:
            return "Nie można wyliczyć parametrów, najpierw wylicz drop1, drop2 i drop3"

    def generete_report(self):
        self.hammer()
        self.name()
        self.test()
        self.coordinates()
        self.drop1()
        self.drop2()
        self.drop3()
        self.other()

        report = ("Badanie: " + self.test_name +
                  "\nNumer seryjny młota: " + str(self.serial_number) +
                  "\nKalibracja tego młota została wykonana:" + str(self.calibration_day) +
                  "." + str(self.calibration_mounth) + "." + str(self.calibration_year) +
                  "\nBadanie zostało wykonane: "+ str(self.test_day) +"." + str(self.test_mounth) +"." + str(self.test_year) + "\t" +
                  str(self.test_hour) + ":" + str(self.test_minute) + ":" + str(self.test_secound) +
                  "\nWspołrzędne badania: " + self.latitude + "\t"+"\t"+ self.longitude)

        return report