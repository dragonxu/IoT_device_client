import Vue from 'vue'
import Vuex from 'vuex'

import user from './module/user'
import app from './module/app'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    current_gateway: '',
    gateway_list: [],
    selected_device: [],
    select_attribute: []
    //
  },
  getters:{
    selected_device_count(state){
      if(state.selected_device.length>0)
        return false
      else
        return true
    }
  },
  mutations: {
    change_gateway (state, name) {
      state.current_gateway = name
    },

    update_gateway_list(state, data){
      if (!data){
        state.gateway_list = []
        return
      }
      for(let i in data){
        if(state.gateway_list.indexOf(data[i].gateway_name) == -1){
          state.gateway_list.push(data[i].gateway_name)
        }
      }
    },

    addDevice: (state, payload) => {
      if(state.selected_device.indexOf(name)==-1)
        state.selected_device.push({
          gateway:payload.gateway,
          name:payload.name
        })
    },

    delateDevice (state, payload) {
      let data = state.selected_device
      for (let i in data) {
        if (data[i].gateway == payload.gateway && data[i].name == payload.name) {
          state.selected_device.splice(i, 1)
          return 
        }
      }
    },
    cleareDevice (state) {
      state.selected_device = []
    },
    updataAttribute(state, a_list){
      state.select_attribute = []
      state.select_attribute = a_list
    }
  },
  actions: {
    //
  },
  modules: {
    user,
    app
  }
})
