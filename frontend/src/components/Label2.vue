<template>
  <div>
    <el-container>
      <el-main>
        <el-card v-if="flag">
          <div slot="header">
            <span>Plot Window</span>
          </div>
          <dygraph :graphData="paintData" id="templateDygraphs" :dataName="paintDataName">
          </dygraph>
        </el-card>
      </el-main>
      <el-aside width="400px">
        <el-card>
          <div slot="header">
            <span>Data Navigator</span>
          </div>
          <p>Current Data ID: {{ currentData }}</p>
          <el-pagination
            background
            @current-change="currentDataChange"
            :current-page.sync=currentData
            :page-size=1
            layout="jumper, pager"
            :total=totalData
            pager-count=4
          ></el-pagination>
        </el-card>
        <el-card>
          <div slot="header">
            <span>Update Class/Centroid</span>
          </div>
          <p>Current Label: {{ currentLabel }}</p>
          <p>
            <table>
              <tr v-for="i in Math.ceil(totalTemplate / 6)" :key="i">
                <td v-for="n in Math.min(totalTemplate - (i - 1) * 6, 6)" :key="n + (i - 1) * 6" class="text item">
                  <label>
                    <input type="checkbox" :value="n + (i - 1) * 6" v-model="templateList" @change="changeCheckBox"/>
                    {{ n + (i - 1) * 6 }}
                  </label>
                </td>
              </tr>
            </table>
          </p>
          <el-button type="primary" @click="updateDataLabel" v-bind:disabled="ifConfirm">Update Label</el-button>
          <el-button type="primary" @click="updateTemplateData" v-bind:disabled="ifConfirm">Update Centroid</el-button>
        </el-card>
        <el-card>
          <div slot="header">
            <span>Export</span>
          </div>
          <p>
            <el-input v-model="path" placeholder="Path"></el-input>
          </p>
          <el-button type="primary" @click="exportLabelData">Export Labelled Data</el-button>
          <!--          <el-button @click="compareReconstruct">Compare Reconstruct</el-button>-->
          <!--          <el-button @click="reloadReconstruct">Reload Reconstruct</el-button>-->
        </el-card>
        <el-card>
          <div slot="header">
            <span>Redirect</span>
          </div>
          <el-button type="primary" @click="toCheck">Check Mode</el-button>
          <!--          <el-button @click="toCheckReconstruct">To Check Reconstruct</el-button>-->
          <!--          <el-button @click="toCheckZ">To Check Z</el-button>-->
        </el-card>
      </el-aside>
    </el-container>
  </div>
</template>

<script>
import qs from 'qs'
import dygraph from './dygraph'

const axios = require('axios')
export default {
  name: 'Label2',
  data() {
    return {
      currentData: 0,
      currentLabel: '',
      totalTemplate: 0,
      ttAlter: 0,
      tdAlter: 0,
      totalData: 0,
      ddAlter: 0,
      dtAlter: 0,
      ifConfirm: true,
      path: '',
      isNewLabel: false,
      templateList: [],
      paintDataName: [],
      paintData: [], // 默认第一个是待标注数据，后面是模板数据
      flag: false // 标记数据是否已经获取完毕
    }
  },
  components: {
    dygraph
  },
  methods: {
    updatePaintdata: function () {
      this.paintDataName = []
      const dataIndex = []
      this.ddAlter = this.currentData
      this.paintDataName.push('data' + this.currentData)
      dataIndex.push(this.currentData)
      for (let i = 0; i < this.templateList.length; i++) {
        this.paintDataName.push('template' + this.templateList[i])
        dataIndex.push(this.$store.getters.getDataindexNameByTemplateid(this.templateList[i]))
      }
      let data = {
        data_index: dataIndex
      }
      axios
        .post(
          this.$store.getters.getBaseUrl + 'mvts/read_data_list',
          qs.stringify(data, {arrayFormat: 'brackets'})
        )
        .then(res => {
          if (res.data !== 'failed') {
            this.paintData = res.data
            console.log(res.data)
          } else {
            this.$message.error('Get data failed!')
          }
        })
    },
    currentDataChange: function () {
      this.isNewLabel = false
      this.currentLabel = this.$store.getters.getLabelByIndex(this.currentData)
      if (this.currentLabel !== undefined) {
        // this.templateList = [ this.currentLabel ]
        this.dtAlter = this.currentLabel
      }
      this.updatePaintdata()
    },
    setNewTemplate: function () {
      if (this.isNewLabel === false) {
        this.totalTemplate += 1
        this.$store.commit('update_template', {
          templateId: this.totalTemplate,
          data_index: this.currentData
        })
        this.$store.commit('add_total_template')
        this.isNewLabel = true
        if (this.totalData !== 0) {
          this.ifConfirm = false
        }
      } else {
        this.totalTemplate -= 1
        if (this.totalTemplate === 0 || this.totalData === 0) {
          this.ifConfirm = true
        }
        this.isNewLabel = false
        this.$store.commit('sub_total_template')
      }
    },
    updateTemplateData: function () {
      // 更新当前模板数据
      this.$store.commit('update_template', {
        templateId: this.dtAlter,
        data_index: this.ddAlter
      })
      this.$message({
        message: 'Update template success',
        type: 'success'
      })
    },
    updateDataLabel: function () {
      // 标注数据
      this.$store.commit('update_label', {
        data_index: this.ddAlter,
        templateId: this.dtAlter
      })
      this.currentLabel = this.$store.getters.getLabelByIndex(this.currentData)
      this.$message({
        message: 'Update data label success',
        type: 'success'
      })
    },
    exportLabelData: function () {
      let data = {
        label: this.$store.getters.getLabel,
        template: this.$store.getters.getTemplate,
        path: this.path
      }
      axios
        .post(this.$store.getters.getBaseUrl + 'mvts/export_data', data)
        .then(res => {
          if (res.data !== 'failed') {
            this.$message({
              message: 'Export data success!',
              type: 'success'
            })
          } else {
            this.$message.error('Export data failed!')
          }
        })
    },
    toCheck: function () {
      this.$router.push('check')
    },
    toCheckZ: function () {
      this.$router.push('check_z')
    },
    changeCheckBox: function () {
      if (this.templateList.length > 1) {
        let last = this.templateList[this.templateList.length - 1]
        this.templateList = [last]
        this.dtAlter = last
      }
      this.updatePaintdata()
    },
    compareReconstruct: function () {
      this.paintDataName = []
      const dataIndex = []
      this.ddAlter = this.currentData
      this.paintDataName.push('data' + this.currentData)
      this.paintDataName.push('data' + this.currentData + '_reconstruct')
      dataIndex.push(this.currentData)
      for (let i = 0; i < this.templateList.length; i++) {
        this.paintDataName.push('template' + this.templateList[i])
        this.paintDataName.push('template' + this.templateList[i] + '_reconstruct')
        dataIndex.push(this.$store.getters.getDataindexNameByTemplateid(this.templateList[i]))
      }
      let data = {
        data_index: dataIndex
      }
      axios
        .post(
          this.$store.getters.getBaseUrl + 'mvts/read_reconstruct_list',
          qs.stringify(data, {arrayFormat: 'brackets'})
        )
        .then(res => {
          if (res.data !== 'failed') {
            this.paintData.push(res.data[0])
            console.log(this.paintData)
          } else {
            this.$message.error('Get data failed!')
          }
        })
    },
    reloadReconstruct: function () {
      axios
        .post(
          this.$store.getters.getBaseUrl + 'mvts/reload_reconstruct'
        )
        .then(res => {
          if (res.data === 'success') {
            console.log(res.data)
          } else {
            this.$message.error('Get data failed!')
          }
        })
    },
    toCheckReconstruct: function () {
      this.$router.push('check_reconstruct')
    }
  },
  mounted: function () {
    this.totalData = this.$store.getters.getDataNum
    if (this.totalData !== 0) {
      this.currentData = 1
      this.currentLabel = this.$store.getters.getLabelByIndex(this.currentData)
      this.tdAlter = 1
      this.ddAlter = 1
      let data = new FormData()
      data.append('data_index', this.currentData)
      axios
        .post(this.$store.getters.getBaseUrl + 'mvts/read_data', data)
        .then(res => {
          this.paintDataName.push('data' + this.currentData)
          this.paintData.push(res.data)
          this.flag = true
        })
    }
    this.totalTemplate = this.$store.getters.getTotalTemplate
    if (this.totalTemplate !== 0) {
      this.ttAlter = 1
      this.dtAlter = 1
    }
    if (this.totalData !== 0 && this.totalTemplate !== 0) {
      this.ifConfirm = false
    }
  }
}
</script>

<style scoped>
.el-aside {
  background: #eee;
}

.el-card {
  margin: 10px;
}

.el-main {
  background: #eee;
  padding: 0;
}

/*.el-col {*/
/*  border-radius: 4px;*/
/*}*/

/*.bg-purple-dark {*/
/*  background: #99a9bf;*/
/*}*/

/*.bg-purple {*/
/*  background: #d3dce6;*/
/*}*/

/*.bg-purple-light {*/
/*  background: #e5e9f2;*/
/*}*/

/*.grid-content {*/
/*  position: fixed;*/
/*  border-radius: 4px;*/
/*  min-height: 36px;*/
/*  top: 0;*/
/*  right: 0;*/
/*  width: 380px;*/
/*  z-index: 9999;*/
/*  filter: alpha(opacity=60);*/
/*  _bottom: auto;*/
/*  _position: absolute;*/
/*}*/

/*.bd-add {*/
/*  border: 1px dashed #000;*/
/*  border-radius: 5px;*/
/*  margin-top: 3px;*/
/*}*/

/*.el-header {*/
/*  position: relative;*/
/*  display: flex;*/
/*}*/

/*.el-pager li {*/
/*  padding: 0px;*/
/*  min-width: 30px;*/
/*}*/

/*.inline {*/
/*  display: inline;*/
/*}*/

/*.el-button--primary {*/
/*  color: #fff;*/
/*  background-color: #409eff;*/
/*  border-color: #409eff;*/
/*  margin-right: 40px;*/
/*  float: right;*/
/*  width: 50px;*/
/*}*/

/*.el-pagination .btn-next .el-icon,*/
/*.el-pagination .btn-prev .el-icon {*/
/*  display: inline;*/
/*}*/

/*.chart-container /deep/ .el-scrollbar__wrap {*/
/*  overflow-x: hidden;*/
/*}*/

/*.chart-container {*/
/*  height: 3000px;*/
/*}*/

/*.template-font {*/
/*  color: #606266;*/
/*  font-size: 14px;*/
/*  text-align: center;*/
/*  width: 90%;*/
/*  margin-top: 10px;*/
/*}*/

/*.aside-font {*/
/*  color: #606266;*/
/*  font-size: 14px;*/
/*  text-align: center;*/
/*  margin: 10px;*/
/*}*/

/*.tool-button {*/
/*  margin: 10px;*/
/*  text-align: center;*/
/*  align-items: center;*/
/*}*/
</style>
