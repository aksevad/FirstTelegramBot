"""
class for a math model of a RoboDog Epsilon2
"""

from math import floor, sin, asin, cos, pi, tan, atan2, fabs, atan, sqrt
import datetime


class SatelliteAntenna:
    __year = 1975
    __month = 2
    __day = 2
    __hour = 0
    __min = 0
    __zone = 0

    __antenna_latitude = 66.000
    __antenna_longitude = -66.000
    __antenna_offset = 17

    __sat_longitude = 0
    __azimuth = 0
    __vertical = 0

    __process_step = 1
    __language = "ENG"

    def __init__(self, language="ENG"):
        self.set_now()
        self.__language=language

    def get_azimuth(self):
        return self.__azimuth

    def get_vertical(self):
        return self.__vertical

    def set_antenna_offset(self, offset):
        __antenna_offset = offset

    def set_antenna_offset_str(self, offset):
        offset = offset.lower().replace(" ", "")
        try:
            antenna_offset = float(offset)
        except Exception:
            return False
        if 0 <= antenna_offset <= 90:
            self.__antenna_offset = antenna_offset
        else:
            return False
        return True

    def get_process_step(self):
        return self.__process_step

    def set_process_step(self, step):
        self.__process_step = step

    def get_language(self):
        return self.__language

    def set_language(self, language):
        self.__language = language

    def get_sat_longitude(self):
        return self.__sat_longitude

    def set_sat_longitude(self, sat_longitude_str):
        sat_longitude_str = sat_longitude_str.lower().replace(" ", "").replace("w", "")
        if 'e' in sat_longitude_str:
            # Convert East to -
            sat_longitude_str = '-' + sat_longitude_str.replace("e", "")
        try:
            sat_longitude = int(float(sat_longitude_str).__round__(0))
        except Exception:
            return False
        if -180 <= sat_longitude <= 180:
            self.__sat_longitude = sat_longitude
        else:
            return False
        return True

    def set_now(self):
        today = datetime.datetime.utcnow()
        this_year = today.year
        if (this_year <= 1900):
            this_year = this_year + 1900  # for Netscape on Mac

        self.__year = this_year
        self.__month = today.month
        self.__day = today.day
        self.__hour = today.hour
        self.__min = today.minute
        self.__zone = 0

    def set_user_day(self, this_month, this_day, this_hour, this_minute, this_zone):
        self.__year = 1975
        self.__month = this_month
        self.__day = this_day
        self.__hour = this_hour
        self.__min = this_minute
        self.__zone = this_zone

    def set_timezone(self, antenna_coords_str):
        # папдалово с конвертацией пояса
        self.__timezone = -5
        return True

    def ut(self, h, m, z):
        return h - z + m / 60

    def jd(self, y, m, d, u):
        return (367 * y) - floor((7 / 4) * (floor((m + 9) / 12) + y)) + floor(275 * m / 9) + d - 730531.5 + (u / 24)

    def azimuth(self, ho, mi, zo):
        uu = self.ut(ho, mi, zo)
        jj = self.jd(self.__year, self.__month, self.__day, uu)
        T = jj / 36525
        k = pi / 180.0
        M = 357.5291 + 35999.0503 * T - 0.0001559 * T * T - 0.00000045 * T * T * T
        M = M % 360
        Lo = 280.46645 + 36000.76983 * T + 0.0003032 * T * T
        Lo = Lo % 360
        DL = (1.9146 - 0.004817 * T - 0.000014 * T * T) * sin(k * M) + (0.019993 - 0.000101 * T) * sin(
            k * 2 * M) + 0.00029 * sin(k * 3 * M)
        L = Lo + DL
        eps = 23.43999 - 0.013 * T
        delta = (1 / k) * asin(sin(L * k) * sin(eps * k))
        RA = (1 / k) * atan2(cos(eps * k) * sin(L * k), cos(L * k))
        RA = (RA + 360) % 360
        GMST = 280.46061837 + 360.98564736629 * jj + 0.000387933 * T * T - T * T * T / 38710000
        GMST = (GMST + 360) % 360
        LMST = GMST + self.__antenna_longitude
        H = LMST - RA
        eqt = (Lo - RA) * 4
        azm = (1 / k) * atan2(-sin(H * k), cos(self.__antenna_latitude * k) * tan(delta * k) - sin(
            self.__antenna_latitude * k) * cos(H * k))
        azm = (azm + 360) % 360
        return azm

    def altitude(self, ho, mi, zo):
        uu = self.ut(ho, mi, zo)
        jj = self.jd(self.__year, self.__month, self.__day, uu)
        T = jj / 36525
        k = pi / 180.0
        M = 357.5291 + 35999.0503 * T - 0.0001559 * T * T - 0.00000045 * T * T * T
        M = M % 360
        Lo = 280.46645 + 36000.76983 * T + 0.0003032 * T * T
        Lo = Lo % 360
        DL = (1.9146 - 0.004817 * T - 0.000014 * T * T) * sin(k * M) + (0.019993 - 0.000101 * T) * sin(
            k * 2 * M) + 0.00029 * sin(k * 3 * M)
        L = Lo + DL
        eps = 23.43999 - 0.013 * T
        delta = (1 / k) * asin(sin(L * k) * sin(eps * k))
        RA = (1 / k) * atan2(cos(eps * k) * sin(L * k), cos(L * k))
        RA = (RA + 360) % 360
        GMST = 280.46061837 + 360.98564736629 * jj + 0.000387933 * T * T - T * T * T / 38710000
        GMST = (GMST + 360) % 360
        LMST = GMST + self.__antenna_longitude
        H = LMST - RA
        eqt = (Lo - RA) * 4
        alt = (1 / k) * asin(
            sin(self.__antenna_latitude * k) * sin(delta * k) + cos(self.__antenna_latitude * k) * cos(delta * k) * cos(
                H * k))
        return alt

    def set_antenna_coordinates(self, latitude, longitude, north_south="North", west_east="East", latitude_minutes=0,
                                longitude_minutes=0):
        self.__antenna_latitude = (latitude + latitude_minutes / 60) * (1 if north_south == "North" else -1)
        self.__antenna_longitude = (longitude + longitude_minutes / 60) * (1 if west_east == "East" else -1)
        return True

    def set_antenna_coordinates_str(self, antenna_coords_str):
        # попадалово с конвертацией координат from string

        antenna_coords_str = antenna_coords_str.lower().replace(" ", "").replace("e", "").replace("n", "") \
            .replace(",", ".")
        coords = antenna_coords_str.split(";", 1)
        north_south = "n"
        east_west = 'e'
        if 's' in coords[0]:
            # Convert South to -
            north_south = "s"
            # coords[0] = '-' + coords[0].replace("s", "")
        if 'w' in coords[1]:
            # Convert west to -
            east_west = 'w'
            # coords[1] = '-' + coords[1].replace("w", "")
        try:
            latitude = float(coords[0])
            if north_south == 's':
                latitude = -latitude
            longitude = -float(coords[1])
            if east_west == 'w':
                longitude = -longitude

        except Exception:
            return False

        if -180 <= longitude <= 180 and -90 <= latitude <= 90:
            self.__antenna_latitude = latitude
            self.__antenna_longitude = longitude
        else:
            return False
        print("la=" + latitude.__str__() + ";lo=" + longitude.__str__())
        return True

    def sunpos(self, twilightr):
        ho = 1.0 * self.__hour
        mi = 1.0 * self.__min
        zo = 1.0 * self.__zone
        twr = 1.0 * twilightr

        k = pi / 180.0
        lgo = self.__antenna_longitude
        lao = self.__antenna_latitude
        aa = 180.0

        b = self.__antenna_longitude * k
        a = self.__antenna_latitude * k
        c = -self.__sat_longitude * k
        scaz = (pi * 1.0 + atan(tan(b - c) / sin(a))) / k
        rverang = atan((cos(b - c) * cos(a) - 0.15126) / sqrt(1 - cos(b - c) * cos(b - c) * cos(a) * cos(a))) / k

        if (self.__antenna_latitude < 0):
            aa = 0.0

        alt = self.altitude(ho, mi, zo)
        azm = self.azimuth(ho, mi, zo)

        h1 = 0
        m = 0
        alt1 = self.altitude(h1, m, zo)
        azm1 = self.azimuth(h1, m, zo)
        s = -0.8333

        # find midday interval

        h = 0
        while h < 24:
            h2 = h
            azm2 = self.azimuth(h2, m, zo)
            if ((azm1 <= 180) and (azm2 >= 180)):
                ha1 = h1
                ha2 = h2
            h1 = h2
            azm1 = azm2
            h = h + 1

        # find exact midday time
        mino = 1.0

        h = ha1
        while h < ha2:
            m = 0
            while m < 60:
                azmo = self.azimuth(h, m, zo)
                dfo = fabs(aa - azmo)
                if (dfo <= mino):
                    mino = dfo
                    hno = h
                    mno = m
                m = m + 1
            h = h + 1

        mday = ""

        altnoon = self.altitude(hno, mno, zo)
        if (altnoon < s):
            mday = "nigth"

        hr = "не происходят"
        mr = ""
        hs = "не происходят"
        ms = ""
        htwr = "не происходят"
        mtwr = ""
        htws = "не происходят"
        mtws = ""

        mintwr = 0.1
        minr = 0.1

        h = 0
        while h <= hno:
            m = 0
            while m < 60:
                if (60 * h + m < 60 * hno + mno):
                    altr = self.altitude(h, m, zo)

                    dftwr = fabs(twr - altr)
                    if (dftwr <= mintwr):
                        mintwr = dftwr
                        htwr = h
                        mtwr = m
                    if (altnoon > s):
                        dfr = fabs(s - altr)
                        if (dfr <= minr):
                            minr = dfr
                            hr = h
                            mr = m
                m = m + 1
            h = h + 1

        mins = 0.1
        mintws = 0.1

        h = hno
        while h < 24:
            m = 0
            while m < 60:
                if (60 * h + m >= 60 * hno + mno):
                    alts = self.altitude(h, m, zo)

                    if (altnoon > s):
                        dfs = fabs(s - alts)
                        if (dfs <= mins):
                            mins = dfs
                            hs = h
                            ms = m

                    dftws = fabs(twr - alts)
                    if (dftws <= mintws):
                        mintws = dftws
                        htws = h
                        mtws = m
                m = m + 1
            h = h + 1

        result = ['True']
        cikti = ""
        if (self.__month <= 9):
            cikti = cikti + "Дата: " + self.__day.__str__() + ".0" + self.__month.__str__() + "." + self.__year.__str__() + ", " + ho.__str__() + " hr :" + mi.__str__() + " min, " + zo.__str__() + "hr GMT \r"
        else:
            cikti = cikti + "Дата: " + self.__day + "." + self.__month + "." + self.__year + ", " + ho + " hr :" + mi + " min, " + zo + "hr GMT \r"
        result.append(cikti)
        cikti = "Место: " + str(round(lao, 3)) + "° " + ("N" if self.__antenna_latitude > 0 else "S") + ",  " + \
                str(round(lgo, 3)) + "° " + ("W" if self.__antenna_longitude < 0 else "E") + "\r"
        result.append(cikti)
        cikti = "Азимут спутника:\t" + str(round(scaz, 3)) + "°" + "\r";
        result.append(cikti)
        cikti = "Угол места истиный:\t" + str(round(rverang, 3)) + "°" + "\r"
        rverang = rverang - fabs(self.__antenna_offset)
        result.append(cikti)
        cikti = "Угол места актуальный:\t" + str(round(rverang, 3)) + "°" + "\r"
        result.append(cikti)
        cikti = "Азимут солнца:\t" + str(round(azm, 1)) + "°"
        result.append(cikti)
        # result = cikti

        print("Finish")
        return result

# def main():
#     print("start")
#     ant = SatelliteAntenna()
#
#     ant.setnow()
#
#     latitude = 63
#     latmin = 18
#     ns = "North"  # North or south
#
#     longitude = 75  # longitude grads
#     longmin = 32  # longitude minutes
#     ew = "East"  # East or West
#     ant.set_antenna_coordinates_str("63,3N;75.53E")
#     #ant.set_antenna_coordinates(latitude, longitude, ns, ew, latmin, longmin)
#     spacecraft = 66  # satelitte longitude
#     ant.set_sat_longitude("-66")
#     ofangle = 17  # ofset angel of antenna
#     twilightr = -7
#     ant.set_antenna_offset(ofangle)
#     ant.sunpos(twilightr)  # main algorithm in it
#
#
# main()


# def set_axes(self, pelvic_x, pelvic_y, shoulder_x, shoulder_y):
#     self.__shoulder_axis_y = shoulder_y
#     self.__shoulder_axis_x = shoulder_x
#     self.__pelvic_axis_x = pelvic_x
#     self.__pelvic_axis_y = pelvic_y
# bot.send_message(message.chat.id, "Lonitude is " + sat_longitude.__str__(), parse_mode='HTML')
