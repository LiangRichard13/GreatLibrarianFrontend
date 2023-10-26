import axios from 'axios'
import qs from 'qs'

axios.defaults.timeout = 5000; //响应时间
// axios.defaults.baseURL = 'http://localhost:3000';   //配置接口地址

//POST传参序列化(添加请求拦截器)
axios.interceptors.request.use((config) => {
  //在发送请求之前做某件事
  //携带请求头
  let token = window.localStorage.getItem("accessToken")
  console.log("token:"+token);
  //下面两种方式都行
  // config.headers.accessToken = token;
  config.headers['accessToken'] = token
  config.headers['content-type'] = 'application/x-www-form-urlencoded'
  return config;
},(error) =>{
  console.log('错误的传参')
  return Promise.reject(error);
});

//返回状态判断(添加响应拦截器)
axios.interceptors.response.use((res) =>{
  //对响应数据做些事
  if(!res.data.success){ return Promise.resolve(res);
  }
  return res;
}, (error) => {
  console.log('网络异常')
  return Promise.reject(error);
});

//返回一个Promise(发送post请求)
export function fetchPost(url, params) {
  return new Promise((resolve, reject) => { axios.post(url, qs.stringify(params)) .then(response => { resolve(response); }, err => { reject(err); }) .catch((error) => { reject(error) })
  })
}

export function fetchGet(url, param) {
  return new Promise((resolve, reject) => { axios.get(url, {params: param}) .then(response => { resolve(response) }, err => { reject(err) }) .catch((error) => { reject(error) })
  })
}
export default {
  fetchPost,
  fetchGet,
}


