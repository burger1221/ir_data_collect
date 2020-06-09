<template>
  <div style="padding: 16px">
    <h1>测温图片确认</h1>
    <div style="padding-top: 16px; padding-bottom: 16px; border-bottom: 1px solid rgba(0, 0, 0, 0.1); margin-bottom: 16px">
      <el-row>
        <el-col :span="6">
          <div style="margin-right: 20px">
            <span style="font-size: 16px">人员ID：</span>
            <div style="display: inline-block; width: calc(100% - 100px)">
              <el-input v-model = "params.id" size="small" />
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div style="margin-right: 20px">
            <span style="font-size: 16px">表名：</span>
            <div style="display: inline-block; width: calc(100% - 100px)">
              <el-input v-model = "params.tableName" size="small" />
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <el-button :disabled="params.id === '' || params.tableName === ''" size="small" type="primary" @click="loadData">拉取数据</el-button>
        </el-col>
      </el-row>
    </div>
    <div style="height: calc(100vh - 140px); overflow-y: auto">
      <div style="text-align: right; padding-top: 16px;">
        <el-pagination
          :current-page="currentPage"
          :page-sizes="[5, 10, 15, 20]"
          :page-size="pageSize"
          :total="totalSize"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange" />
      </div>
      <div v-for="(item, index) in tableData" :key="index">
        <el-row :style="{ background: item.save ? '#e1f3d8' : '' }" class="row" style="padding: 12px">
          <el-col :span="6">
            <img v-lazy=" '/image/' + item.visible_img_file_name" style="height: 220px; max-width: 100%">
          </el-col>
          <el-col :span="6">
            <img v-lazy=" '/image/' + item.unvisible_img_file_name" style="height: 220px; max-width: 100%">
          </el-col>
          <el-col :span="12">
            <div style="margin-bottom: 12px">
              <span style="font-size: 14px"><span style="font-weight: bold">box_id：</span>{{ item.box_id }}</span>
              <span style="font-size: 14px; margin-left: 16px"><span style="font-weight: bold">id：</span>{{ item.id }}</span>
            </div>
            <div style="margin-bottom: 12px">
              <el-row>
                <el-col :span="8">
                  <el-checkbox v-model="item.face_ret_shift" true-label="1" false-label="0">人脸框偏移</el-checkbox>
                </el-col>
                <el-col :span="8">
                  <el-checkbox v-model="item.face_ret_hight_temp_shift" true-label="1" false-label="0">高温点偏移</el-checkbox>
                </el-col>
                <el-col :span="8">
                  <el-checkbox v-model="item.face_ret_error" true-label="1" false-label="0">人脸误检</el-checkbox>
                </el-col>
              </el-row>
            </div>
            <div>
              <el-button size="small" type="primary" @click="saveData(item)">保存</el-button>
            </div>
          </el-col>
        </el-row>
      </div>
      <div style="text-align: right; padding-top: 16px;">
        <el-pagination
          :current-page="currentPage"
          :page-sizes="[5, 10, 15, 20]"
          :page-size="pageSize"
          :total="totalSize"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sign',
  components: {
  },
  data() {
    return {
      params: {
        id: '',
        tableName: ''
      },
      tableData: [],
      totalData: [],
      currentPage: 1,
      totalSize: 0,
      pageSize: 10
    }
  },
  watch: {

  },
  mounted: function() {
  },
  destroyed: function() {
  },
  methods: {
    loadData() {
      const self = this
      const url = '/api/get_box_id_by_user_id/' + this.params.tableName + '/' + this.params.id
      this.$axios.post(url)
        .then((res) => {
          const list = res.data
          list.forEach(function(n) {
            n.face_ret_shift = 0
            n.face_ret_hight_temp_shift = 0
            n.face_ret_error = 0
            n.save = false
          })
          self.totalData = list
          self.initTable()
        }).catch((error) => {
          console.log(error)
          this.$message.error('数据拉取失败！')
        })
    },
    saveData(item) {
      const url = '/api/update_face_check_ret/' + this.params.tableName + '/' + item.face_ret_shift + '/' +
        item.face_ret_hight_temp_shift + '/' + item.face_ret_error + '/' + item.id
      console.log(url)
      this.$axios.post(url)
        .then((res) => {
          if (res.data === 'success') {
            item.save = true
          } else {
            this.$message.error('保存失败！')
          }
        }).catch((error) => {
          console.log(error)
          this.$message.error('保存失败！')
        })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.handleCurrentChange(this.currentPage)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.totalSize = this.totalData.length

      const start = (this.currentPage - 1) * this.pageSize
      let end = this.currentPage * this.pageSize
      end = end < this.totalSize ? end : this.totalSize
      this.tableData = []
      for (let i = start; i < end; i++) {
        this.tableData.push(this.totalData[i])
      }
    },
    initTable() {
      this.totalSize = this.totalData.length
      const start = (this.currentPage - 1) * this.pageSize
      let end = this.currentPage * this.pageSize
      end = end < this.totalSize ? end : this.totalSize
      this.tableData = []
      for (let i = start; i < end; i++) {
        this.tableData.push(this.totalData[i])
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  .row{
    display: flex;
    align-items: center; /*定义body的元素垂直居中*/
  }
</style>
