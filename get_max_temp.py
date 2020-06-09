import numpy as np
import cv2


img_id = '2020052802252090_209'
ir_img_path = 'get_max/unvisible_' + img_id + '.jpg'
temp_matrix_path = 'get_max/temp_' + img_id + '.npy'

temp_matrix = np.load(temp_matrix_path)
ir_img = cv2.imread(ir_img_path)

x_max, y_max, z = ir_img.shape
x_max = x_max - 1
y_max = y_max - 1

def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
        x_start = x - 10
        x_end = x + 10
        y_start = y - 10
        y_end = y + 10

        if x_start < 0:
            x_start = 0
        if x_end > x_max:
            x_end = x_max
        if y_start < 0:
            y_start = 0
        if y_end > y_max:
            y_end = y_max

        ir_small = ir_img[y_start:y_end,x_start:x_end]
        temp_matrix_small = temp_matrix[y_start:y_end,x_start:x_end]

        ir_max = np.max(ir_small)
        ir_min = np.min(ir_small)
        ir_avg = np.average(ir_small)
        temp_matrix_small_max = np.max(temp_matrix_small)
        temp_matrix_small_min = np.min(temp_matrix_small)
        temp_matrix_small_avg = np.average(temp_matrix_small)
        # cv2.imshow("small", ir_small)
        # cv2.waitKey(0)
        print('PIX:', x, y)
        print("BGR ir_max:", ir_max)
        print("BGR ir_min:", ir_min)
        print("BGR ir_avg:", ir_avg)
        print("TEMP temp_matrix_small_max:", temp_matrix_small_max)
        print("TEMP temp_matrix_small_min:", temp_matrix_small_min)
        print("TEMP temp_matrix_small_avg:", temp_matrix_small_avg)


cv2.namedWindow("ir_img")
cv2.setMouseCallback("ir_img", mouse_click)
cv2.imshow('ir_img', ir_img)


# cv2.imshow("test", temp_matrix.astype(np.int))
cv2.waitKey(0)