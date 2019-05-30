import axios from 'axios'
import store from '@/store'
// import { Spin } from 'iview'
const addErrorLog = errorInfo => {
  const {
    statusText,
    status,
    request: { responseURL }
  } = errorInfo
  let info = {
    type: 'ajax',
    code: status,
    mes: statusText,
    url: responseURL
  }
  if (!responseURL.includes('save_error_logger')) store.dispatch('addErrorLog', info)
}

class HttpRequest {
  constructor (baseUrl = baseURL) {
    this.baseUrl = baseUrl
    this.queue = {}
  }
  getInsideConfig () {
    const config = {
      baseURL: 'http://localhost:8000/',
      // baseURL: '',
      // baseURL: this.baseUrl,
      headers: {
        //
      }
    }
    return config
  }
  destroy (url) {
    delete this.queue[url]
    if (!Object.keys(this.queue).length) {
      // Spin.hide()
    }
  }
  interceptors (instance, url) {
    // 请求拦截
    instance.interceptors.request.use(
      config => {
        // 添加全局的loading...
        if (!Object.keys(this.queue).length) {
          // Spin.show() // 不建议开启，因为界面不友好
        }
        this.queue[url] = true
        return config
      },
      error => {
        return Promise.reject(error)
      }
    )
    // 响应拦截
    instance.interceptors.response.use(
      res => {
        this.destroy(url)
        const { data, status } = res
        return { data, status }
      },
      error => {
        this.destroy(url)
        let errorInfo = error.response
        if (!errorInfo) {
          const {
            request: { statusText, status },
            config
          } = JSON.parse(JSON.stringify(error))
          errorInfo = {
            statusText,
            status,
            request: { responseURL: config.url }
          }
        }
        addErrorLog(errorInfo)
        return Promise.reject(error)
      }
    )
  }
  transform (data) {
    let param = new URLSearchParams()
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        param.append(key, data[key])
      }
    }
    return param
  }
  // const axiosUrl = env === 'development'
  // ? 'http://localhost:8080/'
  // : 'http://192.168.0.1:8080'

  request (options) {
    // axios 默认是不发送cookie
    axios.defaults.withCredentials = true

    const instance = axios.create()
    options = Object.assign(this.getInsideConfig(), options)
    this.interceptors(instance, options.url)
    if(options.params){
      options.params = this.transform(options.params)
    }
    if(options.data){
      options.data = this.transform(options.data)
    }
    return instance(options)
  }
}
export default HttpRequest
