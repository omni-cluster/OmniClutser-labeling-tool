
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    canLabel: false,
    BASEURL: 'http://127.0.0.1:8000/',
    templates: {}, // 模板号： 数据index
    labels: {}, // 数据index ： label值
    total_template_num: 0,
    total_data: 0
  },
  mutations: {
    update_total_data (state, num) {
      state.total_data = parseInt(num)
    },
    update_label (state, para) {
      state.labels[parseInt(para.data_index)] = parseInt(para.templateId)
    },
    delete_label (state, para) {
      delete state.labels[parseInt(para.data_index)]
    },
    update_template (state, para) {
      para.templateId = parseInt(para.templateId)
      if (!state.templates.hasOwnProperty(para.templateId)) {
        state.total_template_num += 1
      }
      state.templates[para.templateId] = parseInt(para.data_index)
    },
    update_can_label (state) {
      state.canLabel = true
    },
    add_total_template (state) {
      state.total_template_num += 1
    },
    sub_total_template (state) {
      delete state.templates[state.total_template_num]
      state.total_template_num -= 1
    }
  },
  getters: {
    getBaseUrl: (state) => {
      return state.BASEURL
    },
    getLabelByIndex: (state) => (index) => {
      return state.labels[index]
    },
    getDataindexNameByTemplateid: (state) => (id) => {
      return state.templates[id]
    },
    getCanLabel: (state) => {
      return state.canLabel
    },
    getTotalTemplate: (state) => {
      return state.total_template_num
    },
    getLabel: (state) => {
      return state.labels
    },
    getTemplate: (state) => {
      return state.templates
    },
    getDataNum: (state) => {
      return state.total_data
    },
    getIndexsByTemplates: (state) => (templateList) => {
      const temIndex = []
      for (var i in templateList) {
        temIndex.push(state.templates[i])
      }
      return temIndex
    },
    getDataByTemplateId: (state) => (id) => {
      const temIndex = []
      id = parseInt(id)
      for (var key in state.labels) {
        var item = state.labels[key]
        if (item === id) {
          temIndex.push(key)
        }
      }
      return temIndex
    }
  }
})

export default store
