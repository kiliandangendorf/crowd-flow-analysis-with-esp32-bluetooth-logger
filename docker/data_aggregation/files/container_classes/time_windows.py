from time import time
from typing import List
import util.time as time_kd
from container_classes.time_window import TimeWindow
from config import GENERAL_CFG
from db.store_meas import store_timewindow

FIRST_POSSIBLE_TS = GENERAL_CFG['FIRST_POSSIBLE_TS']
TIME_WINDOW_IN_MIN = GENERAL_CFG['TIME_WINDOW_IN_MIN']
MAX_TIME_WINDOW_IN_MEMORY = GENERAL_CFG['MAX_TIME_WINDOW_IN_MEMORY']
MAX_COUNT_IN_ORPHANS_TIME_WINDOW = 100
MAX_COUNT_IN_UNSYNCED_TIME_WINDOW = 100


class TimeWindows:
    def __init__(self):
        self.time_windows: List[TimeWindow] = []
        # Dummy timewindow to track too late arriving
        self.orphans: TimeWindow = TimeWindow(time_kd.timestamp_to_tz_aware(0), 0)
        # Dummy timewindow to track wrong meas from usynced devices
        self.unsynced: TimeWindow = TimeWindow(time_kd.timestamp_to_tz_aware(0), 0)
        # TODO: Do something with these dummy_tws

    def get_cur_timewindow(self, timestamp: int) -> TimeWindow:
        if len(self.unsynced) > MAX_COUNT_IN_UNSYNCED_TIME_WINDOW:
            # TODO: save to db and clear list
            pass
        if timestamp < FIRST_POSSIBLE_TS:
            print("Unsynced device with timestamp", timestamp)
            return self.unsynced

        system_timestamp = int(time())
        if timestamp > system_timestamp + 10:
            print("Unsynced device with timestamp", timestamp)
            return self.unsynced

        # Create first one if list is empty
        if len(self.time_windows) == 0:
            # TODO try to retrieve from db?
            print("Empty list, create first element.")
            start_time = time_kd.round_minutes_down(time_kd.timestamp_to_tz_aware(system_timestamp), TIME_WINDOW_IN_MIN)
            self.time_windows.append(TimeWindow(start_time, TIME_WINDOW_IN_MIN))

        # Remove old entries from memory (since they were written to db anyways)
        while len(self.time_windows) > MAX_TIME_WINDOW_IN_MEMORY:
            # Check if this is unchanged since last time writing it to db
            if self.time_windows[0].changed:
                print("Store updated timewindow", self.time_windows[0].time_from)
                store_timewindow(self.time_windows[0])
            del self.time_windows[0]

        # Select latest element in list
        cur_tw = self.time_windows[- 1]

        local_time = time_kd.timestamp_to_tz_aware(timestamp)

        # Return tw
        if cur_tw.time_is_within_this_window(local_time):
            return cur_tw

        # Not in cur_tw: lower?
        if local_time < cur_tw.time_from:
            # Running downwards through timewindows
            for i in range(len(self.time_windows) - 1)[::-1]:
                cur_tw_canditate = self.time_windows[i]
                if cur_tw_canditate.time_is_within_this_window(local_time):
                    # Found timewindow not containing this meas
                    print("Found timewindow for belated time")
                    self.time_windows[i].changed = True
                    return cur_tw_canditate
                # else (not in memory anymore) return orphans
                print("No timewindow for belated time was found, put to orphans")
            return self.orphans

        # Not in cur_tw: higher! New timewindow (save old one and create next one)
        print("Store timewindow", cur_tw.time_from)
        store_timewindow(cur_tw)
        next_tw = TimeWindow(time_from=cur_tw.time_to, window_size_in_minutes=TIME_WINDOW_IN_MIN)
        self.time_windows.append(next_tw)
        return next_tw

    def to_string(self, indent=0) -> str:
        prefix = " " * indent
        s = prefix + "time_windows: [\n"
        for win in self.time_windows:
            s += win.to_string(indent) + ",\n"
        s += prefix + "]\n"
        s += prefix + "size: " + str(len(self.time_windows))
        return s
