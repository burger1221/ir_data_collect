import queue
import numpy as np
import random
from sqlalchemy import create_engine, text
import config
import math
import copy

TEMP_QUEUE_SIZE = 1000
temp_queue = queue.Queue(TEMP_QUEUE_SIZE)
temp_list = []

def get_threshold(t_be):
    t_th = 35.24 + 0.2657368 * (t_be - 30) + 0.6
    return t_th


def judge_is_fever(t_sur, t_be, box_id):
    '''
    judge a person is fever by his/her surface temperature
    :param t_sur: surface temperature
    :type t_sur: float
    :param t_be: the temperature of the edge of black
    :type t_be: float
    :returns: is not fever, description, queue size , temperature index in queue
    :rtype: truple
    '''
    t_th = get_threshold(t_be)
    if t_sur > t_th + 0.6:
        return False, "direct fever", temp_queue.qsize(), None
    else:
        # 加队列
        obj = {
            "box_id": box_id,
            "t_sur": t_sur
        }
        if len(temp_list) >= config.TEMP_QUEUE_SIZE:
            del temp_list[0]
        flag = 0
        for item in temp_list:
            if item['box_id'] == box_id:
                flag = 1
                if item['t_sur'] < t_sur:
                    item['t_sur'] = t_sur
                    flag = 2
                break
            else:
                continue

        # had saved , do nothing
        if flag == 1:
            return True, None, None, None

        if flag == 0:
            temp_list.append(obj)

        # judge fever person by his/her position of temperature in queue
        if t_sur > t_th - 0.6:
            # if queue size < 100 return not fever
            if(len(temp_list) < 100):
                return True, None, None, None
            else:
                sort_list = copy.copy(temp_list)
                sort_list.sort(key=lambda k: (k.get('t_sur', 0)))
                sort_list = sort_list[::-1]
                temp_idx = -1
                for item in sort_list:
                    temp_idx = temp_idx + 1
                    if item['box_id'] == box_id:
                        temp_idx = temp_idx + 1
                        # temp_idx = list.index(item)
                        break
                if(temp_idx <= math.ceil(len(temp_list) * 0.0054)):
                    return False, "in top queue", len(temp_list), temp_idx
                else:
                    return True, None, None, None
        else:
            return True, None, None, None


# create db connection
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


def get_backgroud_temp_info(temp_file_path, pts, black_set_temp, black_real_temp):
    diff_temp = black_set_temp - black_real_temp
    temp_matrix = np.load(temp_file_path)
    pts_len = len(pts)
    temp_list = []
    for (x,y) in pts:
        temp = temp_matrix[y, x]
        temp = diff_temp + temp
        temp_list.append(temp)
    if temp_list:
        sum = np.sum(temp_list)
        avg = np.average(temp_list)
        max = np.max(temp_list)
        min = np.min(temp_list)
        std = np.std(temp_list)
        med = np.median(temp_list)
        return sum, avg, max, min, std, med
    return None


if __name__ == "__main__":
    id_list = []
    box_ids = []
    count =  0
    conn = get_db_connection()
    pts = [(19, 97)]
    table_name = "ir_data_0526"
    sql = "select id, box_id, in_temp, evn_temp, wind_speed, humidity, sur_t_o, black_set_temp, black_real_temp, unvisible_img_file_name, visible_img_file_name, tmp_img_file_name " \
          "from " + table_name + " order by create_time asc "
    time_list = conn.execute(sql).fetchall()
    for (id , box_id, in_temp, evn_temp, wind_speed, humidity, sur_t_o, black_set_temp, black_real_temp, unvisble_file_path, visible_file_path, tmp_file_path) in time_list:
        sum, avg, max, min, std, med = get_backgroud_temp_info(tmp_file_path, pts, black_set_temp, black_real_temp)
        if id == 6505:
            print()
        is_not_fever, ret, queue_size, queue_idx = judge_is_fever(sur_t_o, avg, box_id)
        if not is_not_fever:
            if box_id not in box_ids:
                box_ids.append(box_id)
            count = count + 1
            id_list.append(id)
            # print("sur_temp:", sur_t_o, "black_edge_temp:",
            #       avg, "result", judge_is_fever(sur_t_o, avg),
            #       "unvisible_img_file_name", unvisble_file_path,
            #       "ret", ret,
            #       "queue_size", queue_size,
            #       "queue_idx", queue_idx)
            print("cp {0} /tmp/test_v/".format(unvisble_file_path))

    print("total", count)
    print(id_list)
    print(len(id_list))
    print(box_ids)
    print(len(box_ids))
