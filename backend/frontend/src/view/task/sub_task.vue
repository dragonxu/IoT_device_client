<template>
  <div>
    <h1>任务：{{ $route.params.task_name }}</h1>
    <p>状态：</p>
    <i-switch v-model="collect_status" disabled>
      <span slot="open">开</span>
      <span slot="close">关</span>
    </i-switch>
    <br />
    <Button type="primary" icon="md-add-circle" @click="handleAdd" style="margin-left: 10px">添加记录</Button>
    <Button  @click="exportData(1)" style="margin-left: 10px"
      ><Icon type="ios-download-outline"></Icon>导出源数据</Button
    >
    <Button  @click="exportData(2)" style="margin-left: 10px"
      ><Icon type="ios-download-outline"></Icon>导出排序和过滤后的数据</Button
    >
    <Divider></Divider>
    <Tabs value="name1">
        <TabPane label="Modbus通讯地址表" name="name1">
          <v-subtasklist ref="sub"></v-subtasklist></TabPane>
        <TabPane label="标签二" name="name2"></TabPane>
    </Tabs>

    <Modal v-model="add_show" title="Common Modal dialog box title" :styles="{top: '0px'}" draggable>
        <p slot="header">添加记录</p>
        <Card dis-hover :bordered="false">
            <Form ref="reocrd" :model="formValidate" :rules="ruleValidate" :label-width="100">
                <FormItem label="操作类型" prop="modbus_function_code" number>
                    <Select v-model="formValidate.modbus_function_code" style="width:330px">
                        <Option v-for="(item, index) in modbus_func_list"  :key='item.value' :value="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem label="选择设备" prop="slave_id">
                    <Select v-model="formValidate.slave_id" style="width:330px">
                        <Option v-for="(item, index) in device_list"  :key='item.value' :value="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>

                <FormItem label="起始地址" prop="start_address">
                    <Row>
                        <Col span="18">
                          <Input  v-model="formValidate.start_address" placeholder="寄存器或线圈地址" number></Input>
                        </Col>
                        <Col span="4" offset="1">
                        </Col>
                    </Row>
                </FormItem>

                <FormItem label="结束地址" prop="stop_address" >
                    <Row>
                        <Col span="18">
                          <Input  v-model="formValidate.stop_address" placeholder="寄存器或线圈地址" number></Input>
                        </Col>
                        <Col span="4" offset="1">
                            <Button @click="show_attribute=true">详细配置>></Button>
                        </Col>
                    </Row>
                </FormItem>

                <FormItem label="原始数据类型" prop="data_length" number>
                    <Select v-model="formValidate.data_length" style="width:330px">
                        <Option v-for="(item, index) in data_size_list"  :key='item.value' :value="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>

                <FormItem label="缩放因子" prop="scale" number>
                    <Input v-model="formValidate.scale"></Input>
                </FormItem>
                
                <FormItem label="采集间隔（秒）" prop="interval" number>
                    <Input v-model="formValidate.interval"></Input>
                </FormItem>
                
                <FormItem label="数据上报方式" prop="send_way" >
                    <RadioGroup v-model="formValidate.send_way">
                        <Radio label="time">按时上报</Radio>
                        <Radio label="change">变更上报</Radio>
                    </RadioGroup>
                </FormItem>
                <Button  type="primary" @click='go_forward'>
                    高级选项
                    <Icon type="ios-arrow-forward" />
                </Button>
            </Form>
        </Card>
        <div slot="footer">
            <Button type="primary" v-if="edit" @click="handleSubmit('reocrd')">确认修改</Button>
            <Button type="primary" v-if="edit" @click="show=false">取消</Button>
            <Button type="primary" v-if="!edit" @click="handleSubmit('reocrd')">确定</Button>
            <Button  v-if="!edit" @click="handleReset('reocrd')" style="margin-left: 8px">重置</Button>
        </div>
    </Modal>

    <Modal v-model="show_high" title="Common Modal dialog box title" draggable>
        <p slot="header">高级选项</p>
        <Card dis-hover :bordered="false">

            <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
                <FormItem label="量程上限" prop="top_limit" number>
                    <Input v-model="formValidate.top_limit" placeholder="输入量程上限"></Input>
                </FormItem>
                <FormItem label="量程下限" prop="low_limit" number>
                    <Input v-model="formValidate.low_limit" placeholder="输入量程下限"></Input>
                </FormItem>
                <Poptip trigger="hover" title="提示" word-wrap width="300" 
                  content="可以自定义一个公式来计算最终希望得到的数据，公式中用X代表原始二进制数据解析后的值。">
                    <FormItem label="计算公式" prop="compute">
                        <Input v-model="formValidate.compute" type="textarea" :rows="4" ></Input>
                    </FormItem>
                </Poptip>
            </Form>
        </Card>
        <div slot="footer">
            <Button type="primary" @click="go_back">确定并返回</Button>
            <!-- <Button @click="add_show=true" style="margin-left: 8px">返回</Button> -->
        </div>
    </Modal>
    <!--  穿梭框 -->
    <v-addAttribute :show_attribute='show_attribute'></v-addAttribute>
  </div>
</template>

<script>
  import axios from '@/libs/api.request'
  import sub_task_list from './sub_task_list.vue'
  import addAttribute from './addAttribute'
  export default {
    name: 'sub_task',
    props: ['collect_status'],
    components: {
      'v-subtasklist': sub_task_list,
      'v-addAttribute': addAttribute
    },

    data() {
      const checkAddress= (rule, value, callback) =>{
            // 转为整形
            value = value -0
            if (isNaN(value))
                callback(new Error('请输入一个整数！'))
            else
                callback();
        };

      return {
        attribute: [],
        edit: false,
        add_show: false,
        show_high: false,
        show_attribute: false,
        device_list: [],
        formValidate:{
          gateway: this.$route.query.gateway,
          slave_id: 1,
          start_address: null,
          stop_address: null,
          function_name: [],
          modbus_function_code: 3,
          identifier: [],
          data_length: 16,
          top_limit: -1,
          low_limit: -1,
          scale: 1,
          interval: 5,
          send_way: 'time',
          compute: ''
        },
        ruleValidate: {
          start_address: [
              { required: true, validator: checkAddress, trigger: 'blur' },
          ],
          stop_address: [
              { required: true, validator: checkAddress, trigger: 'blur' },
          ],
        },
        send_way_list:[
          {
            value: 'time',
            label: '按时上报'
          },
          {
            value: 'change',
            label: '变更上报'
          }
          
        ],
        modbus_func_list:[
          {
            value: 1,
            label: '线圈状态 (只读，01)'
          },
          {
            value: 2,
            label: '离散量输入 (只读，02)'
          },
          {
            value: 3,
            label: '保持寄存器 (只读，03)'
          },
          {
            value: 4,
            label: '输入寄存器 (只读，04)'
          },
          {
            value: 5,
            label: '线圈状态 (读写，读取使用01，写入使用05)'
          },
          {
            value: 6,
            label: '保持寄存器 (读写，读取使用03，写入使用06)'
          },
          {
            value: 7,
            label: '线圈状态 (读写，读取使用01，写入使用0F)'
          },
          {
            value: 8,
            label: '保持寄存器 (读写，读取使用03，写入使用10)'
          },
        ],
        data_size_list: [
          {
            value: 1,
            label: 1
          },
          {
            value: 8,
            label: 8
          },
          {
            value: 16,
            label: 16
          },
          {
            value: 32,
            label: 32
          },
        ]
      }
    },
    methods: {
      handleAdd(){
        this.add_show=true
        this.formValidate.function_name = []
        this.formValidate.identifier = []
      },
      go_forward(){
        this.add_show = false
        this.show_high = true
      },

      go_back(){
        this.show_high = false,
        this.add_show = true
      },

      getAlldevice(){
        axios
          .request({
            url: 'api/device/getAll',
            methods: 'post',
            data:{
              gateway_name: this.$route.query.gateway
            }
          })
          .then(res => {
            if (res.data.msg == 'ok'){
              let data = res.data.data
              for(let i in data){
                this.device_list.push(
                  {
                    value: data[i]['slave'],
                    label: data[i]['name']
                  })
              }
              console.log('device: ', this.device_list)
            }
            else this.$Message.success('获取设备信息失败！')
          })
          .catch(error => {
            console.log(error)
          })
      },

      handleSubmit (name) {
          this.$refs[name].validate((valid) => {
              if (valid) {
                console.log(this.formValidate)
                if(this.formValidate.function_name.length != (this.formValidate.stop_address - this.formValidate.start_address+1))
                {
                  this.$Notice.error ({
                    title: 'Note:',
                    desc: '地址数与标识符数目无法对应！'
                  })
                  return
                }
                axios.request({
                    url: 'api/task/addRecord',
                    method: 'post',
                    data: this.formValidate
                  })
                  .then(res=>{
                      console.log(res.data)
                      if(res.data.msg == 'ok')
                      {
                        this.add_show = false
                        this.$refs.sub.get_all_record()
                          // this.get_all_task()
                        this.$Notice.success({
                            title: 'Note:',
                            desc: '成功'
                            });
                          }
                      else
                      {
                          this.$Notice.error ({
                          title: 'Note:',
                          desc: '创建失败！'
                          });
                      }
                      
                  })
                  .catch(error => {
                      console.log(error)
                  })
                }
                else {
                  this.$Message.error('请填写正确参数!');
                }
            })
          },
      exportData(type) {
      //   if (type === 1) {
      //     this.$refs.sub.exportCsv({
      //       filename: 'The original data'
      //     })
      //   } else if (type === 2) {
      //     this.$refs.table.exportCsv({
      //       filename: 'Sorting and filtering data',
      //       original: false
      //     })
      //   }
      },
      handleReset (name) {
          this.$refs[name].resetFields();
        },
    },
    mounted() {
      console.log(this.$route.params)
      console.log(this.$route.query)
      this.getAlldevice()
    }
  }
</script>
