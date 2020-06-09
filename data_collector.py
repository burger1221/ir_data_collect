import paho.mqtt.client as mqtt
import random
from flask import Flask, render_template, jsonify, request, send_file
import websocket
from ir_data_resolver import IrDataResolver
import json
import logging
import config
import traceback


#数据采集流程：
#接受摄像头消息 -> 解析数据 -> 推前端 -> 输入环境温度 -> 后端保存记录

# flask init
# 在app创建之前先重置日志级别为debug，后面的日志级别设置才能生效
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

ws = websocket.WebSocket()
ws.connect(config.WS_URL)


resolver = IrDataResolver(config.MYSQL_USER, config.MYSQL_PASSWD,
                          db_host=config.MYSQL_HOST, db_name=config.MYSQL_DB_NAME)


# flask url start
@app.route('/')
def index():
    return render_template('index.html')


@app.route("/image/<imageId>")
def image(imageId):
    path = 'images/' + imageId
    return send_file(path)


@app.route("/image/images/<imageId>")
def image2(imageId):
    path = 'images/' + imageId
    return send_file(path)


@app.route("/update_box_id", methods=['POST'])
def update_box_id():
    update_data = json.loads(request.get_data())
    resolver.update_ir_data(update_data)
    return 'success'


@app.route("/final_update_box_id", methods=['POST'])
def final_update_box_id():
    update_data = json.loads(request.get_data())
    resolver.final_update_ir_data(update_data)
    return 'success'


@app.route("/get_box_id_by_user_id/<table_name>/<user_id>", methods=['POST', 'GET'])
def get_box_id_by_user_id(table_name, user_id):
    query_ret = resolver.get_box_id_by_user_id(table_name, user_id)
    return json.dumps(query_ret)


@app.route("/update_face_check_ret/<table_name>/<face_ret_shift>/<face_ret_hight_temp_shift>/<face_ret_error>/<id>", methods=['POST', 'GET'])
def update_face_check_ret(table_name, face_ret_shift, face_ret_hight_temp_shift, face_ret_error ,id):
    resolver.update_face_check_ret(table_name, face_ret_shift, face_ret_hight_temp_shift, face_ret_error, id)
    return "success"
# flask url end

# mqtt connect && subscribe topic
def on_connect(client, userdata, flags, rc):
    client.subscribe(config.IR_DATA_COLLECT_TOPIC)
    print("Connected with result code "+str(rc))


# 接受消息 -> 解析数据 -> 推前端
def on_message(client, userdata, msg):
    m = str(msg.payload, encoding='utf-8')
    ir_data_dto = json.loads(m)
    type = ir_data_dto['type']
    if type == "XMONITOR":
        try:
            resolve_ret = resolver.ir_data_resolve(ir_data_dto['data'],False)
            ws.send(json.dumps(resolve_ret))
        except Exception as err:
            traceback.print_exc()



# 接受消息 -> 解析数据 -> 推前端
def on_message_only_collect(client, userdata, msg):
    m = str(msg.payload, encoding='utf-8')
    ir_data_dto = json.loads(m)
    type = ir_data_dto['type']
    if type == "XMONITOR":
        resolve_ret = resolver.ir_data_resolve(ir_data_dto['data'], True)


client_num = random.randint(0, 100)
client_id = 'ir_data_collector_' + str(client_num)

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.MQTT_SERVER_IP, config.MQTT_SERVER_PORT, config.MQTT_KEEP_ALIVE)

client_only_collect = mqtt.Client(client_id)
if config.IS_MQTT_ONLY_COLLECT:
    client_only_collect.on_connect = on_connect
    client_only_collect.on_message = on_message_only_collect
    client_only_collect.connect(config.MQTT_SERVER_IP_ONLY_COLLECT, config.MQTT_SERVER_PORT_ONLY_COLLECT, config.MQTT_KEEP_ALIVE_ONLY_COLLECT)


if __name__ == "__main__":
    print("start ir_data_collect")
    # mqtt start
    client.loop_start()
    if config.IS_MQTT_ONLY_COLLECT:
        client_only_collect.loop_start()
    # web start
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(config.LOG_LEVEL)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0')