<template>
  <div>
    <div style="padding-top: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(0, 0, 0, 0.1)">
      <el-row :gutter="20" class="row">
        <el-col :span="14">
          <el-row>
            <el-col :span="8">
              <div class="label">环境温度：</div>
              <div class="input-div">
                <el-input v-model="environment.env_temp" size="small" />
              </div>
              <div class="unit">℃</div>
            </el-col>
            <el-col :span="8">
              <div class="label">湿度：</div>
              <div class="input-div">
                <el-input v-model="environment.humidity" size="small" />
              </div>
              <div class="unit">℃</div>
            </el-col>
            <el-col :span="8">
              <div class="label">风速：</div>
              <div class="input-div">
                <el-input v-model="environment.wind_speed" size="small" />
              </div>
              <div class="unit">m/s</div>
            </el-col>
          </el-row>
          <el-row style="margin-top: 8px">
            <el-col :span="8">
              <div class="label">光照强度：</div>
              <div class="input-div">
                <el-input v-model="environment.light" size="small" />
              </div>
              <div class="unit">lux</div>
            </el-col>
            <el-col :span="8">
              <div class="label">走多远：</div>
              <div class="input-div">
                <el-input v-model="environment.distance" size="small" />
              </div>
              <div class="unit">m</div>
            </el-col>
            <el-col :span="8">
              <div class="label">走多久：</div>
              <div class="input-div">
                <el-input v-model="environment.duration" size="small" />
              </div>
              <div class="unit">min</div>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="7" style="font-size: 14px">
          <div>
            <span>队列长度： {{ temp_idx.queue_len }}</span>
          </div>
          <div>
            <div>
              <div class="cell">idx_5</div>
              <div class="cell">idx_10</div>
              <div class="cell">idx_15</div>
              <div class="cell">idx_20</div>
              <div class="cell">idx_25</div>
              <div class="cell">idx_30</div>
              <div class="cell">idx_35</div>
              <div class="cell">idx_40</div>
              <div class="cell">idx_45</div>
              <div class="cell">idx_50</div>
            </div>
            <div>
              <div class="cell">{{ temp_idx.temp_idx_5.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_10.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_15.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_20.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_25.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_30.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_35.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_40.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_45.toFixed(2) }}</div>
              <div class="cell">{{ temp_idx.temp_idx_50.toFixed(2) }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="3">
          <el-button size="small" @click="clearLeft">清左</el-button>
          <el-button size="small" @click="clearRight">清右</el-button>
        </el-col>
      </el-row>
    </div>
    <div style="height: calc(100vh - 60px); overflow-y: auto">
      <el-row :gutter="20">
        <el-col :span="12">
          <div style="color: rgba(0, 0, 0, 0); height: 1px">-</div>
          <div
            v-for="(item, index) in msgList"
            v-if="!item.pre_save"
            :key="index"
            :style="{ background: item.pre_save ? '#e1f3d8' : '' }"
            style="border-bottom: 1px solid rgba(0, 0, 0, 0.1); padding: 12px 20px; position: relative">
            <i
              class="el-icon-circle-close close-icon"
              @click="deleteItem(index)"/>
            <div style="font-size: 14px">
              <span>人员编号：</span>
              <span>{{ item.box_id }}（{{ item.cnt }}）</span>
              <span style="font-size: 14px; color: #909399; padding-left: 16px; text-align: right">{{ item.time }}</span>
            </div>
            <el-row class="row">
              <el-col :span="12" style="text-align: center">
                <el-col :span="12" style="text-align: center">
                  <img :src=" '/image/' + item.visible_img_file_name" style="height: 220px; max-width: 100%">
                </el-col>
                <el-col :span="12" style="text-align: center">
                  <img :src="'/image/' + item.unvisible_img_file_name" style="height: 220px; max-width: 100%">
                </el-col>
                <div style="font-size: 12px; color: #909399">{{ item.visible_img_file_name }}</div>
              </el-col>
              <el-col :span="12" style="padding-top: 12px;">
                <div>
                  <el-row style="margin-bottom: 20px">
                    <el-col :span="12">
                      <div>
                        <div class="label">排名：</div>
                        <span style="font-size: 14px">{{ item.temp_idx }} / {{ item.queue_len }}</span>
                      </div>
                      <div>
                        <div class="label">CEM体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.cem" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">O1体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.o1" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">O2体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.o2" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">水银温度计：</div>
                        <div class="input-div">
                          <el-input v-model="item.mercury" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">后测体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.after_ir_cem_surf" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div style="text-align: center">
                        <div style="font-size: 12px; color: #909399">体表温度：{{ item.sur_t_o.toFixed(2) }}</div>
                        <div style="font-size: 12px; color: #909399">体内温度：{{ item.sur_t_2_core.toFixed(2) }}</div>
                        <div style="font-size: 12px; color: #909399">黑体设定：{{ item.bla_s.toFixed(2) }}</div>
                        <div style="font-size: 12px; color: #909399">黑体测量：{{ item.bla_o.toFixed(2) }}</div>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div>
                        <div style="font-size: 14px; font-weight: bold">预存字段</div>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.is_umbrella" true-label="1" false-label="0">有无伞</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.is_hat" true-label="1" false-label="0">有无帽子</el-checkbox>
                          </el-col>
                        </el-row>
                        <div>
                          <el-row>
                            <el-col :span="12">
                              <el-select v-model="item.sweat" placeholder="汗量" size="small">
                                <el-option label="无汗" value="0" />
                                <el-option label="微汗" value="1" />
                                <el-option label="汗如雨下" value="2" />
                              </el-select>
                            </el-col>
                            <el-col :span="12">
                              <el-select v-model="item.vehicle" placeholder="交通工具" size="small">
                                <el-option label="步行" value="0" />
                                <el-option label="骑车" value="1" />
                                <el-option label="开车" value="2" />
                              </el-select>
                            </el-col>
                          </el-row>
                        </div>
                        <div>
                          <div class="label" style="width: 42px">备注：</div>
                          <div class="input-div" style="width: calc(100% - 46px)">
                            <el-input v-model="item.description" size="small" />
                          </div>
                        </div>
                      </div>
                      <div style="padding-top: 16px">
                        <div style="font-size: 14px; font-weight: bold">测温过高原因</div>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_bac" true-label="1" false-label="0">背景过高</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_hair" true-label="1" false-label="0">头发过高</el-checkbox>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_black_pos" true-label="1" false-label="0">黑体偏移</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_black_temp" true-label="1" false-label="0">黑体温度变化</el-checkbox>
                          </el-col>
                        </el-row>
                      </div>
                      <div style="padding-top: 16px">
                        <div style="font-size: 14px; font-weight: bold">图片异常标记</div>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.face_ret_shift" true-label="1" false-label="0">人脸框偏移</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.face_ret_hight_temp_shift" true-label="1" false-label="0">高温点偏移</el-checkbox>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.face_ret_error" true-label="1" false-label="0">人脸误检</el-checkbox>
                          </el-col>
                        </el-row>
                      </div>
                      <div style="padding-top: 16px">
                        <div style="font-size: 14px; font-weight: bold">统计结果</div>
                        <el-row>
                          <el-col :span="12">
                            <span>中位数：{{ item.med.toFixed(2) }}</span>
                          </el-col>
                          <el-col :span="12">
                            <span>平均数：{{ item.avg.toFixed(2) }}</span>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <span>统计个数：{{ item.cnt }}</span>
                          </el-col>
                          <el-col :span="12">
                            <span>方差：{{ item.var.toFixed(2) }}</span>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <span>最大：{{ item.max.toFixed(2) }}</span>
                          </el-col>
                          <el-col :span="12">
                            <span>最小：{{ item.min.toFixed(2) }}</span>
                          </el-col>
                        </el-row>
                      </div>
                    </el-col>
                  </el-row>
                </div>
                <div style="text-align: center">
                  <el-button
                    :disabled="item.pre_save"
                    type="primary"
                    style="width: 150px"
                    size="small"
                    @click="saveEnv(item, index)">预存</el-button>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="color: rgba(0, 0, 0, 0); height: 1px">-</div>
          <div
            v-for="(item, index) in msgList"
            v-if="item.pre_save"
            :key="index"
            :style="{ background: item.pre_save ? '#e1f3d8' : '' }"
            style="border-bottom: 1px solid rgba(0, 0, 0, 0.1); padding: 12px 20px; position: relative">
            <i
              class="el-icon-circle-close close-icon"
              @click="deleteItem(index)"/>
            <div style="font-size: 14px">
              <span>人员编号：</span>
              <span>{{ item.box_id }}（{{ item.cnt }}）</span>
              <span style="font-size: 14px; color: #909399; padding-left: 16px; text-align: right">{{ item.time }}</span>
            </div>
            <el-row class="row">
              <el-col :span="12" style="text-align: center">
                <el-col :span="12" style="text-align: center">
                  <img :src=" '/image/' + item.visible_img_file_name" style="height: 220px; max-width: 100%">
                </el-col>
                <el-col :span="12" style="text-align: center">
                  <img :src="'/image/' + item.unvisible_img_file_name" style="height: 220px; max-width: 100%">
                </el-col>
                <div style="font-size: 12px; color: #909399">{{ item.visible_img_file_name }}</div>
              </el-col>
              <el-col :span="12" style="padding-top: 12px;">
                <div>
                  <el-row style="margin-bottom: 20px">
                    <el-col :span="12">
                      <div>
                        <div class="label">排名：</div>
                        <span style="font-size: 14px">{{ item.temp_idx }} / {{ item.queue_len }}</span>
                      </div>
                      <div>
                        <div class="label">CEM体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.cem" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">O1体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.o1" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">O2体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.o2" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">水银温度计：</div>
                        <div class="input-div">
                          <el-input v-model="item.mercury" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div>
                        <div class="label">后测体表：</div>
                        <div class="input-div">
                          <el-input v-model="item.after_ir_cem_surf" size="small" />
                        </div>
                        <div class="unit">℃</div>
                      </div>
                      <div style="text-align: center">
                        <div style="font-size: 12px; color: #909399">体表温度：{{ item.sur_t_o.toFixed(2) }}</div>
                        <div style="font-size: 12px; color: #909399">体内温度：{{ item.sur_t_2_core.toFixed(2) }}</div>
                        <div style="font-size: 12px; color: #909399">黑体设定：{{ item.bla_s.toFixed(2) }}</div>
                        <div style="font-size: 12px; color: #909399">黑体测量：{{ item.bla_o.toFixed(2) }}</div>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div>
                        <div style="font-size: 14px; font-weight: bold">预存字段</div>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.is_umbrella" true-label="1" false-label="0">有无伞</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.is_hat" true-label="1" false-label="0">有无帽子</el-checkbox>
                          </el-col>
                        </el-row>
                        <div>
                          <el-row>
                            <el-col :span="12">
                              <el-select v-model="item.sweat" placeholder="汗量" size="small">
                                <el-option label="无汗" value="0" />
                                <el-option label="微汗" value="1" />
                                <el-option label="汗如雨下" value="2" />
                              </el-select>
                            </el-col>
                            <el-col :span="12">
                              <el-select v-model="item.vehicle" placeholder="交通工具" size="small">
                                <el-option label="步行" value="0" />
                                <el-option label="骑车" value="1" />
                                <el-option label="开车" value="2" />
                              </el-select>
                            </el-col>
                          </el-row>
                        </div>
                        <div>
                          <div class="label" style="width: 42px">备注：</div>
                          <div class="input-div" style="width: calc(100% - 46px)">
                            <el-input v-model="item.description" size="small" />
                          </div>
                        </div>
                      </div>
                      <div style="padding-top: 16px">
                        <div style="font-size: 14px; font-weight: bold">测温过高原因</div>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_bac" true-label="1" false-label="0">背景过高</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_hair" true-label="1" false-label="0">头发过高</el-checkbox>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_black_pos" true-label="1" false-label="0">黑体偏移</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.over_ir_ret_black_temp" true-label="1" false-label="0">黑体温度变化</el-checkbox>
                          </el-col>
                        </el-row>
                      </div>
                      <div style="padding-top: 16px">
                        <div style="font-size: 14px; font-weight: bold">图片异常标记</div>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.face_ret_shift" true-label="1" false-label="0">人脸框偏移</el-checkbox>
                          </el-col>
                          <el-col :span="12">
                            <el-checkbox v-model="item.face_ret_hight_temp_shift" true-label="1" false-label="0">高温点偏移</el-checkbox>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <el-checkbox v-model="item.face_ret_error" true-label="1" false-label="0">人脸误检</el-checkbox>
                          </el-col>
                        </el-row>
                      </div>
                      <div style="padding-top: 16px">
                        <div style="font-size: 14px; font-weight: bold">统计结果</div>
                        <el-row>
                          <el-col :span="12">
                            <span>中位数：{{ item.med.toFixed(2) }}</span>
                          </el-col>
                          <el-col :span="12">
                            <span>平均数：{{ item.avg.toFixed(2) }}</span>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <span>统计个数：{{ item.cnt }}</span>
                          </el-col>
                          <el-col :span="12">
                            <span>方差：{{ item.var.toFixed(2) }}</span>
                          </el-col>
                        </el-row>
                        <el-row>
                          <el-col :span="12">
                            <span>最大：{{ item.max.toFixed(2) }}</span>
                          </el-col>
                          <el-col :span="12">
                            <span>最小：{{ item.min.toFixed(2) }}</span>
                          </el-col>
                        </el-row>
                      </div>
                    </el-col>
                  </el-row>
                </div>
                <div style="text-align: center">
                  <el-button
                    style="width: 150px"
                    size="small"
                    @click="saveEnv(item, index)">预存</el-button>
                  <el-button
                    :disabled="!item.pre_save"
                    type="primary"
                    style="width: 150px"
                    size="small"
                    @click="saveData(item, index)">保存</el-button>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
export default {
  name: 'Index',
  components: {
  },
  data() {
    return {
      msgList: [],
      environment: {
        env_temp: '28', // 环境温度
        humidity: '70', // 湿度
        wind_speed: '3', // 风速
        light: '10000', // 光照强度
        distance: '0', // 距离（走多远）
        duration: '0' // 走多久
      },
      result: {
        med: '', // 中位数
        avg: '', // 平均数
        cnt: '', // 最近多少个
        var: '', // 方差
        max: '', // 最大
        min: '' // 最小
      },
      cnt: 1000,
      websock: undefined,
      temp_idx: {
        queue_len: 0,
        temp_idx_5: 0,
        temp_idx_10: 0,
        temp_idx_15: 0,
        temp_idx_20: 0,
        temp_idx_25: 0,
        temp_idx_30: 0,
        temp_idx_35: 0,
        temp_idx_40: 0,
        temp_idx_45: 0,
        temp_idx_50: 0
      }
    }
  },
  watch: {

  },
  mounted: function() {
    this.initWebSocket()
  },
  destroyed: function() {
    this.websock.close()
  },
  methods: {
    saveEnv(item) {
      const temp = {
        box_id: item.box_id,
        o1: item.o1,
        o2: item.o2,
        cem: item.cem,
        is_umbrella: item.is_umbrella,
        is_hat: item.is_hat,
        sweat: item.sweat,
        vehicle: item.vehicle,
        description: item.description
      }
      const params = Object.assign({}, this.environment, temp)
      this.$axios.post('/api/update_box_id', params)
        .then((res) => {
          if (res.data === 'success') {
            item.pre_save = true
            this.$message.success('预存成功！')
          } else {
            this.$message.error('预存失败！')
          }
        }).catch((error) => {
          console.log(error)
          this.$message.error('预存失败！')
        })
    },
    saveData(item, index) {
      const params = {
        box_id: item.box_id,
        mercury: item.mercury,
        after_ir_cem_surf: item.after_ir_cem_surf,
        over_ir_ret_bac: item.over_ir_ret_bac,
        over_ir_ret_hair: item.over_ir_ret_hair,
        over_ir_ret_black_pos: item.over_ir_ret_black_pos,
        over_ir_ret_black_temp: item.over_ir_ret_black_temp,
        face_ret_shift: item.face_ret_shift,
        face_ret_hight_temp_shift: item.face_ret_hight_temp_shift,
        face_ret_error: item.face_ret_error,
        description: item.description
      }
      this.$axios.post('/api/final_update_box_id', params)
        .then((res) => {
          if (res.data === 'success') {
            this.$message.success('保存成功！')
          } else {
            this.$message.error('消息保存失败！')
          }
        }).catch((error) => {
          console.log(error)
          this.$message.error('消息保存失败！')
        })
    },
    deleteItem(index) {
      this.msgList.splice(index, 1)
    },
    clearLeft() {
      const self = this
      var i = this.msgList.length
      while (i--) {
        if (!this.msgList[i].pre_save) {
          self.msgList.splice(i, 1)
        }
      }
    },
    clearRight() {
      const self = this
      var i = this.msgList.length
      while (i--) {
        if (this.msgList[i].pre_save) {
          self.msgList.splice(i, 1)
        }
      }
    },
    /* 初始化websocket */
    initWebSocket() {
      const wsuri = 'ws://localhost:8181'
      this.websock = new WebSocket(wsuri)
      this.websock.onopen = this.websocketOnOpen

      this.websock.onerror = this.websocketOnError

      this.websock.onmessage = this.websocketOnMessage
      this.websock.onclose = this.websocketClose
    },

    websocketOnOpen() {
      console.log('WebSocket连接成功')
    },
    websocketOnError(e) {
      console.log('WebSocket连接发生错误')
    },
    websocketOnMessage(e) {
      if (e.data === 'Connected.') {
        console.log(e.data)
      } else {
        try {
          const message = JSON.parse(e.data)
          const index = this.msgList.findIndex(item => item.box_id === message.box_id)
          if (index === -1) {
            const todo = {
              mercury: 0,
              o1: '0',
              o2: '0',
              cem: '0',
              pre_save: false,
              time: moment().format('YYYY-MM-DD HH:mm:ss'),
              cnt: 1,
              is_umbrella: 0,
              is_hat: 0,
              sweat: '0',
              vehicle: '0',
              description: '',
              after_ir_cem_surf: 0,
              face_ret_error: 0,
              face_ret_hight_temp_shift: 0,
              face_ret_shift: 0,
              over_ir_ret_bac: 0,
              over_ir_ret_black_pos: 0,
              over_ir_ret_black_temp: 0,
              over_ir_ret_hair: 0
            }
            this.temp_idx = message
            const newMsg = Object.assign({}, message, todo)
            this.msgList.push(newMsg)
          } else {
            this.msgList[index].cnt++
          }
        } catch (error) {
          console.log(error)
        }
      }
    },
    websocketSend(agentData) {
      this.websock.send(agentData)
    },
    websocketClose(e) {
      console.log('Websocket connection closed (' + e.code + ')')
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  .label {
    display: inline-block;
    width: 90px;
    font-size: 14px;
    color: #606266;
    text-align: right;
  }
  .input-div{
    display: inline-block;
    width: calc(100% - 140px);
  }
  .unit{
    display: inline-block;
    width: 30px;
    font-size: 14px;
    color: #606266;
    margin-left: 8px;
  }
  .row{
    display: flex;
    align-items: center; /*定义body的元素垂直居中*/
  }
  .close-icon{
    position: absolute;
    right: 2px;
    top: 6px;
    font-size: 28px;
    color: #909399;
    cursor: pointer;
    z-index: 10;
  }
  .close-icon:hover{
    color: #606266;
  }
  .cell{
    display: inline-block;
    width: calc(10% - 2px);
    text-align: center;
    margin-left: 0px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    margin: -2px;
  }
</style>
