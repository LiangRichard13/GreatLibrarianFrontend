<template>
  <div class="login">
    <div class="login-form">
      <div class="login-form-header">
        <img style="width: 75px; height: 75px;float:left;padding-right: 10px;" src="../assets/logo.png" alt="" />
        <div class="login-form-text">大模型测评工具箱-登录</div>
      </div>
      <div style="color: #91949c;font-weight: bolder">
        <el-tabs v-model="activeTab" @tab-click="handleClick">
          <el-tab-pane label="邮箱登录" name="emailLogin">
            <p>E-mail</p>
            <el-input class="login-form-input" v-model="email" placeholder="邮箱"></el-input>
          </el-tab-pane>
          <el-tab-pane label="手机号登录" name="phoneLogin">
            <p>Phone Number</p>
            <el-input class="login-form-input" v-model="phoneNumber" placeholder="手机号"></el-input>
          </el-tab-pane>
        </el-tabs>
        <p>Password</p>
        <el-input class="login-form-input" placeholder="密 码" v-model="password" show-password></el-input>
        <div style="padding-top: 10px">
          <el-checkbox v-model="remember">记住我</el-checkbox>
          <div style="float: right">
            <el-tooltip class="item" effect="dark" content="请联系管理员修改" placement="bottom">
              <el-link style="font-weight: bolder;font-size: 14px;color:#91949c;" :underline="false">
                忘记密码?
              </el-link>
            </el-tooltip>
          </div>
        </div>
        <el-button @click="postLogin" class="login-form-button" type="primary">SIGN IN</el-button>
      </div>
      <div class="login-form-footer">
        <el-link href="/register" style="font-weight: bolder;font-size: 16px;color: #91949c;" :underline="false">
          还没有账号？去注册
          <i style="font-weight: bolder;font-size: 15px" class="el-icon-right"></i>
        </el-link>
      </div>
    </div>
  </div>
</template>

<script>
import { Login } from '@/api/user.js';
// import setUserIp from '@/api/user.js';
import { Notification } from "element-ui";

export default {
  data() {
    return {
      activeTab: "emailLogin", // 默认选中的选项卡
      phoneNumber: '18457096496',
      email: '1760268004@qq.com',
      password: '123456',
      remember: false,
    }
  },

  methods: {
    postLogin() {
      let LoginData
      if (this.activeTab === "emailLogin") {
        LoginData = {
          loginName: this.email,
          password: this.password,
          remember: this.remember,
          type: 'email'
        };
        console.log(LoginData);
      } else if (this.activeTab === "phoneLogin") {
        LoginData = {
          loginName: this.phoneNumber,
          password: this.password,
          remember: this.remember,
          type: 'tel'
        }
      }
      Login(LoginData).then(res => {
        if (res.success) {
          Notification.success({
            title: 'Success!',
            message: '登录成功！',
            type: 'success'
          });
          localStorage.setItem("uid", res.data.id);
          console.log(res.data.token)
          localStorage.setItem("loginToken", res.data.loginToken);//将用户id和token存放到本地
          // localStorage.setItem("authToken", res.data.authToken);
          // this.handleSetUserIp()
          this.$router.push({ path: '/home', replace: true })
        }
      })
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    // handleSetUserIp() {
    //   const id = localStorage.getItem('uid')
    //   setUserIp(id)
    // }
  }
}
</script>

<style scoped>
.login-form-button:hover {
  color: #ffffff;
  text-shadow: 0 0 10px #ffffff,
    0 0 20px #ffffff,
    0 0 40px #ffffff,
    0 0 80px #ffffff,
    0 0 120px #ffffff,
    0 0 160px #ffffff;
}

.login {
  width: 100%;
  height: 100%;
  background: white;
}

.login-form {
  width: 500px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -60%);
  letter-spacing: 2px;
}

.login-form-input {
  margin-bottom: 10px;
}

.login-form-button {
  border-radius: 3px;
  width: 100%;
  font-weight: 600;
  font-size: 15px;
  letter-spacing: 2px;
  height: 60px;
  background: black;
  box-shadow: 0 5px 30px rgb(0 66 8.5%);
  margin-top: 35px;
}

.login-form-footer {
  font-weight: bolder;
  color: #91949c;
  padding-top: 40px;
  text-align: center;
}

.el-checkbox {
  color: #91949c;
  font-weight: bolder;
  font-size: 15px;
}

.login-form-text {
  color: #000000;
  font-weight: bold;
  font-size: 30px;
  padding-top: 15px;
}

.login-form-header {
  height: 20px;
  padding-left: 20px;
  padding-bottom: 100px;
}
</style>
