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
            <FormItem label="ip地址" prop="ip">
                <Input v-model="formValidate.ip" placeholder="请输入正确的IP地址：例如：192.168.1.10" style="width: 50%"></Input>
            </FormItem>
            <FormItem label="端口号" prop="port" placeholder="例如：502"  >
                <Input v-model="formValidate.port" number style="width: 50%"></Input>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('formValidate')">确认</Button>
                <Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button>
            </FormItem>
        </Form>
    </template>
    <script>
        export default {
            name: 'TCP_device',
            data () {
                // 注意写在return上方
                const checkIP= (rule, value, callback) =>{
                    let ipRegex =  /(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}/g
                    if (value === '') {
                        callback(new Error('Please enter your ip'))
                    }
                    else if(!ipRegex.test(value)){
                        callback(new Error('Please enter correct ip'))
                    }
                    else{
                        callback();
                    }
                };
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
                const checkPort = (rule, value, callback) => {
                    value = value-0
                    if(!value){
                        callback(new Error('please enter correct port(1-65535)'))
                    }
                    else if(value < 0 || value > 65535)
                        callback(new Error('please enter correct port(1-65535)'))
                    else
                        callback();
                };
                return {
                    formValidate: {
                        name: '',
                        description: '',
                        ip: '127.0.0.1',
                        port: null,
                        slave: '',
                    },
                    // 写在return中
                    ruleValidate: {
                        name: [
                            { required: true, message: 'The name cannot be empty', trigger: 'blur' }
                        ],
                        description: [
                            { required: false, message: 'Mailbox cannot be empty', trigger: 'blur' },
                        ],
                        ip: [
                            { required: true, validator: checkIP, trigger: 'blur' }
                        ],
                        port: [
                            { required: true, validator: checkPort, trigger: 'blur' }
                        ],
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
                            this.$Message.success('Success!');
                        } else {
                            this.$Message.error('Fail!');
                        }
                    })
                },
                handleReset (name) {
                    this.$refs[name].resetFields();
                }
            }
        }
    </script>
    