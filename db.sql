CREATE TABLE `ir_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `box_id` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '人员id',
  `visible_img_file_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '可见光文件路径',
  `unvisible_img_file_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '热成像文件路径',
  `tmp_img_file_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '温度图片路径',
  `vx1` int(11) NOT NULL COMMENT '可见光vx1',
  `vx2` int(11) NOT NULL COMMENT '可见光vx2',
  `vy1` int(11) NOT NULL COMMENT '可见光vy1',
  `vy2` int(11) NOT NULL COMMENT '可见光vy2',
  `x1` int(11) NOT NULL COMMENT '热成像x1',
  `x2` int(11) NOT NULL COMMENT '热成像x2',
  `y1` int(11) NOT NULL COMMENT '热成像y1',
  `y2` int(11) NOT NULL COMMENT '热成像y1',
  `evn_temp` double DEFAULT NULL COMMENT '环境温度(摄氏度)',
  `wind_speed` double DEFAULT NULL COMMENT '风速(m/s)',
  `humidity` double DEFAULT NULL COMMENT '湿度(%)',
  `lux` double DEFAULT NULL COMMENT '光照强度(lux)',
  `black_set_temp` double DEFAULT NULL COMMENT '黑体设定温度(摄氏度)',
  `black_real_temp` double DEFAULT NULL COMMENT '黑体测量温度(摄氏度)',
  `ir_temp_surf` double DEFAULT NULL COMMENT '热成像温度(摄氏度)',
  `ir_cem_surf` double DEFAULT NULL COMMENT 'cem体表温度(摄氏度)',
  `ir_o1_surf` double DEFAULT NULL COMMENT 'o1体表温度(摄氏度)',
  `ir_o2_surf` double DEFAULT NULL COMMENT 'o2体表温度(摄氏度)',
  `ir_cem_core` double DEFAULT NULL COMMENT 'cem体内温度(摄氏度)',
  `ir_o1_core` double DEFAULT NULL COMMENT 'o1体内温度(摄氏度)',
  `ir_o2_core` double DEFAULT NULL COMMENT 'o2体内温度(摄氏度)',
  `core_temp` double DEFAULT NULL COMMENT '水银体内温度(摄氏度)',
  `in_temp` double DEFAULT NULL COMMENT '机芯温度(摄氏度)',
  `face_ret_shift` int(11) DEFAULT NULL COMMENT '人脸识别检查结果，0：ok；1：人脸偏移',
  `face_ret_hight_temp_shift` int(11) DEFAULT NULL COMMENT '人脸识别检查结果，0：ok；1：最高温偏移',
  `face_ret_error` int(11) DEFAULT NULL COMMENT '人脸识别检查结果，0：ok；1：人脸误检',
  `face_ret_is_check` int(11) DEFAULT NULL COMMENT '是否已经标记，0:no；1:yes',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `distance` int(11) DEFAULT NULL COMMENT '走多远(米)',
  `duration` int(11) DEFAULT NULL COMMENT '走多久（min）',
  `is_umbrella` int(11) DEFAULT NULL COMMENT '是否打伞 0:no；1:yes',
  `is_hat` int(11) DEFAULT NULL COMMENT '是否戴帽子 0:no；1:yes',
  `sweat` int(11) DEFAULT NULL COMMENT '是否戴帽子 0:no；1:出汗；2：出很多汗',
  `vehicle` int(11) DEFAULT NULL COMMENT '是否戴帽子 0:步行；1:骑车；2：汽车',
  `after_ir_cem_surf` double DEFAULT NULL COMMENT 'o1体表温度(摄氏度)，补充采集',
  `over_ir_ret_bac` int(11) DEFAULT NULL COMMENT '测温过高原因-背景过高 0:no；1:yes',
  `over_ir_ret_hair` int(11) DEFAULT NULL COMMENT '测温过高原因-头发过高 0:no；1:yes',
  `over_ir_ret_black_pos` int(11) DEFAULT NULL COMMENT '测温过高原因-黑体位置 0:no；1:yes',
  `over_ir_ret_black_temp` int(11) DEFAULT NULL COMMENT '测温过高原因-黑体温度 0:no；1:yes',
  `is_only_collect` int(11) DEFAULT NULL COMMENT '是否来至采集设备 0:no；1:yes',
  `sur_t_o` double DEFAULT NULL COMMENT '修正热成像温度(摄氏度)',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '备注',
  `avg` double DEFAULT NULL COMMENT '当前队列avg',
  `max` double DEFAULT NULL COMMENT '当前队列max',
  `min` double DEFAULT NULL COMMENT '当前队列min',
  `std` double DEFAULT NULL COMMENT '当前队列std',
  `var` double DEFAULT NULL COMMENT '当前队列var',
  `med` double DEFAULT NULL COMMENT '当前队列med',
  `temp_idx` int(11) DEFAULT NULL COMMENT '所在当前队列位置',
  `queue_len` int(11) DEFAULT NULL COMMENT '当前队列长度',
  `temp_idx_5` double DEFAULT NULL COMMENT '当前队列%5温度',
  `temp_idx_10` double DEFAULT NULL COMMENT '当前队列%10温度',
  `temp_idx_15` double DEFAULT NULL COMMENT '当前队列%15温度',
  `temp_idx_20` double DEFAULT NULL COMMENT '当前队列%20温度',
  `temp_idx_25` double DEFAULT NULL COMMENT '当前队列%25温度',
  `temp_idx_30` double DEFAULT NULL COMMENT '当前队列%30温度',
  `temp_idx_35` double DEFAULT NULL COMMENT '当前队列%35温度',
  `temp_idx_40` double DEFAULT NULL COMMENT '当前队列%40温度',
  `temp_idx_45` double DEFAULT NULL COMMENT '当前队列%45温度',
  `temp_idx_50` double DEFAULT NULL COMMENT '当前队列%50温度',
  PRIMARY KEY (`id`),
  KEY `idx_ir_data_box_id` (`box_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;