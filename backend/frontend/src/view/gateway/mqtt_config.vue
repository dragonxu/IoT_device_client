<template>
   <div>
    <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80" size='large'>
        <FormItem label="主机地址(host)" prop="host" >
            <Input v-model="formValidate.host" placeholder="物联网平台地址" :disabled="edit" style="width: 50%"></Input>
        </FormItem>
        <FormItem label="端口号" prop="port">
            <Input v-model="formValidate.port" :disabled="edit" style="width: 50%"></Input>
        </FormItem>
        <FormItem label="认证口令(token)" prop="token">
            <Input v-model="formValidate.token" :disabled="edit" style="width: 50%"></Input>
        </FormItem>
        <FormItem label="缓存大小" prop="cache">
            <Input v-model="formValidate.cache" :disabled="edit" style="width: 20%"></Input>M/b
        </FormItem>
        <FormItem label="描述" prop="description">
            <Input type="textarea" :rows="4" v-model="formValidate.description" :disabled="edit" style="width: 50%" placeholder="请输入描述"></Input>
        </FormItem>
        <FormItem>
            <Button type="primary" :disabled='edit' @click="handleSubmit">提交</Button>
            <Button type="primary" :disabled="!edit" @click="handleEdit">修改</Button>
        </FormItem>
    </Form>
   </div>
</template>

<script>
import axios from '@/libs/api.request'
export default {
data() {
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
        edit: true,
        formValidate:{
            host: '60.205.202.24',
            port: '31883',
            token: 'ooYKWsZZXuGqDWkRYCPZ',
            description: '物联网平台',
            cache: 500
        },
        ruleValidate: {
            host: [
                { required: true, validator: checkIP, trigger: 'blur' }
            ],
            port: [
                { required: true, validator: checkPort, trigger: 'blur' }
            ],
            token: [
                { required: true, message: 'Cannot be empty', trigger: 'blur' }
            ],
        }
    }
    },
    methods: {
        handleSubmit(){
            this.edit = !this.edit
            axios.request({
                url: 'api/gateway/mqtt_config',
                data: {data: JSON.stringify(this.formValidate)},
                method: 'post'
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
          this.edit = true
        },
        handleEdit(){
            this.edit = false
        }
    },
    mounted() {
        let query = this.$route.query
        console.log('参数：',query)
        if(query){
            // this.formValidate.edit_name = query.name
            // this.formValidate.name = query.name
            // this.formValidate.description = query.description
            // this.formValidate.slave = query.slave
            if(query.edit){
                this.edit = true
            }
        }
    },
}
</script>