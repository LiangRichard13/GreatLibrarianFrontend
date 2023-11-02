<template>
  <div class="login">
    <div class="login-form">
      <div style="color: #91949c;font-weight: bolder">
        <p>Username</p>
        <el-input class="login-form-input" v-model="username" placeholder="账 号"></el-input>
        <p>Password</p>
        <el-input class="login-form-input" placeholder="密 码" v-model="password" show-password></el-input>
        <p>Check Password</p>
        <el-input class="login-form-input" placeholder="确 认 密 码" v-model="checkPassword"
                  show-password></el-input>
        <el-button @click="postLogin" class="login-form-button" type="primary">SIGN UP</el-button>
      </div>
      <div class="login-form-footer">
        <el-link href="/login" style="font-weight: bolder;font-size: 16px;color: #91949c;"
                 :underline="false">
          我有账号 去登录
          <i style="font-weight: bolder;font-size: 15px" class="el-icon-right"></i>
        </el-link>
      </div>
    </div>
  </div>
</template>

<script>
import {Register} from '@/api/user.js';

export default {
  data() {
    return {
      username: '',
      password: '',
      checkPassword: '',
    }
  },
  methods: {
    postLogin() {
      // const postUrl = URL.captchaURL; // 使用基本URL,需要时可进行拼接扩展
      if (this.username.length < 6) {
        this.$message({
          message: '请输入不少于6位的用户名',
          type: 'warning'
        });
        return
      }
      if (this.password !== this.checkPassword) {
        this.$message({
          message: '您两次输入的密码不同!',
          type: 'warning'
        });
        return
      }
      const RegisterData = {
        username: this.username,
        password: this.password,
      };
      console.log(RegisterData);
      Register(RegisterData).then(res => {
        if (res.success) {
          this.$router.push("/login")
        }
      })
    }
  }
}
</script>

<style scoped>

.login {
  width: 100%;
  height: 100%;
  background: #FFFFFF;
}

.login-form {
  width: 500px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
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

.login-form-button:hover {
  color: #ffffff;
  text-shadow: 0 0 10px #ffffff,
  0 0 20px #ffffff,
  0 0 40px #ffffff,
  0 0 80px #ffffff,
  0 0 120px #ffffff,
  0 0 160px #ffffff;
}

.login-form-footer {
  font-weight: bolder;
  color: #91949c;
  padding-top: 40px;
  text-align: center;
}

</style>
