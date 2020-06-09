from sqlalchemy import create_engine, text
import config
import numpy as np
import datetime
import math

def create_db_engine(connection_param):
    username, password, db_ip,db_name = connection_param["USER"], connection_param["PASSWORD"], \
                                        connection_param["DB_IP"], connection_param["DB_NAME"]
    pool_size = connection_param["POOL_SIZE"]
    db_engine = create_engine('mysql+mysqldb://{0}:{1}@{2}/{3}'.format(username, password, db_ip, db_name),
                              pool_size=pool_size, pool_recycle=3600, encoding='utf-8', pool_timeout=10)
    return db_engine


connection_param = {
    "USER":config.MYSQL_USER,
    "PASSWORD":config.MYSQL_PASSWD,
    "DB_IP": config.MYSQL_HOST,
    "DB_NAME": config.MYSQL_DB_NAME,
    "POOL_SIZE":config.POOL_SIZE
}
db_engine = create_db_engine(connection_param)


def get_db_connection():
    db_conn = db_engine.connect()
    return db_conn


def release_db_connection(conn):
    conn.close()


def get_backgroud_temp_info(temp_file_path, pts):
    temp_matrix = np.load(temp_file_path)
    pts_len = len(pts)
    temp_list = []
    for (x,y) in pts:
        temp = temp_matrix[x,y]
        temp_list.append(temp)
    if temp_list:
        avg = np.average(temp_list)
        max = np.max(temp_list)
        min = np.min(temp_list)
        std = np.std(temp_list)
        med = np.median(temp_list)
    return

if __name__ == "__main__":
    conn = get_db_connection()

    sql = "select create_time from ir_data_0527_pm ORDER BY create_time"
    time_list = conn.execute(sql).fetchall()
    time_list_size = len(time_list)
    max_time = np.max(time_list)
    min_time = np.min(time_list)
    diff_sec = (max_time - min_time).seconds
    interval_sec = 3600
    max_index = math.ceil(diff_sec / interval_sec)
    for idx in range(max_index):
        start_time_delta = idx * interval_sec
        end_time_delta = (idx + 1) * interval_sec
        start_time = min_time + datetime.timedelta(seconds=start_time_delta)
        end_time = min_time + datetime.timedelta(seconds=end_time_delta)
        sql = "select tmp_img_file_name from ir_data_0527_pm where create_time > \'{0}\' and create_time <= \'{1}\'".format(start_time, end_time)
        temp_file_name = conn.execute(sql).fetchall()
        print(temp_file_name)

    release_db_connection(conn)

