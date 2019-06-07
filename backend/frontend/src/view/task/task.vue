<template>
    <div>
        <h1>采集任务</h1>
        <Button type="primary" @click="addTask" icon="md-add-circle" >新建任务</Button>
        <Button type="warning" :disabled="button_disabled" @click='del_confirm=true'>删除</Button>
        <Divider></Divider>
        <Table
            ref="table"
            :columns="columns1"
            :data="taskList"
            stripe
            size='large'
            @on-select="selectOne"
            @on-select-cancel="cancleOne"
        ></Table>
      
        <Modal v-model="show" title="Common Modal dialog box title" draggable>
            <p slot="header">创建采集任务</p>
            <Card dis-hover :bordered="false">
                <Form ref="task" :model="formValidate" :rules="ruleValidate">
                    <FormItem label="项目名称" prop="name">
                        <Input  v-model="formValidate.name" placeholder="请填写项目名称"></Input>
                    </FormItem>
                    <FormItem label="工业协议" prop="protocol">
                        <RadioGroup v-model="formValidate.protocol">
                            <Radio label="Modbus"></Radio>
                            <Radio label="IEC 103" disabled></Radio>
                            <Radio label="OPC" disabled></Radio>
                        </RadioGroup>
                    </FormItem>
                    <FormItem label="数据来源" prop="gateway" v-if="!edit">
                        <Select v-model="formValidate.gateway" style="width:400px">
                            <Option v-for="item in $store.state.gateway_list" :value="item" :key="item">{{ item }}</Option>
                        </Select>
                    </FormItem>
                    <FormItem label="描述" prop="description">
                        <Input type="textarea" :rows="4"  v-model="formValidate.description" placeholder="请填写描述信息"></Input>
                    </FormItem>
                </Form>
            </Card>
            <div slot="footer">
                <Button type="primary" v-if="edit" @click="handleSubmit('task')">确认修改</Button>
                <Button type="primary" v-if="edit" @click="show=false">取消</Button>
                <Button type="primary" v-if="!edit" @click="handleSubmit('task')">确定</Button>
                <Button  v-if="!edit" @click="handleReset('task')" style="margin-left: 8px">重置</Button>
            </div>
        </Modal>
    
        <Modal v-model="del_confirm" width="360">
            <p slot="header" style="color:#f60;text-align:center">
                <Icon type="ios-information-circle"></Icon>
                <span>Delete confirmation</span>
            </p>
            <div style="text-align:center">
                <p>确定删除？{{select_task}}</p>
                <p>Will you delete it?</p>
            </div>
            <div slot="footer">
                <Button type="error" size="large" long @click='delateTask' >Delete</Button>
            </div>
          </Modal>
    </div>
</template>
      
<script>
import axios from '@/libs/api.request'
import sub_task from './sub_task'

export default {
    name: 'task',
    components:{
        'v-subtask': sub_task,
    },
    data() {
    return {
        show: false,
        del_confirm: false,
        collect_status: '',
        temp_task: '',
        taskList: [],
        select_task : [],
        edit: false,
        formValidate:{
            name: '',
            protocol: 'Modbus',
            gateway: '',
            description: '',
            create_time: ''
        },
        ruleValidate: {
            name: [
                { required: true, message: 'The name cannot be empty', trigger: 'blur' }
            ],
            gateway: [
                { required: true, message: 'Description cannot be empty', trigger: 'blur' },
            ],
        },
        columns1: [
        {
            type: 'selection',
            width: 50,
            align: 'center'
          },
        {
            title: '任务名称',
            key: 'name',
            width: 160,
            sortable: true,
            render: (h, params) => {
                return h('div', [
                    h('Icon', {
                        props: {
                            type: 'person'
                        }
                    }),
                    h('strong', params.row.name)
                ]);
            }
        },
        {
            title: '状态',
            key: 'status',
            width: 130,
            render: (h, params) => {
                if(params.row.status=='true'){
                    return h('div', [
                        'on',
                        h('i-switch', {
                            props: {
                                disabled: true,
                                value: true
                            },
                        }),
                    ]);
                }
                else{
                    return h('div', [
                            'off',
                            h('i-switch', {
                                props: {
                                    disabled: true,
                                    value: false
                                },
                            }),
                        ]);
                }
            }
        },
        {
            title: '协议',
            key: 'protocol',
            width: 100,
            sortable: true
        },
        {
            title: '描述',
            key: 'description',
        },
        {
            title: '数据来源',
            key: 'gateway',
            width: 100,
        },
        {
            title: '创建时间',
            key: 'create_time',
            width: 140,
        },
        {
            title: '数据来源',
            key: 'gateway',
            // width: 150,
            align: 'center',
            render: (h, params) => {
            return h('div', [
            h('a',
                {
                    style: {
                    marginLeft: '0px'
                    },
                    on: {
                        click: () => {
                            if(params.row.status == 'false')
                                {
                                    params.row.status = 'true'
                                    this.collect_status = true
                                    axios.request({
                                        url: 'api/task/startTask',
                                        method: 'post',
                                        data: {
                                            gateway: params.row.gateway
                                        }
                                    })
                                    .then(res => {
                                        console.log(res.data)
                                        if(res.data.msg=='ok')
                                          this.$Message.success('成功')
                                        else
                                          this.$Message.success('失败')
                                    })
                                    .catch(error => {
                                        console.log(error)
                                    })
                                }
                            else{
                                params.row.status = 'false'
                                this.collect_status = false
                            }
                        }
                    }
                    },
            '切换状态 / '),
            h('a',
                {
                    style: {
                        marginLeft: '0px'
                    },
                    on: {
                        click: () => {
                            this.edit = true
                            this.temp_task = params.row.name
                            this.formValidate = params.row
                            this.show = true
                        }
                    }
                },
                '编辑 / '),
            h('a',
                {
                    style: {
                    marginLeft: '0px'
                    },
                    on: {
                        click: () => {
                            this.$router.push({name: 'sub_task', 
                                params: {task_name: params.row.name},
                                query:{
                                    gateway: params.row.gateway
                                }
                            })
                        }
                    }
                    },
            '解析设置'),
            ])
            }
        }
        ]
    }
    },
    computed: {
        button_disabled(){
            if(this.select_task.length>0)
                return false
            else
                return true
        }
    },
    methods: {
        addTask() {
            this.edit = false
            this.show = true
        },
        selectOne(selection, row) {
            this.select_task.push(row.name)
            // this.addDevice(row.name)
        },
      //   取消选定一项
        cancleOne(selection, row) {
            for(let i in this.select_task){
                if (this.select_task[i] == row.name){
                    this.select_task.splice(i, 1)
                }
            }
        },
        delateTask(){
            axios.request({
                url: 'api/task/delete',
                method: 'post',
                data: {
                    name: this.select_task
                }
            })
            .then(res => {
                console.log(res.data)
                if(res.data.msg=='ok'){
                   this.$Message.success('删除成功')
                   this.get_all_task()
                   this.select_task = []
                }
                else
                    this.$Message.success('删除失败')
                this.del_confirm= false
                }   
            )
            .catch(error => {
                console.log(error)
            })


        },
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(!this.edit){
                        axios.request({
                            url: 'api/task/create',
                            method: 'post',
                            data: this.formValidate
                        })
                        .then(res=>{
                            console.log(res.data)
                            if(res.data.msg == 'ok')
                            {
                                this.get_all_task()
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
                else{
                    let data = this.formValidate
                    data.before_edit = this.temp_task
                    axios.request({
                            url: 'api/task/edit',
                            method: 'post',
                            data: data
                        }).then(res=>{
                            console.log(res.data)
                            if(res.data.msg == 'ok'){
                                this.get_all_task()
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

        get_all_task(){
            axios.request({
                url: 'api/task/getAll',
            })
            .then(response=>{
                console.log(response.data)
                if (response.data.msg == 'ok')
                this.taskList = response.data.data
            //   this.$store.commit('update_gateway_list', response.data.data)
            })
            .catch(error=>{
                console.log('get all task fail')
                console.log(error)
            })
        },
    },
    mounted() {
        this.get_all_task()
    },
}
</script>
