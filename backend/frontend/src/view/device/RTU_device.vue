<template>
    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
        <FormItem label="设备名" prop="name">
            <Input v-model="formValidate.name" placeholder="设备名必须唯一" style="width: 50%"></Input>
        </FormItem>
        <FormItem label="描述" prop="description">
            <Input type="textarea" :rows="4" v-model="formValidate.description" style="width: 50%" placeholder="请输入设备描述"></Input>
        </FormItem>
        <FormItem label="设备地址" prop="slave">
            <Input v-model="formValidate.slave" number placeholder="可输入1-247之间的整数值" style="width: 50%" ></Input>
        </FormItem>

        <FormItem label="波特率" prop="baudRate">
            <Select v-model="formValidate.baudRate" style="width:400px">
                <Option v-for="item in baudRateList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </FormItem>
        <FormItem label="数据位" prop="biteSize">
            <Select v-model="formValidate.biteSize" style="width:400px">
                <Option v-for="item in biteSizeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </FormItem>

        <FormItem label="校验" prop="parity">
            <Select v-model="formValidate.parity" style="width:400px">
                <Option v-for="item in parityList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </FormItem>
        <FormItem label="停止位" prop="stopbits">
            <Select v-model="formValidate.stopbits" style="width:400px">
                <Option v-for="item in stopbitsList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
        </FormItem>
        <FormItem>
            <Button type="primary" v-if="!edit" @click="handleSubmit('formValidate')">确认</Button>
            <Button type="primary" v-if="edit" @click="handleSubmit('formValidate')">修改</Button>
            <Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button>
        </FormItem>
    </Form>
</template>

<script>
    import axios from '@/libs/api.request'
    export default {
        name: 'add_rtu',
        data () {
            const checkSlave = (rule, value, callback) =>{
                // 转为整形
                value = value -0
                if (!value)
                    callback(new Error('please enter correct address(1-247)'))
                if (value < 0 || value > 247)
                    callback(new Error('please enter correct address(1-247)'))
                else
                    callback();
            };
            return {
                edit: false,
                baudRateList: [
                    {
                        value: '300',
                        label: '300'
                    },
                    {
                        value: '600',
                        label: '600'
                    },
                    {
                        value: '1200',
                        label: '1200'
                    },
                    {
                        value: '1440',
                        label: '1440'
                    },
                    {
                        value: '2440',
                        label: '2440'
                    },
                    {
                        value: '4800',
                        label: '4800'
                    },
                    {
                        value: '9600',
                        label: '9600'
                    },
                    {
                        value: '19200',
                        label: '19200'
                    },
                    {
                        value: '38400',
                        label: '38400'
                    },

                ],
                biteSizeList:[
                    {
                        value: 8,
                        label: 8
                    },
                    {
                        value: 7,
                        label: 7
                    }
                ],
                parityList:[
                    {
                        value: 'N',
                        label: '无校验'
                    },
                    {
                        value: 'E',
                        label: '奇校验'
                    },
                    {
                        value: 'O',
                        label: '偶校验'
                    },
                    {
                        value: 'M',
                        label: 'Mark'
                    },
                    {
                        value: 'S',
                        label: 'Space'
                    }
                ],
                stopbitsList:[
                    {
                        value: 1,
                        label: 1
                    },
                    {
                        value: 1.5,
                        label: 1.5
                    },
                    {
                        value: 2,
                        label: 2
                    }

                ],
                formValidate: {
                    name: '',
                    edit_name : '',
                    description: '',
                    baudRate: '9600',
                    biteSize: 8,
                    parity: 'N',
                    stopbits: 1,
                    slave: '',
                    gateway_name: this.$store.state.current_gateway
                },
                // 写在return中
                ruleValidate: {
                    name: [
                        { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                    ],
                    baudRate: [
                        { required: true, message: 'cannot be empty', trigger: 'blur' }
                    ],
                    // biteSize: [
                    //     { required: true, message: 'cannot be empty', trigger: 'blur' }
                    // ],
                    parity: [
                        { required: true, message: 'Cannot be empty', trigger: 'blur' }
                    ],
                    // stopbits: [
                    //     { required: true, message: 'cannot be empty', trigger: 'blur' }
                    // ],
                    slave: [
                        { required: true, validator: checkSlave, trigger: 'blur' }
                    ],
                }
            }
        },
        methods: {
            handleSubmit (name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        axios.request({
                            url: 'api/device/create_rtu',
                            method: 'post',
                            data: this.formValidate
                        }).then(res=>{
                            console.log(res.data)
                            // this.$Message.success('创建成功')
                            if(res.data.msg == 'ok'){
                                this.$Notice.success({
                                    title: 'Note:',
                                    desc: '成功'
                                    });
                                this.$router.push('/device/device_manage')
                                // this.$parent.show_view = ''
                                }
                            else{
                                this.$Notice.error ({
                                title: 'Note:',
                                desc: '创建失败！'
                                });
                            }
                        })
                        .catch(error=>{
                            console.log(error)
                            this.$Notice.error ({
                                title: 'Notification title',
                                desc: '创建失败！'
                                });
                        })
                    } else {
                        this.$Message.error('请填写正确参数!');
                    }
                })
            },
            handleReset (name) {
                this.$refs[name].resetFields();
            }
        },
        mounted() {
            let query = this.$route.query
            console.log('参数：',query)
            if(query){
                this.formValidate.edit_name = query.name
                this.formValidate.name = query.name
                this.formValidate.description = query.description
                this.formValidate.slave = query.slave
                if(query.edit){
                    this.edit = true
                }
            }
        },
    }

</script>
