<template>
  <div>
    <Row :gutter="20">
        <i-col :xs="12" :md="8" :lg="4" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
          <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="30">
            <count-to :end="infor.count" count-class="count-style"/>
            <p>{{ infor.title }}</p>
          </infor-card>
        </i-col>
      </Row>
  </div>
</template>

<script>
  import axios from '@/libs/api.request'
  import InforCard from '_c/info-card'
  import CountTo from '_c/count-to'
  export default {
    data() {
      return {
        inforCardData: [
          { title: '今日设备消息量', icon: 'md-locate', count: 232, color: '#19be6b' },
          { title: '设备在线时长 (分钟)', icon: 'md-help-circle', count: 142, color: '#ff9900' },
          { title: '异常警报', icon: 'md-chatbubbles', count: 12, color: '#E46CBB' },
          { title: '设备总数', icon: 'md-map', count: 14, color: '#9A66E4' }
        ]
      }
    },
    components: {
      InforCard,
      CountTo,
    },

    methods: {}
  }
</script>
<style lang="less">
  .count-style{
    font-size: 50px;
  }
</style>