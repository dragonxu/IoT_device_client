<template>
  <!-- 穿梭框 + 抽屉-->
  <Drawer title="Basic Drawer" :mask-closable="false" v-model="show_attribute" width="500">
    <Transfer
      :data="attribute"
      :target-keys="targetKeys1"
      :render-format="render1"
      filterable
      :filter-method="filterMethod"
      @on-change="handleChange1"
      :titles="['未添加', '已添加']"
    >
      <div :style="{float: 'right', margin: '5px'}">
        <Button size="small" @click="confirm">确定</Button>
      </div>
    </Transfer>
  </Drawer>
</template>
<script>
  import axios from '@/libs/api.request'
  export default {
    name: 'addAttribute',
    props:['show_attribute'],
    data() {
      return {
        attribute: [],
        targetKeys1: []
      }
    },
    methods: {
      render1(item) {
        return item.label
      },
      handleChange1(newTargetKeys, direction, moveKeys) {
        if(direction == 'right'){
          this.targetKeys1.push(...moveKeys)
          // console.log(this.targetKeys1)
        }
        else{
          for(let i in moveKeys){
            let index = this.targetKeys1.indexOf(moveKeys[i])
            this.targetKeys1.splice(index, 1)
          }
        }
        
      },
      // 确认穿梭框
      confirm() {
        console.log(this.$parent.show_attribute)
        this.$parent.formValidate.identifier = this.targetKeys1
        for(let i in this.attribute){
          if(this.targetKeys1.indexOf(this.attribute[i].key) != -1){
            this.$parent.formValidate.function_name.push(this.attribute[i].label)
          }
        }
        console.log('穿梭框：')
        console.log(this.$parent.formValidate.identifier)
        console.log(this.$parent.formValidate.function_name)
        this.$parent.show_attribute = false
      },
      getAttribute() {
        axios
          .request({
            url: 'api/device/getAttribute'
          })
          .then(res => {
            if (res.data.msg == 'ok') this.attribute = res.data.data
            else this.$Message.success('获取属性表失败！')
          })
          .catch(error => {
            console.log(error)
          })
      },
      filterMethod(data, query) {
        return data.label.indexOf(query) > -1
      }
    },
    mounted() {
      this.getAttribute()
      console.log(this.$parent.show_attribute)
      console.log(this.attribute)
    }
  }
</script>
