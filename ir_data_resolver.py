import random
import base64
import numpy as np
import cv2
import pymysql.cursors
import struct


class IrDataResolver:


    INSERT_SQL = "INSERT INTO `ir`.`ir_data` (`box_id`,`visible_img_file_name`,`unvisible_img_file_name`," \
                 "`tmp_img_file_name`,`vx1`,`vx2`,`vy1`,`vy2`,`x1`,`x2`,`y1`,`y2`,`ir_temp_surf`,`black_set_temp`," \
                 "`black_real_temp`, `in_temp`) " \
                 "VALUES ('{0}','{1}','{2}','{3}',{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15});"

    UPDATE_SQL = "UPDATE `ir`.`ir_data` " \
                 "SET evn_temp = {0}, wind_speed = {1}, humidity = {2}, lux = {3}, ir_cem_surf = {4}, " \
                 "ir_o1_surf = {5}, ir_o2_surf = {6} " \
                 "WHERE `box_id` = {7}"

    FINAL_UPDATE_SQL = "UPDATE `ir`.`ir_data` SET core_temp = {0} WHERE box_id = {1}"

    def __init__(self, db_user, db_passwd, db_host='localhost', db_port=3306, db_name='ir'):
        self.connection = pymysql.connect(host=db_host,
                                     user=db_user,
                                     password=db_passwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def insert_ir_data(self, ir_dict):
        sql = self.INSERT_SQL.format(ir_dict['box_id'], ir_dict['visible_img_file_name'], ir_dict['unvisible_img_file_name'],
                               ir_dict['tmp_img_file_name'], ir_dict['vx1'], ir_dict['vx2'], ir_dict['vy1'],
                               ir_dict['vy2'], ir_dict['x1'], ir_dict['x2'], ir_dict['y1'], ir_dict['y2'],
                               ir_dict['sur_t'], ir_dict['bla_s'], ir_dict['bla_o'], ir_dict['in_temp'])
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def update_ir_data(self, update_dict):
        sql = self.UPDATE_SQL.format(update_dict['env_temp'], update_dict['wind_speed'],
                                     update_dict['humidity'], update_dict['light'], update_dict['cem'] ,
                                     update_dict['o1'], update_dict['o2'], update_dict['box_id'])

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def final_update_ir_data(self, update_dict):
        sql = self.FINAL_UPDATE_SQL.format(update_dict['mercury'], update_dict['box_id'])

        with self.connection.cursor() as cursor:
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
    def ir_data_resolve(self, ir_data):
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
        # 数据入库
        self.insert_ir_data(ret)

        # 计算体表修正温度
        sur_t_o  = bla_s - bla_o + sur_t
        ret["sur_t_o"] = sur_t_o
        sur_t_2_core = self.convert_2_core_temp(sur_t_o)
        ret["sur_t_2_core"] = sur_t_2_core

        return ret