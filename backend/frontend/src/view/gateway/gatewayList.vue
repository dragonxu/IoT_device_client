<template>
  <div>
    <Table ref="selection" border stripe :columns="columns7" :data="data6" 
    @on-select="handleSelect" @on-select-cancel='handleCancle'></Table>
    <br>
    <Button @click="handleSelectAll(true)">全选</Button>
    <Button @click="handleSelectAll(false)">取消全选</Button>
    
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
        columns7: [
          {
          type: 'selection',
          width: 60,
          align: 'center'
          },
          {
            title: '名称',
            key: 'gateway_name',
            sortable: true
          },
          {
            title: '描述',
            key: 'description'
          },
          {
            title: '子设备数',
            key: 'sub_device',
            sortable: true,
            width: 130,
            align: 'center'
          },
          {
            title: '创建时间',
            key: 'create_date',
            width: 150,
            align: 'center',
            sortable: true,
          },
          {
            title: '管理',
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
                      // size: 'small'
                    },
                    style: {
                      width: '80%',
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                        this.$store.commit('change_gateway', params.row.gateway_name)
                        // console.log(this.$store.state.current_gateway)
                        this.$router.push({ path: '/device/device_manage'}) 
                      }
                    }
                  },
                  '管理子设备'
                ),
              ])
            }
          }
        ],
        data6: [
        ]
      }
    },
    methods: {
      handleSelectAll (status) {
          this.$refs.selection.selectAll(status);
          if (status == true){
            for(let i in this.data6){
              this.$parent.gateway_list.push(i.gateway_name)
            }
          }
          else
            this.$parent.gateway_list = []
      },
      handleSelect(selection, row){
        this.$parent.gateway_list.push(row.gateway_name)
      },
      handleCancle(selection, row){
        var data = this.$parent.gateway_list
        for(let i in data){
          if (data[i] == row.gateway_name){
            this.$parent.gateway_list.splice(i,1)
            return
        }
      }

      },
      // show(index) {
      //   this.$Modal.info({
      //     title: 'User Info',
      //     content: `Name：${this.data6[index].name}<br>Age：${this.data6[index].age}<br>Address：${
      //       this.data6[index].decription
      //     }`
      //   })
      // },
  

      get_all_gateway(){
        axios.request({
          url: 'api/gateway/getAll'
        })
        .then(response=>{
          console.log(response.data)
          if (response.data.msg == 'ok')
          this.data6 = response.data.data
          this.$store.commit('update_gateway_list', response.data.data)
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
