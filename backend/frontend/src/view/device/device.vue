<template>
  <div>
    <!-- <h1>网关： {{ $store.state.current_gateway }}</h1> -->
    <!-- <Button type="text" ></Button><Icon type="ios-cog" size="25"/>选择网关:</Button> -->
    <h1>选择网关：</h1>
    <Select v-model="$store.state.current_gateway" style="width:200px" icon="ios-cog"  @on-change='selectGateway'>
        <Option v-for="(item, index) in  $store.state.gateway_list" :value="item" :key="index">{{ item }}</Option>
    </Select>
    <Divider style="padding: 0%"></Divider>
    <Button type="primary" icon="md-add-circle" @click="add_tcp">添加TCP设备</Button>
    <Button icon="md-add" @click="add_rtu">添加RTU设备</Button>
    <Button type="warning" :disabled="$store.getters.selected_device_count" @click="del_confirm">删除</Button>

    <!-- 删除确认 -->
    <Modal v-model="flag" width="360">
      <p slot="header" style="color:#f60;text-align:center">
        <Icon type="ios-information-circle"></Icon>
        <span>Delete confirmation</span>
      </p>
      <div style="text-align:center">
        <p>删除网关子设备：{{ $store.state.selected_device }}</p>
        <p>是否继续删除？</p>
      </div>
      <div slot="footer">
        <Button type="error" size="large" long @click="delate_device_a">删除</Button>
      </div>
    </Modal>
    <Divider></Divider>
    <router-view></router-view>
  </div>
</template>

<script>
  import axios from '@/libs/api.request'
  import { delate_device, get_all_device } from '@/api/device.js'
  import show_list from './show_list.vue'
  export default {
    data() {
      return {
        flag: false
      }
    },

    computed: {
      button_disabled() {
        if (this.$store.state.selected_device.length > 0) return false
        else return true
      }
    },

    methods: {
      del_confirm() {
        // 验证是否选定网关
        // if (!this.$store.state.current_gateway)
        //    this.$Message.warning('请先选择网关！')
        // else this.flag = true
        this.flag = true
      },

      delate_device_a() {
        // delate_device({ device: this.$store.state.selected_device, gateway_name: this.$store.state.current_gateway })
        delate_device({ device: JSON.stringify(this.$store.state.selected_device) })
          .then(res => {
            console.log(res.data)
            if (res.data.msg == 'ok') {
              this.$Message.success('删除成功！')
              // this.$store.commit('update_gateway_list', [])
              // this.$destroy()
              // this.$router.push('/gateway/gateway_config')
              this.$router.push('/device/device_manage')
            } else {
              this.$Message.success('删除失败！')
            }
          })
          .catch(error => {
            this.$Message.success('删除失败！')
            console.log(error)
          })
        this.flag = false
      },

      add_tcp() {
        this.$router.push({ name: 'add_tcp' })
      },

      add_rtu() {
        this.$router.push({ name: 'add_rtu' })
      },
      // 下拉选择网关
      selectGateway(value){
        this.$store.commit('change_gateway', value)
      }
    },
    // created() {
    //   获取路由参数
    //   this.gateway_name = this.$route.params.gateway_name
    //   this.$store.commit('change_gateway', this.$route.params.gateway_name)
    // }
    mounted() {
      if (this.$store.state.current_gateway) {
        axios
          .request({
            url: 'api/gateway/getAll'
          })
          .then(response => {
            if (response.data.msg == 'ok') 
              this.$store.commit('update_gateway_list', response.data.data)
          })
      }
    },
    destroy(){
      this.$router.push('/gateway/gateway_config')
      console.log('销毁')
    }
  }
</script>
