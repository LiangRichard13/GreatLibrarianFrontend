<template>
    <div class="login">
        <div class="login-form">
            <div style="color: #91949c;font-weight: bolder">
                <p>Username</p>
                <el-input class="login-form-input" v-model="username" placeholder="账 号"></el-input>
                <p>Password</p>
                <el-input class="login-form-input" placeholder="密 码" v-model="password" show-password></el-input>
                <div style="padding-top: 10px">
                    <div style="float: right">
                        <el-tooltip class="item" effect="dark" content="请联系管理员修改" placement="bottom">
                            <el-link style="font-weight: bolder;font-size: 14px;color:#91949c;"
                                     :underline="false">
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
// import {fetchPost} from '@/services/ajax';
// import { URL } from '../services/conf';
    export default {
        data() {
            return {
                username: '',
                password: '',
            }
        },

        methods: {
            postLogin()
    {
                // const postUrl = URL.captchaURL; // 使用基本URL,需要时可进行拼接扩展
                const LoginData = {
                    username: this.username,
                    password: this.password,
                };
                console.log(LoginData);

                // fetchPost(LoginData,postUrl).then(res => {
                //     localStorage.setItem("uid", res.data.user.id);
                //     localStorage.setItem("token", res.data.token);//将用户id和token存放到本地
                //     this.$router.push({path: '/Home', replace: true})
                // })
            }
        }
    }
</script>

<style scoped>
.login-form-button:hover{
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
        background:white;
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

    >>> .el-input__inner {
        height: 48px;
    }
</style>
