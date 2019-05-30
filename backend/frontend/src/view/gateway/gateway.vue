<template>
  <div id="gateway">
    <h2>>>网关配置</h2>
    <Divider></Divider>
    <Button type="primary" @click="modal1 = true">新建网关</Button>
    <Button type="warning" :disabled="button_disabled">删除</Button>
    <Modal v-model="modal1" title="Common Modal dialog box title" :styles="{top: '150px'}">
        <p slot="header">新建网关</p>
        <Card dis-hover :bordered="false">
            
            <Form ref="formValidate" :model="formValidate" :rules="ruleValidate">
            <FormItem label="网关名称" prop="gateway_name">
                <Input v-model="formValidate.gateway_name" placeholder="名称必须唯一"></Input>
            </FormItem>
            <FormItem label="描述" prop="description">
                <Input type="textarea" :rows="4"  v-model="formValidate.description" placeholder="请填写描述信息"></Input>
            </FormItem>
            
            </Form>
        </Card>
        <div slot="footer">
                <Button type="primary" @click="handleSubmit('formValidate')">确定</Button>
                <Button @click="handleReset('formValidate')" style="margin-left: 8px">重置</Button>
            </div>
    </Modal>
    <Divider></Divider>
    <v-gatewaylist ref='gatewaylist'></v-gatewaylist>
  </div>
</template>

<script>
 import axios from '@/libs/api.request'
 import gatewayList from './gatewayList.vue'
  export default {
    data() {
      return {
        gateway_list: [],
        modal1: false,
        formValidate:{
            gateway_name: '',
            description: ''
        },
        ruleValidate: {
            gateway_name: [
                { required: true, message: 'The id cannot be empty', trigger: 'blur' }
            ],
            description: [
                { required: true, message: 'Description cannot be empty', trigger: 'blur' },
            ],
        }
      }
    },
    components: {
        'v-gatewaylist': gatewayList,
    },
    computed: {
        button_disabled(){
            if(this.gateway_list.length>0){
                return false
            }
            else return true
        }
    },
    methods: {
      handleSubmit (name) {
        this.$refs[name].validate((valid) => {
        if (valid) {
            let data = this.$refs.gatewaylist.data6
            for(let i in data){
                if (data[i].gateway_name == this.formValidate.gateway_name){
                    this.$Message.error('网关名称已存在！')
                    return
                }
            }
            axios.request({
                url: 'api/gateway/new',
                method: 'post',
                data: {
                    gateway_name: this.formValidate.gateway_name,
                    description: this.formValidate.description
                }
            })
            .then((response) => {
                if(response.data.msg === 'ok'){
                    this.modal1 = false
                    this.$Message.success('创建成功！');
                    this.$refs.gatewaylist.get_all_gateway()
                    this.formValidate = {
                        gateway_name: '',
                        description: ''
                    }
                }
                else
                    this.$Message.error('创建失败1！');
            })
            .catch((error) => {
                this.modal1 = true
                console.log(error)
                this.$Message.error('创建失败2！');
            });
            
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
