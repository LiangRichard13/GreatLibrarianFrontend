import request from "axios"
import config from "../services/conf"
import {Notification} from 'element-ui'
import router from "@/router";

const token = localStorage.getItem('token');

//基本请求体
const service = request.create({
    baseURL: config.API_URL,
    headers: {
        "Authorization": token
    }
});

//响应拦截器
service.interceptors.response.use(
    response => {
        const res = response.data;
        if (res.success === true) {
            if (res.msg !== null) {
                Notification.success({
                    title: 'Success ',
                    message: res.msg,
                    type: 'success'
                });
            }

        } else {
            Notification.error({
                title: '错误提示: ' + res.code,
                message: res.msg
            });
        }
        return res
    },

    error => {
  const res = error.data;
  if (res.code === 401 && res.msg === '令牌已过期') {
    // 如果状态码为401，表示令牌过期需要重新登录
    this.$message({
      message: '您的令牌已过期请重新登录',
      type: 'warning'
    });
    localStorage.removeItem("uid");
    localStorage.removeItem("token");

    return router.push("/login"); // 返回router.push的Promise
  }

  console.log('err' + error);
  return Promise.reject(error);
}

);

export default service
