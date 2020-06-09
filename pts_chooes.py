from sqlalchemy import create_engine, text
import config
import numpy as np
import datetime
import math
import random
import re

invisible_w = 160
invisible_h = 120


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


def get_statis_info(list):
    sum = np.sum(list)
    avg = np.average(list)
    max = np.max(list)
    min = np.min(list)
    std = np.std(list)
    med = np.median(list)
    return sum, avg, max, min, std, med


def print_statis_info(title, list):
    sum, avg, max, min, std, med = get_statis_info(list)
    print("{6} statis : sum:{0:.2f}, avg:{1:.2f}, max:{2:.2f}, min:{3:.2f}, std:{4:.2f}, med:{5:.2f}"
          .format(sum, avg, max, min, std, med, title))


def random_pts(w, h, pts_size):
    pts = []
    for i in range(pts_size):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        pts.append((x,y))
    return pts


def print_random_ten_img(img_list):
    list_len = len(img_list)
    if list_len == 0:
        return

    max = 10
    if list_len < 10:
        max = list_len
    for i in range(max):
        idx = random.randint(0, list_len - 1)
        print(img_list[idx])



if __name__ == "__main__":
    conn = get_db_connection()

    skip = 10
    pts_len = 16
    test_len = 64
    chooes_map = {}
    table_name = "ir_data_0525"

    for test_idx in range(test_len):

        # random pts
        pts = random_pts(invisible_w, invisible_h, pts_len)

        unvisble_file_paths = []


        sql = "select create_time from " + table_name + " ORDER BY create_time"
        time_list = conn.execute(sql).fetchall()
        time_list_size = len(time_list)
        max_time = np.max(time_list)
        min_time = np.min(time_list)
        diff_sec = (max_time - min_time).seconds
        interval_sec = 3600 * 24
        max_index = math.ceil(diff_sec / interval_sec)
        sums = []
        avgs = []
        maxs = []
        mins = []
        stds = []
        meds = []
        for idx in range(max_index):
            start_time_delta = idx * interval_sec
            end_time_delta = (idx + 1) * interval_sec
            start_time = min_time + datetime.timedelta(seconds=start_time_delta)
            end_time = min_time + datetime.timedelta(seconds=end_time_delta)
            sql = "select black_set_temp, black_real_temp, unvisible_img_file_name, tmp_img_file_name " \
                  "from " + table_name + " where create_time > \'{0}\' and create_time <= \'{1}\'".format(start_time, end_time)
            temp_file_name = conn.execute(sql).fetchall()
            count = 0
            for (black_set_temp, black_real_temp, unvisble_file_path, tmp_file_path) in temp_file_name:
                count = count + 1
                if count % skip != 0:
                    continue

                sum, avg, max, min, std, med = get_backgroud_temp_info(tmp_file_path, pts, black_set_temp, black_real_temp)
                sums.append(sum)
                avgs.append(avg)
                maxs.append(max)
                mins.append(min)
                stds.append(std)
                meds.append(med)
                unvisble_file_paths.append(unvisble_file_path)
            print("{0} - {1}".format(start_time + datetime.timedelta(hours=8), end_time + datetime.timedelta(hours=8)))
            print_statis_info("sums", sums)
            print_statis_info("avgs", avgs)
            print_statis_info("maxs", maxs)
            print_statis_info("mins", mins)
            print_statis_info("stds", stds)
            print_statis_info("meds", meds)
            print("pts:", pts)
            print_random_ten_img(unvisble_file_paths)

            sum, avg, max, min, std, med = get_statis_info(avgs)
            chooes_map[std] = (avg, max, min, std, med, pts)
            print("======================================")

    print(chooes_map)
    print(sorted(chooes_map))
    release_db_connection(conn)

