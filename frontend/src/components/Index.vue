<template>
  <div>
    <img src="../assets/logo.png" class="logo-img" />
    <div class="box">
      <el-row>
        <el-col :offset="7" :span="2">
          <span class="text">Path:</span>
        </el-col>
        <el-col :span="9">
          <el-input v-model="address" placeholder="Absolute Path"></el-input>
        </el-col>
      </el-row>
      <el-row>
        <el-col :offset="11">
          <el-button type="primary"  @click="onReset">Reset</el-button>
          <el-button type="primary" @click="onSubmit">Confirm</el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
const axios = require('axios')
export default {
  data () {
    return {
      address: 'C:\\Users\\Lenovo\\Desktop\\all_data_to_label.npy'
    }
  },
  methods: {
    onSubmit () {
      if (this.checkstatus() === true) {
        const loading = this.$loading({
          lock: true,
          text: 'data processing...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        })
        let data = new FormData()
        data.append('filePath', this.address)
        axios.post(
          this.$store.getters.getBaseUrl + 'mvts/read_save_file',
          data
        ).then(
          res => {
            loading.close()
            if (res.data !== 'failed') {
              this.$store.commit('update_total_data', res.data)
              this.$store.commit('update_can_label')
              this.$router.push('check_new')
            } else {
              this.$message.error('Failed!Please try again!')
            }
          }
        )
      }
    },
    onReset () {
      this.address = ''
    },
    checkstatus () {
      if (this.address === '') {
        this.$message({
          showClose: true,
          message: 'Input cannot be empty!',
          type: 'error'
        })
        return false
      }
      return true
    }
  },
  mounted: function () {
    axios.get(this.$store.getters.getBaseUrl +
    'mvts/search_file').then(res => {
      if (res.data === 'Existed') {
        this.$confirm('An unfinished annotation was detected. Do you want to continue?', 'Prompt', {
          confirmButtonText: 'continue',
          cancelButtonText: 'cancel',
          type: 'warning'
        }).then(() => {
          const loading = this.$loading({
            lock: true,
            text: 'data processing...',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          })
          axios.get(this.$store.getters.getBaseUrl + 'mvts/get_template').then(res => {
            if (res.data !== 'failed') {
              if (res.data !== 'no template data') {
                for (var key in res.data) {
                  this.$store.commit('update_template', {templateId: key, data_index: res.data[key]})
                }
              }
            }
            axios.get(this.$store.getters.getBaseUrl + 'mvts/get_label').then(res => {
              if (res.data !== 'failed') {
                if (res.data !== 'no label data') {
                  for (var key in res.data) {
                    this.$store.commit('update_label', {data_index: key, templateId: res.data[key]})
                  }
                }
              }
              axios.get(this.$store.getters.getBaseUrl + 'mvts/read_file').then(res => {
                if (res.data !== 'failed') {
                  this.$store.commit('update_total_data', res.data)
                  this.$store.commit('update_can_label')
                  loading.close()
                  this.$router.push('label').catch(err => { console.log(err) })
                }
              })
            })
          })
        }).catch(() => {
          axios.get(this.$store.getters.getBaseUrl + 'mvts/clear_file').then(res => {
            if (res.data === 'success') {
              this.$message({
                type: 'info',
                message: 'Clear Success!'
              })
            } else {
              this.$message.error('Clear Failed!')
            }
          })
        })
      }
    })
  }
}
</script>

<style scoped>
.logo-img {
  height: 80px;
}

.el-row {
  margin-bottom: 20px;
}

.box {
  margin: 40px;
}

.text {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  font-size: 16px;
  line-height: 40px;
  color: #606266;
}

.el-button--primary {
  color: white;
  background-color: black;
  border-color: black;
  margin-right: 20px;
}
</style>
