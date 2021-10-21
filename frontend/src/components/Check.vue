<template>
  <div>
    <el-col :xs="15" :sm="16" :md="17" :lg="18" :xl="19">
      <div class="chart-container bg-purple-dark" v-if="flag">
        <el-scrollbar style="height: 100%; width: 100%">
          <dygraph
            :graphData="paintData"
            :oldLabel="oldLabel"
            :is-compare="isCompare"
            id="templateDygraphs"
            :dataName="paintDataName"
          >
          </dygraph>
        </el-scrollbar>
      </div>
    </el-col>
    <el-col :xs="9" :sm="8" :md="7" :lg="6" :xl="5">
      <div class="grid-content">
        <div class="aside-font bd-add">
          Current template:{{ currentTemplate }}
          <el-pagination
            @current-change="start"
            :current-page.sync="currentTemplate"
            :page-size="1"
            :pager-count="4"
            layout="jumper,prev, pager, next"
            :total="totalTemplate"
          ></el-pagination>
        </div>
        <div class="aside-font bd-add">
          DataPage
          <div class="inline">
            <el-pagination
              @current-change="updatePaintdata"
              :current-page.sync="dataPage"
              :page-size="1"
              layout="jumper, prev, pager, next"
              :pager-count="4"
              :total="totalDataPage"
            ></el-pagination>
          </div>
        </div>
        <div class="aside-font bd-add">Current label:{{currentTemplate}}</div>
        <div class="aside-font bd-add">
          Change label
          <br />
          <div class="inline">
            <div
              style="display: inline-block"
              v-for="(item, key) in paintDataName"
              v-bind:key="key"
            >
              <input type="checkbox" v-model="checkList[key]" />{{ item }}
            </div>
          </div>
          <div class="change">
            <div class="change-text">new label:</div>
            <el-input
              class="change-input"
              v-model="input"
              placeholder="input new label"
            ></el-input>
          </div>
          <div class="tool-button">
            <el-button plain @click="resetData">Change</el-button>
          </div>
        </div>

        <div class="aside-font bd-add">
          <div class="tool-button">
            <el-button @click="start">Update data</el-button>
            <el-button @click="changeCompare">Change Status</el-button>
          </div>
        </div>
        <div class="aside-font bd-add">
          <el-input v-model="path" placeholder="Path"></el-input>
          <div class="tool-button">
            <el-button @click="exportLabelData">Export labelled data</el-button>
          </div>
        </div>
        <div class="aside-font bd-add">
          <div class="tool-button">
            <el-button @click="toLabel">To Label Mode</el-button>
          </div>
        </div>
      </div>
    </el-col>
  </div>
</template>
<script>
/* eslint-disable */
import dygraph from "./dygraph";
import qs from "qs";
const axios = require("axios");
export default {
  name: "Check",
  data() {
    return {
      dataPage: 0,
      totalDataPage: 0,
      currentTemplate: 0,
      reData: 0,
      totalTemplate: 0,
      totalData: 0,
      dataList: [],
      paintDataName: [],
      paintData: [], // 默认第一个是待标注数据，后面是模板数据
      flag: false, // 标记数据是否已经获取完毕
      path: "",
      isCompare: true, // 标记当前页面是否用于与手动标注数据的对比
      oldLabel: [],
      dataNum: 10 /* 20 */,
      checkList: [],
      dataIndex: [],
      ddAlter: 0,
      dtAlter: 0,
      input: 0,
    };
  },
  components: {
    dygraph,
  },
  methods: {
    async updatePaintdata() {
      this.paintDataName = [];
      this.dataIndex = [];
      this.checkList = [];
      for (let j = 0, len = this.dataList.length; j < len; j++) {
        if (
          j >= this.dataPage * this.dataNum - this.dataNum &&
          j < this.dataPage * this.dataNum
        ) {
          this.paintDataName.push("data" + this.dataList[j]);
          this.dataIndex.push(this.dataList[j]);
        }
      }
      for (let i = 0; i < this.paintDataName.length; i++) {
        this.checkList.push(false);
      }
      let data = {
        data_index: this.dataIndex,
      };
      if (this.isCompare) {
        await axios
          .post(
            this.$store.getters.getBaseUrl + "mvts/read_label_list",
            qs.stringify(data, { arrayFormat: "brackets" })
          )
          .then((res) => {
            if (res.data !== "failed") {
              this.oldLabel = res.data;
            } else {
              this.$message.error("Get label failed!");
            }
          });
        await axios
          .post(
            this.$store.getters.getBaseUrl + "mvts/read_z_list",
            qs.stringify(data, { arrayFormat: "brackets" })
          )
          .then((res) => {
            if (res.data !== "failed") {
              this.paintData = res.data;
              this.flag = true;
            } else {
              this.$message.error("Get data failed!");
            }
          });
      } else {
        axios
          .post(
            this.$store.getters.getBaseUrl + "mvts/read_z_list",
            qs.stringify(data, { arrayFormat: "brackets" })
          )
          .then((res) => {
            if (res.data !== "failed") {
              this.paintData = res.data;
              this.flag = true;
            } else {
              this.$message.error("Get data failed!");
            }
          });
      }
    },
    resetData: function () {
      let deleteList = [];
      for (let i = 0; i < this.checkList.length; i++) {
        if (this.checkList[i] === true) {
          deleteList.push(this.dataIndex[i]);
        }
      }
      console.log(deleteList);
      if (this.input !== 0) {
        for (let i = 0; i < deleteList.length; i++) {
          this.$store.commit("update_label", {
            data_index: deleteList[i],
            templateId: this.input, //label
          });
        }
        this.$message({
          message: "Update data label success",
          type: "success",
        });
        this.input = 0;
        this.exportLabelData();
        this.update();
      } else {
        this.$message({
          message: "Update data failed!Check the label you input again!",
          type: "error",
        });
      }
    },
    toLabel: function () {
      this.$router.push("label");
    },
    exportLabelData: function () {
      let data = {
        label: this.$store.getters.getLabel,
        template: this.$store.getters.getTemplate,
        path: this.path,
      };
      axios
        .post(this.$store.getters.getBaseUrl + "mvts/export_data", data)
        .then((res) => {
          if (res.data !== "failed") {
            this.$message({
              message: "Export data success!",
              type: "success",
            });
          } else {
            this.$message.error("Export data failed!");
          }
        });
    },
    start: function () {
      this.dataList = this.$store.getters.getDataByTemplateId(
        this.currentTemplate
      );
      if (this.dataList.length === 0) {
        this.$message.error("No data");
      } else {
        this.paintDataName = [];
        if (this.dataList.length > 0) {
          this.dataPage = 1;
          if ((this.dataList.length / this.dataNum) % 1 === 0) {
            this.totalDataPage = parseInt(this.dataList.length / this.dataNum);
          } else {
            this.totalDataPage =
              parseInt(this.dataList.length / this.dataNum) + 1;
          }
        }
        this.updatePaintdata();
      }
    },
    changeCompare: function () {
      this.isCompare = !this.isCompare;
    },
  },
  mounted: function () {
    this.totalData = this.$store.getters.getDataNum;
    this.totalTemplate = this.$store.getters.getTotalTemplate;
    if (this.totalData !== 0) {
      this.reData = 1;
    }
    if (this.totalTemplate !== 0) {
      this.currentTemplate = 1;
    } else {
      this.$message.error("There is no labelled data!");
      this.$router.push("label");
    }
    document.onkeydown = function (e) {
      if (e.code === "Enter") {
        this.resetData();
      }
    };
    this.start();
  },
};
</script>
<style>
.el-pagination__jump {
  display: block;
}

.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  position: fixed;
  border-radius: 4px;
  min-height: 36px;
  top: 0;
  right: 0;
  width: 345px;
  z-index: 9999;
  filter: alpha(opacity = 60);
  _bottom: auto;
  _position: absolute;
}
.bd-add {
  border: 1px dashed #000;
  border-radius: 5px;
  margin-top: 3px;
}
.el-header {
  position: relative;
  display: flex;
}
.el-pager li {
  padding: 0;
  min-width: 30px;
}
.inline {
  display: inline;
}
.el-button--primary {
  color: #fff;
  background-color: #409eff;
  border-color: #409eff;
  margin-right: 40px;
  float: right;
  width: 50px;
}

.el-pagination .btn-next .el-icon,
.el-pagination .btn-prev .el-icon {
  display: inline;
}

.chart-container /deep/ .el-scrollbar__wrap {
  overflow-x: hidden;
}
.chart-container {
  height: 1900px;
}
.template-font {
  color: #606266;
  font-size: 14px;
  text-align: center;
  width: 90%;
  margin-top: 10px;
}

.aside-font {
  color: #606266;
  font-size: 14px;
  text-align: center;
  margin: 10px;
}

.tool-button {
  margin: 10px;
  text-align: center;
  align-items: center;
}

.change {
  display: flex;
  padding: 0 30px;
}

.change-text {
  flex: 1;
  align-self: center;
}

.change-input {
  flex: 2;
}
</style>
