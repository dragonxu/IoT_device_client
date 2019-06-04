<template>
  <div id="gateway">
    <h2>>>网关配置</h2>
    <Divider></Divider>
    <Button type="primary" @click="modal1 = true" icon="md-add-circle" >新建网关</Button>
    <Button type="warning" :disabled="button_disabled" @click="del_confirm">删除</Button>
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
        <!-- 删除确认 -->
    <Modal v-model="modal2" width="360">
        <p slot="header" style="color:#f60;text-align:center">
            <Icon type="ios-information-circle"></Icon>
            <span>Delete confirmation</span>
        </p>
        <div style="text-align:center">
            <p>删除网关{{ $store.state.current_gateway }}其子设备也一并删除</p>
            <p>是否继续？</p>
        </div>
        <div slot="footer">
            <Button type="error" size="large" long @click="remove">删除</Button>
        </div>
        </Modal>
 
    <Divider></Divider>
    <v-gatewaylist ref='gatewaylist'></v-gatewaylist>
  </div>
</template>

<script>
//  import { mapMutations } from 'vuex'
 import axios from '@/libs/api.request'
 import gatewayList from './gatewayList.vue'
 
  export default {
    data() {
      return {
        gateway_list: [],
        modal1: false,
        modal2: false,
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
    del_confirm() {
        this.modal2 = true
      },
    remove() {
    axios.request({
        url: 'api/gateway/delate',
        method: 'post',
        data:{name: this.gateway_list}
    })
    .then(res=>{
        if(res.data.msg === 'ok'){
            this.$Message.success('删除成功！')
            this.$refs.gatewaylist.get_all_gateway()
            this.gateway_list = []
            this.modal2 = false
        }
        else this.$Message.error('删除失败！')
            this.modal2 = false
    })
    .catch(error=>{
        // this.$Message.error('删除失败！')
        console.log(error)
        this.modal2 = false
    })

    // this.$parent.gateway_list.splice(index, 1)
    },
    handleReset (name) {
        this.$refs[name].resetFields();
            }
    }
  }
</script>
