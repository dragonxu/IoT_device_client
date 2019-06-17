<template>
  <div>
    <Row :gutter="20">
      <i-col :xs="12" :md="8" :lg="4" v-for="(infor, i) in inforCardData" :key="`infor-${i}`" style="height: 120px;padding-bottom: 10px;">
        <infor-card shadow :color="infor.color" :icon="infor.icon" :icon-size="36">
          <count-to :end="infor.count" count-class="count-style"/>
          <p>{{ infor.title }}</p>
        </infor-card>
      </i-col>
    </Row>
    <Row :gutter="20" style="margin-top: 10px;">
      <!-- <i-col :md="24" :lg="8" style="margin-bottom: 20px;"> -->
        <!-- <Card shadow>
          <chart-pie style="height: 300px;" :value="pieData" text="用户访问来源"></chart-pie>
        </Card> -->
      <!-- </i-col> -->
      <i-col :md="24" :lg="16" style="margin-bottom: 20px;">
        <Card shadow>
          <chart-bar style="height: 300px;" :value="barData" text="每周设备活跃量"/>
        </Card>
      </i-col>
    </Row>
    <Row>
      <Card shadow>
        <example style="height: 310px;"/>
      </Card>
    </Row>
  </div>
</template>

<script>
import axios from '@/libs/api.request'
// import Axios from 'axios'
// import axios from '@/libs/api.request'
// import axios from 'axios'
import InforCard from '_c/info-card'
import CountTo from '_c/count-to'
import { ChartPie, ChartBar } from '_c/charts'
import Example from './example.vue'
export default {
  name: 'home',
  components: {
    InforCard,
    CountTo,
    ChartPie,
    ChartBar,
    Example
  },
  data () {
    return {
      inforCardData: [
          { title: '今日设备消息量', icon: 'md-locate', count: 232, color: '#19be6b' },
          { title: '设备在线时长 (分钟)', icon: 'md-help-circle', count: 142, color: '#ff9900' },
          { title: '异常警报', icon: 'md-chatbubbles', count: 12, color: '#E46CBB' },
          { title: '设备总数', icon: 'md-map', count: 14, color: '#9A66E4' }
        ],
      pieData: [
      ],
      barData: {
        Mon: 1,
        Tue: 3,
        Wed: 5,
        Thu: 6,
        Fri: 3,
        Sat: 6,
        Sun: 4
      }
    }
  },
  mounted () {
    //
  },
  methods: {
    transform(data){
      let param = new URLSearchParams()
      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          param.append(key, data[key])
        }
      }
      return param;
  },
    test(){
      axios.request({
        method: 'post',
        url:'api/gateway/new', 
        data: {gateway_id: 'a', description: 'c'}
      })
      .then((response) => {
          console.log(response);
      })
      .catch((error) => {
          console.log(error);
      });
    }
  },
}
</script>

<style lang="less">
.count-style{
  font-size: 50px;
}
</style>
