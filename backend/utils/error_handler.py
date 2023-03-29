import sys, datetime
import traceback
from backend.config.config import get_config
config_app = get_config()
def error_handler(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log = time+'\n'+traceback.format_exc()
    error = str(e).replace(r"_", "-")
    error_type = str(exc_type).split("\'")[1] + ': ' + error
    # print(time)
    with open(config_app['log']['app'], 'a') as app_log:
        app_log.write(log)
    return error_type