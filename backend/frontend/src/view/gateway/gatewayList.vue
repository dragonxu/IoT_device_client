<template>
  <div>
    <Table border :columns="columns7" :data="data6"></Table>
    <Modal v-model="modal2" width="360">
      <p slot="header" style="color:#f60;text-align:center">
        <Icon type="ios-information-circle"></Icon>
        <span>Delete confirmation</span>
      </p>
      <div style="text-align:center">
        <p>删除网关：{{del_gateway}}子设备将一并删除，</p>
        <p>是否继续删除？</p>
      </div>
      <div slot="footer">
        <Button type="error" size="large" long @click="remove">删除</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
  import axios from '@/libs/api.request'
  export default {
    name: 'gatewayList',
    // props: [data6],
    data() {
      return {
        modal2: false,
        del_gateway: '',
        columns7: [
          {
            title: '名称',
            key: 'gateway_name'
          },
          {
            title: '描述',
            key: 'description'
          },
          {
            title: '子设备数',
            key: 'sub_device'
          },
          {
            title: '创建时间',
            key: 'create_date'
          },
          {
            title: '创建时间',
            key: 'aa',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h(
                  'Button',
                  {
                    props: {
                      type: 'primary',
                      size: 'small'
                    },
                    style: {
                      width: '80%',
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                        this.show(params.index)
                      }
                    }
                  },
                  '管理子设备'
                ),
                h(
                  'Button',
                  {
                    props: {
                      type: 'error',
                      size: 'small'
                    },
                    style: {
                      // marginRight: '5px'
                      // padding: '10px'
                      width: '80%'
                    },
                    on: {
                      click: () => {
                        this.del_confirm(params.row.gateway_name);

                      }
                    }
                  },
                  '删除'
                )
              ])
            }
          }
        ],
        data6: [
        ]
      }
    },
    methods: {
      show(index) {
        this.$Modal.info({
          title: 'User Info',
          content: `Name：${this.data6[index].name}<br>Age：${this.data6[index].age}<br>Address：${
            this.data6[index].decription
          }`
        })
      },
      del_confirm(name) {
        console.log(name)
        this.modal2 = true
        this.del_gateway = name
      },
      remove() {
        axios.request({
          url: 'api/gateway/delate',
          method: 'post',
          data:{name: this.del_gateway}
        })
        .then(res=>{
          if(res.data.msg === 'ok')
            this.$Message.success('删除成功！')
          else this.$Message.error('删除失败！')
          this.modal2 = false
          this.get_all_gateway()
        })
        .catch(error=>{
          this.$Message.error('删除失败！')
          console.log(error)
        })

        // this.$parent.gateway_list.splice(index, 1)
      },
      get_all_gateway(){
        axios.request({
          url: 'api/gateway/getAll'
        })
        .then(response=>{
          console.log(response.data)
          if (response.data.msg == 'ok')
          this.data6 = response.data.data
        })
        .catch(error=>{
          console.log('get all gateway fail')
          console.log(error)
        })
      }
    },
    mounted() {
      this.get_all_gateway()
    },
  }
</script>
