<template>
  <div>
    <h1>网关：{{ gateway_name }}</h1>
    <Divider style="padding: 0%"></Divider>
    <Button type="primary" icon="md-add-circle" @click='create_tcp'>添加TCP设备</Button>
    <Button  icon="md-add" @click='create_rtu'>添加RTU设备</Button>
    <Divider></Divider>
    <tcp-device v-show="show_view=='tcp'"></tcp-device>
    <rtu-device v-show="show_view=='rtu'"></rtu-device>
  </div>
</template>

<script>
  import RTU_device from './RTU_device.vue'
  import TCP_device from './TCP_device.vue'
  export default {
    data() {
      return {
        show_view: '',
        gateway_name: ''
      }
    },
    components:{
        'tcp-device': TCP_device,
        'rtu-device': RTU_device
    },
    methods: {
        create_tcp(){
            this.show_view ='tcp'

        },
        create_rtu(){
            this.show_view = 'rtu'
        }
    },
    mounted() {
      // 获取路由参数
      this.gateway_name = this.$route.params.gateway_name
    }
  }
</script>
