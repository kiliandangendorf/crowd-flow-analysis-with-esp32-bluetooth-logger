import datetime as dt
from typing import List

from container_classes.station import Station

from container_classes.meas import BleMeas
from util.time import add_minutes_to_time


class TimeWindow:
    def __init__(self, time_from:dt.datetime, window_size_in_minutes:int):
        # incl.
        self.time_from=time_from
        # excl.
        self.time_to=add_minutes_to_time(time_from,window_size_in_minutes)
        self.window_size_in_minutes=window_size_in_minutes
        self.stations:List[Station]=[]

        self.changed=False

    def time_is_within_this_window(self, time:dt.datetime)->bool:
        return self.time_from <= time < self.time_to

    def station_contains_meas(self, station_id:str, mac_hash:str, time:dt.datetime)->bool:
        # is station in stations?
        for station in self.stations:
            if station.id==station_id:
                break
        else:
            # if not found in list create new one
            station=Station(station_id)
            # and add to list
            self.stations.append(station)
        return station.contains_id(mac_hash, time)

    def add_meas(self, station_id:str, mac_hash:str, time:dt.datetime, manuf:str, is_cwa:bool, name:str, public_addr:bool):
        station:Station=self._find_station(station_id)
        meas: BleMeas = BleMeas(mac_hash, time, manuf, is_cwa, name, public_addr)
        station.meas.append(meas)

    def to_string(self, indent=0)->str:
        prefix=" "*indent
        s:str=prefix+"{from: "+str(self.time_from)+", to: "+str(self.time_to)+", window_size: "+str(self.window_size_in_minutes)+", "
        s+=prefix+"stations: [\n"
        for station in self.stations:
            s+=station.to_string(indent)
        s+=prefix+"]}"
        return s

    def _find_station(self, station_id:str)->Station:
        for station in self.stations:
            if station.id==station_id:
                return station
        # station was created in station_contains_meas
        return None