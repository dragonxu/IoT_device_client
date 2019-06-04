<template>
  <div>
    
    <Row>
        <Col><h1>Mqtt Topic配置</h1></Col>
        <Col offset="20"> 
            <Button type="primary" @click="addTopic" size='large'>定义Topic</Button>
        </Col>
    </Row>
    <Divider></Divider>

    <Table
    ref="table"
    :columns="columns1"
    :data="topicList"
    stripe
    size='large'
  ></Table>

    <Modal v-model="show" title="Common Modal dialog box title" draggable>
        <p slot="header">定义Topic</p>
        <Card dis-hover :bordered="false">
            <Form ref="newTopic" :model="formValidate" :rules="ruleValidate">
                <FormItem label="Topic类" prop="topic">
                    <Input  v-model="formValidate.topic" placeholder="请填写Topic"></Input>
                </FormItem>
                <FormItem label="操作功能" prop="function_des">
                    <Input v-model="formValidate.function_des" placeholder="例如：connect"></Input>
                </FormItem>
                <FormItem label="描述" prop="description">
                    <Input type="textarea" :rows="4"  v-model="formValidate.description" placeholder="请填写描述信息"></Input>
                </FormItem>
                <FormItem label="标签" prop="tag">
                    <Input  v-model="formValidate.tag"></Input>
                </FormItem>
            </Form>
        </Card>
        <div slot="footer">
            <Button type="primary" v-if="edit" @click="handleSubmit('newTopic')">确认修改</Button>
            <Button type="primary" v-if="edit" @click="show=false">取消</Button>
            <Button type="primary" v-if="!edit" @click="handleSubmit('newTopic')">确定</Button>
            <Button  v-if="!edit" @click="handleReset('newTopic')" style="margin-left: 8px">重置</Button>
        </div>
    </Modal>

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
            <Button type="error" size="large" long  @click="del">Delete</Button>
        </div>
    </Modal>
  </div>
</template>

<script>
  import axios from '@/libs/api.request'
  export default {
    name: 'mqtt_topic',
    data() {
      return {
        show: false,
        del_confirm: false,
        temp_topic: '',
        topicList: [],
        edit: false,
        formValidate:{
            topic: '',
            function_des:'',
            description: '',
            tag: ''
        },
        ruleValidate: {
            topic: [
                { required: true, message: 'The topic cannot be empty', trigger: 'blur' }
            ],
            function_des: [
                { required: true, message: 'Description cannot be empty', trigger: 'blur' },
            ],
        },
        columns1: [
        {
            title: 'Topic',
            key: 'topic',
            width: 260,
            sortable: true
          },
          {
            title: '功能',
            key: 'function_des',
            width: 150,
            sortable: true
          },
          {
            title: '描述',
            key: 'description',
          },
          {
            title: '标签',
            key: 'tag',
            width: 120,
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
                    props: {
                    },
                    style: {
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                        this.edit = true
                        this.temp_topic = params.row.topic
                        this.formValidate = params.row
                        this.show = true
                      }
                    }
                  },
                  '编辑 / '
                ),
                h(
                  'a',
                  {
                    style: {
                      marginLeft: '0px'
                    },
                    on: {
                      click: () => {
                          this.del_confirm = true
                          this.temp_topic = params.row.topic
                      }
                    }
                  },
                  '删除'
                ),
              ])
            }
          }
        ]
      }
    },
    methods: {
      addTopic() {
        this.edit = false
        this.show = true
      },
      handleSubmit (name) {
        this.$refs[name].validate((valid) => {
            if (valid) {
                if(!this.edit){
                    axios.request({
                        url: 'api/gateway/createTopic',
                        method: 'post',
                        data: this.formValidate
                    })
                    .then(res=>{
                        console.log(res.data)
                        if(res.data.msg == 'ok'){
                            this.get_all_topic()
                            this.$Notice.success({
                                title: 'Note:',
                                desc: '创建成功！'
                                });
                            }
                        else{
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
            else{
                let data = this.formValidate
                data.before_edit = this.temp_topic
                axios.request({
                        url: 'api/gateway/editTopic',
                        method: 'post',
                        data: data
                    }).then(res=>{
                        console.log(res.data)
                        if(res.data.msg == 'ok'){
                            this.get_all_topic()
                            this.$Notice.success({
                                title: 'Note:',
                                desc: '修改成功'
                                });
                            }
                        else{
                            this.$Notice.error ({
                            title: 'Note:',
                            desc: '修改失败！'
                            });
                        }
                })
                .catch(error => {
                console.log(error)
          })
            }
                this.show = false
            }
             else {
                this.$Message.error('请填写正确参数!');
            }
        })
    },
    handleReset (name) {
        this.$refs[name].resetFields();
        },

    get_all_topic(){
    axios.request({
        url: 'api/gateway/getAllTopic',
    })
    .then(response=>{
        console.log(response.data)
        if (response.data.msg == 'ok')
        this.topicList = response.data.data
    //   this.$store.commit('update_gateway_list', response.data.data)
    })
    .catch(error=>{
        console.log('get all topic fail')
        console.log(error)
    })
    },
    del(){
        axios.request({
            url: 'api/gateway/delTopic',
            method: 'post',
            data:{
                topic: this.temp_topic
            }
        })         
        .then(res => {
            console.log(res.data)
            if(res.data.msg=='ok'){
                    this.$Message.success('删除成功')
                    this.get_all_topic()
                }
            else
                this.$Message.success('删除失败')
            this.del_confirm = false
        })
        .catch(error => {
            console.log(error)
        })
    }
    },
    mounted() {
        this.get_all_topic()
    },
  }
</script>
