from datetime import datetime
from backend.config.constant import MINUTES_RESTART_INPROCESS, MINUTES_RESTART_MULTIPRODUCT

def check_reset_state(time_start, time_latest, pre_tag):
    flag_restart = {
        "in_process": False,
        "end": False,
        "multiproduct": False
    }
    
    if pre_tag == "deal":
        flag_restart["end"] = True
    # ---------------------------------- #
    if time_latest and not flag_restart["end"]:
        time_latest = datetime.strptime(time_latest,"%Y-%m-%d %H:%M:%S")
        time_latest = datetime.timestamp(time_latest)
        time_start =  datetime.strptime(time_start,"%Y-%m-%d %H:%M:%S")
        time_start =  datetime.timestamp(time_start)
        if int(time_start-time_latest)/60 >MINUTES_RESTART_MULTIPRODUCT: #ask other product_name > 2' -> restart
            flag_restart["multiproduct"] = True

        if int(time_start-time_latest)/60>MINUTES_RESTART_INPROCESS : # >5p when in_processing -> restart
            flag_restart.update({"in_process":True, "multiproduct":False})
    return flag_restart