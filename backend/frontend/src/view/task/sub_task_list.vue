<template>
  <div>
    <Table ref="recordTable" :columns="recordColumns" :data="recordList" stripe></Table>
    <Modal v-model="del_confirm" width="360">
      <p slot="header" style="color:#f60;text-align:center">
        <Icon type="ios-information-circle"></Icon>
        <span>Delete confirmation</span>
      </p>
      <div style="text-align:center">
        <p>确定删除？</p>
        <p>Will you delete it?</p>
      </div>
      <div slot="footer">
        <Button type="error" size="large" long >Delete</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
  import axios from '@/libs/api.request'
  export default {
    name: 'sub_task_list',
    data() {
      return {
        del_confirm: false,
        recordList: [],
        recordColumns: [
          {
            title: 'Slave',
            key: 'slave_id',
            width: 120,
            sortable: true
          },
          {
            title: '数据描述',
            key: 'function_name',
            width: 120
          },
          {
            title: '标识符',
            key: 'identifier',
            width: 120,
            sortable: true
          },
          {
            title: '采集地址',
            key: 'start_address',
            width: 120,
            sortable: true
          },
          {
            title: '状态',
            key: 'active_status',
            width: 120,
            render: (h, params) => {
              if (params.row.active_status == 'true') {
                return h('div', [
                  'on',
                  h('i-switch', {
                    props: {
                      disabled: true,
                      value: true
                    }
                  })
                ])
              } else {
                return h('div', [
                  'off',
                  h('i-switch', {
                    props: {
                      disabled: true,
                      value: false
                    }
                  })
                ])
              }
            }
          },
          {
            title: '功能码',
            key: 'modbus_function_code',
            width: 80,
            sortable: true
          },
          {
            title: '数据长度',
            key: 'data_length',
            width: 120
          },
          {
            title: '计算公式',
            key: 'compute',
            width: 120,
            sortable: true
          },
          {
            title: '发送方式',
            key: 'send_way',
            width: 120,
            sortable: true
          },
          {
            title: '操作',
            key: 'aa',
            // width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h(
                  'a',
                  {
                    style: {
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                        this.chnge_status(params.row.slave_id, params.row.start_address)
                        if (params.row.active_status == 'false') {
                          params.row.active_status = 'true'
                        } else {
                          params.row.active_status = 'false'
                        }
                      }
                    }
                  },
                  '切换状态 / '
                ),
                h(
                  'a',
                  {
                    props: {
                      // type: 'primary',
                      // size: 'small'
                    },
                    style: {
                      // width: '80%',
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                        console.log('111111111')
                      }
                    }
                  },
                  '编辑 /'
                ),
                h(
                  'a',
                  {
                    style: {
                      // width: '80%',
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                        this.delateRecord(params.row.slave_id, params.row.start_address)
                      }
                    }
                  },
                  ' 删除'
                )
              ])
            }
          }
        ]
      }
    },
    methods: {
      get_all_record() {
        axios
          .request({
            url: 'api/task/getAllRecord'
          })
          .then(response => {
            console.log(response.data)
            if (response.data.msg == 'ok') this.recordList = response.data.data
          })
          .catch(error => {
            console.log('get all record fail')
            console.log(error)
          })
      },

      chnge_status(slave_id, start_address) {
        axios
          .request({
            url: 'api/task/changeStatus',
            method: 'post',
            data: {
              slave_id: slave_id,
              start_address: start_address
            }
          })
          .then(response => {
            console.log(response.data)
            if (response.data.msg == 'ok') this.get_all_record()
          })
          .catch(error => {
            console.log(error)
          })
      },

      //   删除一条记录
      delateRecord(slave_id, start_address) {
        axios
          .request({
            url: 'api/task/deleteRecord',
            method: 'post',
            data: {
              slave_id: slave_id,
              start_address: start_address
            }
          })
          .then(response => {
            console.log(response.data)
            if (response.data.msg == 'ok') this.get_all_record()
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    mounted() {
      console.log('sub_task_record')
      this.get_all_record()
    }
  }
</script>
