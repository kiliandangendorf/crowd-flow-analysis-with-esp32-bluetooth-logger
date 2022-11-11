from typing import List
import datetime as dt
from container_classes.meas import Meas


class Station:
    def __init__(self, station_id: str):
        self.id = station_id
        self.meas: List[Meas] = []

    def contains_id(self, id: str, time: dt.datetime) -> bool:
        for m in self.meas:
            if m.id == id:
                # update out timestamp with latest one
                m.time_out = time
                return True
        else:
            return False

    def to_string(self, indent=0) -> str:
        prefix = " " * indent * 2
        s: str = prefix + "{id: " + self.id
        s += ", meas: [\n"
        for m in self.meas:
            s += m.to_string(indent)
        s += prefix + "]},\n"
        return s
