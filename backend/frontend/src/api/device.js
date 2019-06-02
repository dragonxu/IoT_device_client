import axios from '@/libs/api.request'

export const get_all_device = (gateway_name) => {
  return axios.request({
    url: 'api/device/getAll',
    method: 'post',
    data: { gateway_name }
  })
}

export const delate_device = (data) => {
  return axios
    .request({
      url: 'api/device/delate',
      method: 'post',
      data,
    })
    // .then(res => {
    //   console.log(res.data)
    //   this.$Message.success('成功')
    // })
    // .catch(error => {
    //   console.log(error)
    // })
}
