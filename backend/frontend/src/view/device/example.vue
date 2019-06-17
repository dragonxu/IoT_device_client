<template>
  <div id="dom111"></div>
</template>

<script>
  import echarts from 'echarts'
  import { on, off } from '@/libs/tools'
  export default {
    name: 'Example',
    data() {
      return {
        value1: false,
        dom: null,
        option: {
        title: {
            text: '近期数据波动'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['湿度','温度']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['-11','-9','-7','-5','-3','-1','now']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name:'湿度',
                type:'line',
                data:[50, 51, 55, 52, 53, 50, 55]
            },
            {
                name:'温度',
                type:'line',
                data:[20, 20.2, 22, 21, 23, 21, 22]
            },
          ]
        }
      }
    },
    methods: {
      resize() {
        this.dom.resize()
      }
    },
    mounted() {
      this.value1 = true
      this.dom = echarts.init(document.getElementById('dom111'))
      this.dom.setOption(this.option)
      console.log('table', this.dom)

      // this.$nextTick(() => {
      //   this.dom = echarts.init(this.$refs.dom111)
      //   this.dom.setOption(this.option)
      //   on(window, 'resize', this.resize)
      // })
    },
    // beforeDestroy() {
    //   off(window, 'resize', this.resize)
    // },
  }
</script>
