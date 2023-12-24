import request from "axios"
import config from "../services/conf"
import {Notification} from 'element-ui'

// const token = localStorage.getItem('token');

//基本请求体
const service = request.create({
    baseURL: config.API_URL,
    // headers: {
    //     "Authorization": token
    // }
});

service.interceptors.request.use(
    config => {
        // 在发送请求前打印发送的数据
        console.log('Sending data:', config.data);
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

//响应拦截器
service.interceptors.response.use(
    response => {
        console.log("响应信息:",response.data)
        const res = response.data;
        if (!res.success)
            {
                  Notification.error({
                      title: '出错了！ ',
                      message: res.message
                  });
              }

        return res
    },

    error => {
  console.log('err' + error);
  return Promise.reject(error);
}

);

export default service
