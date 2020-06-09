import random
import base64
import numpy as np
import cv2
import pymysql.cursors
import struct
import config
import queue
import math


class IrDataResolver:

    temp_queue = queue.Queue(maxsize=config.TEMP_QUEUE_SIZE)


    INSERT_SQL = "INSERT INTO `ir`.`" + config.MYSQL_TABLE_NAME + "` (`box_id`,`visible_img_file_name`," \
                "`unvisible_img_file_name`," \
                "`tmp_img_file_name`,`vx1`,`vx2`,`vy1`,`vy2`,`x1`,`x2`,`y1`,`y2`,`ir_temp_surf`,`black_set_temp`," \
                "`black_real_temp`, `in_temp`, `sur_t_o`, `is_only_collect`," \
                "avg, max, min, std, var, med, temp_idx, queue_len, " \
                "temp_idx_5, temp_idx_10, temp_idx_15, temp_idx_20, temp_idx_25, temp_idx_30," \
                " temp_idx_35, temp_idx_40, temp_idx_45, temp_idx_50) " \
                "VALUES ('{0}','{1}','{2}','{3}',{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}," \
                "{18},{19},{20},{21},{22},{23},{24},{25},{26}," \
                "{27},{28},{29},{30},{31},{32},{33},{34},{35});"



    UPDATE_SQL = "UPDATE `ir`.`ir_data` " \
                 "SET evn_temp = {0}, wind_speed = {1}, humidity = {2}, lux = {3}, ir_cem_surf = {4}, " \
                 "ir_o1_surf = {5}, ir_o2_surf = {6}, distance = {8}, duration = {9}, is_umbrella = {10}, " \
                 "is_hat = {11}, sweat = {12}, vehicle = {13}, description = '{14}'" \
                 "WHERE `box_id` = {7}"

    FINAL_UPDATE_SQL = "UPDATE `ir`.`"  + config.MYSQL_TABLE_NAME +  "` SET core_temp = {0}, " \
                "after_ir_cem_surf = {2}, over_ir_ret_bac = {3}, over_ir_ret_hair = {4}, over_ir_ret_black_pos = {5}, " \
                "over_ir_ret_black_temp = {6}, face_ret_shift = {7}, face_ret_hight_temp_shift = {8}, " \
                "face_ret_error = {9}, description = '{10}'" \
                "WHERE box_id = {1}"

    SELECT_BOX_ID_BY_USER_ID = "SELECT id, box_id, visible_img_file_name, unvisible_img_file_name " \
                               "from {0} where box_id % 4 = {1} and face_ret_is_check = 0 OR face_ret_is_check IS NULL"

    FACE_CHECK_UPDATE_SQL = "UPDATE {0} SET face_ret_shift = {1}, face_ret_hight_temp_shift = {2}, " \
                            "face_ret_error = {3} , face_ret_is_check = 1 WHERE id = {4}"

    def __init__(self, db_user, db_passwd, db_host='localhost', db_port=3306, db_name='ir'):
        self.connection = pymysql.connect(host=db_host,
                                     user=db_user,
                                     password=db_passwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        self.init_queue()

    def init_queue(self):
        sql = "select ir_temp_surf from  " + config.MYSQL_TABLE_NAME + " ORDER BY create_time desc limit 1000"

        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
        ret = cursor.fetchall()
        for i in range(len(ret)):
            self.temp_queue.put(ret[i]['ir_temp_surf'])
        print()

    def add_queue(self, ir_tem_surf):
        if len(self.temp_queue.queue) >= config.TEMP_QUEUE_SIZE:
            self.temp_queue.get()
            self.temp_queue.task_done()
        self.temp_queue.put(ir_tem_surf)
        avg = np.average(self.temp_queue.queue)
        max = np.max(self.temp_queue.queue)
        min = np.min(self.temp_queue.queue)
        std = np.std(self.temp_queue.queue)
        var = np.var(self.temp_queue.queue)
        med = np.median(self.temp_queue.queue)

        queue_len = len(self.temp_queue.queue)
        temp_idx_5 =  0
        temp_idx_10 = 0
        temp_idx_15 = 0
        temp_idx_20 = 0
        temp_idx_25 = 0
        temp_idx_30 = 0
        temp_idx_35 = 0
        temp_idx_40 = 0
        temp_idx_45 = 0
        temp_idx_50 = 0
        sort_list = np.sort(self.temp_queue.queue)[::-1]
        if queue_len != 0 :
            per_5_idx = math.floor(queue_len * 0.05)
            per_10_idx = math.floor(queue_len * 0.1)
            per_15_idx = math.floor(queue_len * 0.15)
            per_20_idx = math.floor(queue_len * 0.20)
            per_25_idx = math.floor(queue_len * 0.25)
            per_30_idx = math.floor(queue_len * 0.30)
            per_35_idx = math.floor(queue_len * 0.35)
            per_40_idx = math.floor(queue_len * 0.40)
            per_45_idx = math.floor(queue_len * 0.45)
            per_50_idx = math.floor(queue_len * 0.50)
            temp_idx_5 = sort_list[per_5_idx]
            temp_idx_10 = sort_list[per_10_idx]
            temp_idx_15 = sort_list[per_15_idx]
            temp_idx_20 = sort_list[per_20_idx]
            temp_idx_25 = sort_list[per_25_idx]
            temp_idx_30 = sort_list[per_30_idx]
            temp_idx_35 = sort_list[per_35_idx]
            temp_idx_40 = sort_list[per_40_idx]
            temp_idx_45 = sort_list[per_45_idx]
            temp_idx_50 = sort_list[per_50_idx]

        temp_idx = np.argwhere(sort_list == ir_tem_surf)[0][0]
        temp_idx = int(temp_idx)
        return avg, max, min, std, var, med, temp_idx, queue_len, temp_idx_5, temp_idx_10, temp_idx_15,\
               temp_idx_20, temp_idx_25, temp_idx_30, temp_idx_35, temp_idx_40, temp_idx_45, temp_idx_50


    def insert_ir_data(self, ir_dict, is_only_collect):
        sql = self.INSERT_SQL.format(ir_dict['box_id'], ir_dict['visible_img_file_name'], ir_dict['unvisible_img_file_name'],
                                    ir_dict['tmp_img_file_name'], ir_dict['vx1'], ir_dict['vx2'], ir_dict['vy1'],
                                    ir_dict['vy2'], ir_dict['x1'], ir_dict['x2'], ir_dict['y1'], ir_dict['y2'],
                                    ir_dict['sur_t'], ir_dict['bla_s'], ir_dict['bla_o'], ir_dict['in_temp'],
                                    ir_dict['sur_t_o'], is_only_collect, ir_dict["avg"], ir_dict["max"], ir_dict["min"],
                                    ir_dict["std"], ir_dict["var"], ir_dict["med"], ir_dict["temp_idx"],
                                    ir_dict["queue_len"],ir_dict["temp_idx_5"],ir_dict["temp_idx_10"],
                                    ir_dict["temp_idx_15"],ir_dict["temp_idx_20"],ir_dict["temp_idx_25"],
                                    ir_dict["temp_idx_30"],ir_dict["temp_idx_35"],ir_dict["temp_idx_40"],
                                    ir_dict["temp_idx_45"],ir_dict["temp_idx_50"])

        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
        self.connection.commit()

    def update_ir_data(self, update_dict):
        sql = self.UPDATE_SQL.format(update_dict['env_temp'], update_dict['wind_speed'],
                                     update_dict['humidity'], update_dict['light'], update_dict['cem'] ,
                                     update_dict['o1'], update_dict['o2'], update_dict['box_id'],
                                     update_dict['distance'], update_dict['duration'], update_dict['is_umbrella'],
                                     update_dict['is_hat'], update_dict['sweat'], update_dict['vehicle'],
                                     update_dict['description'])

        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
        self.connection.commit()

    def final_update_ir_data(self, update_dict):
        sql = self.FINAL_UPDATE_SQL.format(update_dict['mercury'], update_dict['box_id'],
            update_dict['after_ir_cem_surf'], update_dict['over_ir_ret_bac'],
            update_dict['over_ir_ret_hair'], update_dict['over_ir_ret_black_pos'], update_dict['over_ir_ret_black_temp'],
            update_dict['face_ret_shift'], update_dict['face_ret_hight_temp_shift'], update_dict['face_ret_error'],
            update_dict['description'])

        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
        self.connection.commit()

    @staticmethod
    def generate_file_name(box_id, is_visible, random_id):
        if is_visible == 'v':
            prefix = "images/visible_"
            suffix = ".jpg"
        elif is_visible == 'u':
            prefix = "images/unvisible_"
            suffix = ".jpg"
        elif is_visible == 't':
            prefix = "npy/temp_"
            suffix = ".npy"
        else:
            prefix = "images/other_"
            suffix = ""
        return prefix + str(box_id) + '_' + str(random_id) + suffix

    def save_matrix_2_file(self, ir_data_dto):
        random_id = random.randint(0, 1000)
        box_id = ir_data_dto['box_id']
        v_img_byte = base64.b64decode(ir_data_dto['v_img'])
        vx1 = ir_data_dto['vx1']
        vx2 = ir_data_dto['vx2']
        vy1 = ir_data_dto['vy1']
        vy2 = ir_data_dto['vy2']
        vw = vx2 - vx1
        vh = vy2 - vy1
        v_img_array = np.array(list(v_img_byte), dtype=np.uint8).reshape((vw, vh, 3), order='F')
        v_img_array = np.rot90(v_img_array, k=-1)
        v_img_array = v_img_array[..., ::-1]
        visible_img_file_name = self.generate_file_name(box_id, 'v', random_id)
        cv2.imwrite(visible_img_file_name, v_img_array)

        uv_img_byte = base64.b64decode(ir_data_dto['uv_img'])

        x1 = ir_data_dto['x1']
        x2 = ir_data_dto['x2']
        y1 = ir_data_dto['y1']
        y2 = ir_data_dto['y2']
        w = 120
        h = 160
        uv_img_array = np.array(list(uv_img_byte), dtype=np.uint8).reshape((w, h))
        cv2.rectangle(uv_img_array, (x1, y1), (x2, y2), (0, 0, 255), 1)
        unvisible_img_file_name = self.generate_file_name(box_id, 'u', random_id)
        cv2.imwrite(unvisible_img_file_name, uv_img_array)

        temp_metrix_byte = base64.b64decode(ir_data_dto['temp_data'])
        w = 120
        h = 160

        temp_ret = np.zeros((w, h))
        temp_array = np.array(list(temp_metrix_byte), dtype=np.int8).reshape((w, h, 4))
        tmp_img_file_name = self.generate_file_name(box_id, 't', random_id)
        for i in range(w):
            for j in range(h):
                temp_ret[i,j] = struct.unpack('<f', struct.pack('4b', *temp_array[i,j]))[0]
        np.save(tmp_img_file_name, temp_ret)

        return visible_img_file_name, unvisible_img_file_name, tmp_img_file_name

    def convert_2_core_temp(self, t):
        if t < 30:
            ret = t
        elif 30 <= t < 32:
            ret = t + 4
        elif 32 <= t <= 36.5:
            a = (t - 32) / (36.5 - 32)
            ret = 36 + a * (37 - 36)
        elif 36.5 < t < 39.5:
            ret = t + 0.5
        else:
            ret = t

        if 29 < ret < 35.7:
            b = (ret - 29) / (35.7 - 29)
            ret = 35.7 + b * (36 - 35.7)
        return ret

    # 解析热成像数据采集mqtt消息
    def ir_data_resolve(self, ir_data, is_only_collect):
        ret = {}
        print("ir_data_resolve start")
        ret['box_id'] = ir_data['box_id']
        ret['vx1'] = ir_data['vx1']
        ret['vx2'] = ir_data['vx2']
        ret['vy1'] = ir_data['vy1']
        ret['vy2'] = ir_data['vy2']
        ret['x1'] = ir_data['x1']
        ret['x2'] = ir_data['x2']
        ret['y1'] = ir_data['y1']
        ret['y2'] = ir_data['y2']

        bla_o = ir_data['bla_o']
        bla_s = ir_data['bla_s']
        sur_t = ir_data['sur_t']
        ret['bla_o'] = bla_o
        ret['bla_s'] = bla_s
        ret['sur_t'] = sur_t
        ret['in_temp'] = ir_data['in_temp']
        # 解析图片文件&解析温度矩阵
        visible_img_file_name, unvisible_img_file_name, tmp_img_file_name = self.save_matrix_2_file(ir_data)
        ret['visible_img_file_name'] = visible_img_file_name
        ret['unvisible_img_file_name'] = unvisible_img_file_name
        ret['tmp_img_file_name'] = tmp_img_file_name

        # 计算体表修正温度
        sur_t_o  = bla_s - bla_o + sur_t
        ret["sur_t_o"] = sur_t_o
        sur_t_2_core = self.convert_2_core_temp(sur_t_o)
        ret["sur_t_2_core"] = sur_t_2_core

        # 计算最近1000条记录的温度统计
        if not is_only_collect:
            avg, max, min, std, var, med, temp_idx, queue_len, temp_idx_5, temp_idx_10, temp_idx_15, temp_idx_20, \
            temp_idx_25, temp_idx_30, temp_idx_35, temp_idx_40, temp_idx_45, temp_idx_50 = self.add_queue(sur_t_o)
            ret["avg"] = avg
            ret["max"] = max
            ret["min"] = min
            ret["std"] = std
            ret["var"] = var
            ret["med"] = med
            ret["temp_idx"] = temp_idx
            ret["queue_len"] = queue_len
            ret["temp_idx_5"] = temp_idx_5
            ret["temp_idx_10"] = temp_idx_10
            ret["temp_idx_15"] = temp_idx_15
            ret["temp_idx_20"] = temp_idx_20
            ret["temp_idx_25"] = temp_idx_25
            ret["temp_idx_30"] = temp_idx_30
            ret["temp_idx_35"] = temp_idx_35
            ret["temp_idx_40"] = temp_idx_40
            ret["temp_idx_45"] = temp_idx_45
            ret["temp_idx_50"] = temp_idx_50


        # 数据入库
        self.insert_ir_data(ret, is_only_collect)

        return ret

    def get_box_id_by_user_id(self, table_name, user_id):
        sql = self.SELECT_BOX_ID_BY_USER_ID.format(table_name, user_id)

        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
            ret = cursor.fetchall()
            return ret

    def update_face_check_ret(self, table_name, face_ret_shift, face_ret_hight_temp_shift, face_ret_error, box_id):
        sql = self.FACE_CHECK_UPDATE_SQL.format(table_name, face_ret_shift, face_ret_hight_temp_shift,
                                                face_ret_error, box_id)
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
        self.connection.commit()