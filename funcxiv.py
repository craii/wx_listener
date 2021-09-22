# - * - coding:utf-8 - * -
from datetime import datetime
import os
import uuid


def make_record_directory() -> str:
    current_session = datetime.now().strftime("%Y-%m-%d___%H-%M-%S")
    path = f"record_{current_session}"
    os.system(f"mkdir {path}")
    return path


def generate_sql(sender, time, msg, msg_type, src) -> str:
    return f'''insert into wxmsg (sender, uuid, time, msg, msgType, src) 
                           values ('{sender}', '{uuid.uuid1()}', '{time}', '{msg}', '{msg_type}', '{src}')'''

def msg_summary():
    return f'''SELECT  sender, count(1) as msg_sum FROM wxmsg GROUP BY sender ORDER BY msg_sum DESC'''

