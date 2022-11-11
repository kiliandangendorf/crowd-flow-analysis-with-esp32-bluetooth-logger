import datetime as dt


class Meas:
    def __init__(self, meas_id: str, time: dt.datetime):
        self.id = meas_id
        self.time_in = time
        self.time_out = time

    def to_string(self, indent=0) -> str:
        prefix = " " * (indent * 3)
        s: str = prefix + "{" + "id: {}, in: {}, out: {}".format(
            self.id, self.time_in, self.time_out) + "},\n"
        return s


class BleMeas(Meas):
    def __init__(self, mac_hash: str, time: dt.datetime, manuf: str, is_cwa: bool, name: str, public_addr:bool):
        super().__init__(mac_hash, time)
        self.manuf = manuf
        self.is_cwa = is_cwa
        self.name = name
        self.public_addr=public_addr

    def to_string(self, indent=0) -> str:
        prefix = " " * (indent * 3)
        s: str = prefix + "{" + "mac_hash: {}, in: {}, out: {}, manuf: {}, is_cwa: {}, name: {}, public_addr: {}".format(
            self.id, self.time_in, str(self.time_out), self.manuf, self.is_cwa, self.name, self.public_addr) + "},\n"
        return s
