<template>
  <div>
    <Table
      ref="table"
      :loading="loading"
      :columns="columns1"
      :data="data1"
      stripe
      @on-select="selectOne"
      @on-select-cancel="cancleOne"
    ></Table>
    <br />
    <Button @click="handleSelectAll(true)">全选</Button>
    <Button @click="handleSelectAll(false)">取消全选</Button>
    <Row >
      <Col span="16">  
        
      </Col>
      <Col >
        <Button type="primary" size="large" @click="exportData(1)"
          ><Icon type="ios-download-outline"></Icon>导出源数据</Button
        >
        <Button type="primary" size="large" @click="exportData(2)"
          ><Icon type="ios-download-outline"></Icon>导出排序和过滤后的数据</Button
        >
      </Col>
    </Row>
  </div>
</template>
<script>
  //   import {get_all_device} from '@/api/user'
  import axios from '@/libs/api.request'
  import { mapMutations } from 'vuex'
  export default {
    // props: ['data1'],
    data() {
      return {
        loading: true,
        data1: [],
        columns1: [
          {
            type: 'selection',
            width: 40,
            align: 'center'
          },
          {
            title: '子设备ID',
            key: 'name',
            width: 120,
            sortable: true
          },
          {
            title: '网关',
            key: 'gateway_name',
            width: 120,
          },
          {
            title: '地址(slave)',
            key: 'slave',
            width: 120,
            sortable: true
          },
          {
            title: '子设备描述',
            key: 'description'
          },
          {
            title: '接入方式',
            key: 'protocal',
            // sortable: true,
            width: 120,
            filters: [
              {
                label: 'TCP设备',
                value: 1
              },
              {
                label: 'RTU设备',
                value: 2
              }
            ],
            filterMultiple: false,
            filterMethod(value, row) {
              if (value === 1) {
                return row.protocal == 'TCP'
              } else if (value === 2) {
                return row.protocal == 'RTU'
              }
            }
          },
          {
            title: '创建时间',
            key: 'create_time',
            sortable: true
          }
        ]
      }
    },
    methods: {
      ...mapMutations(['addDevice']),
      // 导出csv
      exportData(type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: 'The original data'
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: 'Sorting and filtering data',
            original: false
          })
        }
      },

      //   查询所有设备
      get_all_device() {
        this.loading = true
        axios
          .request({
            url: 'api/device/getAll',
            method: 'post',
            data: { gateway_name: this.$store.state.current_gateway }
          })
          .then(res => {
            console.log(res.data)
            //   this.$Message.success('成功')
            this.data1 = res.data.data
          })
          .catch(error => {
            console.log(error)
          })
        this.loading = false
      },

      // 选定一项
      selectOne(selection, row) {
        this.$store.commit('addDevice', {'gateway': row.gateway_name, 'name': row.name})
        // this.addDevice(row.name)
      },
      //   取消选定一项
      cancleOne(selection, row) {
        this.$store.commit('delateDevice', {'gateway': row.gateway_name, 'name': row.name})
      },
      // 全选、取消全选
      handleSelectAll(status) {
        if (status) {
          let temp = this.data1
          for (let i in temp) {
            this.$store.commit('addDevice', {'gateway': temp[i].gateway_name, 'name': temp[i].name})
          }
        } else {
          this.$store.commit('cleareDevice')
        }
        this.$refs.table.selectAll(status)
      }
    },
    mounted() {
      this.get_all_device()
    }
  }
</script>
