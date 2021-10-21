<template>
  <div>
    <div v-for="(item, i) in graphs" v-bind:key="item.id">
      <label class="dimension-label">{{i + 1}}</label>
      <div :id="gelabelid(item.id)"></div>
      <div :id="gegraphid(item.id)" class="graph"></div>
    </div>
  </div>
</template>

<script>
import Dygraphs from 'dygraphs'
export default {
  data () {
    return {
      graphs: [],
      waitingForUpdate: false,
      ifPlot: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      g: [undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined, undefined],
      colors: ['black', 'red', 'blue', '#8E6B23', 'orange', '#00FFFF', 'purple', '#38B0DE', ' #458B74', '#215E21', '#00ff7F', '#00009C', '#99CC32', '#EAADEA', '#5F9F9F', '#FF1CAE']
    }
  },
  props: {
    id: {
      type: String,
      default: 'dygraph'
    },
    height: {
      type: String,
      default: '100%'
    },
    width: {
      type: String,
      default: '100%'
    },
    dimension: {
      type: Number,
      default: 19
    },
    graphData: {
      required: true
    },
    dataName: {
      required: true
    },
    graphOptions: {
    },
    graphStyle: {
      type: Object,
      default () {
        return {
          width: '100%',
          height: '500px'
        }
      }
    },
    oldLabel: {
      type: Array,
      default: new Array(19)
    },
    isCompare: {
      type: Boolean,
      default: false
    }
  },
  created () {
    for (let i = 0; i < this.dimension; i++) {
      this.graphs.push({id: i, obj: undefined})
    }
  },
  mounted () {
    this.renderGraph()
  },
  methods: {
    gegraphid (id) {
      return 'graph' + id
    },
    gelabelid (id) {
      return 'labeldiv' + id
    },
    renderGraph () {
      let dataNum = this.graphData.length
      let indexNum = this.graphData[0].length
      let dataLength = this.graphData[0][0].length
      if (this.isCompare) {
        let colors = []
        for (let i = 0; i < dataNum; i++) {
          this.dataName[i] = this.dataName[i] + '_' + this.oldLabel[i]
          colors.push(this.colors[this.oldLabel[i] - 1])
          // if (this.oldLabel[i] === 1 || this.oldLabel[i] === 3) {
          //   colors.push(this.colors[0])
          // } else if (this.oldLabel[i] === 4 || this.oldLabel[i] === 9) {
          //   colors.push(this.colors[1])
          // } else if (this.oldLabel[i] === 6 || this.oldLabel[i] === 10) {
          //   colors.push(this.colors[2])
          // } else if (this.oldLabel[i] === 2 || this.oldLabel[i] === 5) {
          //   colors.push(this.colors[3])
          // } else {
          //   colors.push(this.colors[4])
          // }
        }
        for (let k = 0; k < indexNum; k++) {
          let data = []
          for (let dl = 0; dl < dataLength; dl++) {
            data[dl] = []
            data[dl][0] = dl + 1
            for (let dn = 0; dn < dataNum; dn++) {
              data[dl][dn + 1] = this.graphData[dn][k][dl]
            }
          }
          /* eslint-disable no-new */
          if (this.ifPlot[k]) {
            this.g[k].destroy()
          } else {
            this.ifPlot[k] = true
          }
          this.g[k] = new Dygraphs(document.getElementById('graph' + k), data, {labels: ['x'].concat(this.dataName), labelsDiv: 'labeldiv' + k, colors: colors, valueRange: [-0.2, 1]})
        }
      } else {
        for (let k = 0; k < indexNum; k++) {
          let data = []
          for (let dl = 0; dl < dataLength; dl++) {
            data[dl] = []
            data[dl][0] = dl + 1
            for (let dn = 0; dn < dataNum; dn++) {
              data[dl][dn + 1] = this.graphData[dn][k][dl]
            }
          }
          /* eslint-disable no-new */
          if (this.ifPlot[k]) {
            this.g[k].destroy()
          } else {
            this.ifPlot[k] = true
          }
          this.g[k] = new Dygraphs(document.getElementById('graph' + k), data, {labels: ['x'].concat(this.dataName), labelsDiv: 'labeldiv' + k, valueRange: [-0.2, 1]})
        }
      }
    }
  },
  watch: {
    'graphData': {
      handler (val, oldVal) {
        this.renderGraph()
      },
      deep: true
    },
    'isCompare': {
      handler (val, oldVal) {
        this.renderGraph()
      },
      deep: true
    }
  }
}
</script>

<style scoped>
  .graph {
    width: 95%;
    height: 100px;
    background-color: #eeeeee;
    margin-left: 20px;
  }
  .dimension-label {
    position: absolute;
  }
</style>
