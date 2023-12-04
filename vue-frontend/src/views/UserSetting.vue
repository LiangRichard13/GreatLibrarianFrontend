<template>
  <div>
    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">基本设置</h3>
    <div style="display: flex; justify-content: center; align-items: flex-start;">
      <el-form style="width: 350px;float: left;margin-right: 20px;" label-position="top" ref="form" :model="user" label-width="80px">
        <el-form-item style="padding: 0" label="用户名">
          <el-input v-model="user.username"></el-input>
        </el-form-item>
        <el-form-item style="padding: 0" label="密码">
          <el-input type="password" v-model="user.password"></el-input>
        </el-form-item>
        <el-form-item style="padding: 0" label="确认密码">
          <el-input type="number" v-model="checkPassword"></el-input>
        </el-form-item>
        <el-form-item style="padding: 0" label="邮箱">
          <el-input type="email" v-model="user.email"></el-input>
        </el-form-item>
        <el-form-item style="padding: 0" label="电话号码">
          <el-input type="number" v-model="user.tel"></el-input>
        </el-form-item>

         <el-form-item style="padding: 0;" label="API_KEY:" >
        <div v-for="(row,index) in apiKeys" :key="index" class="api-key-item">
      API_KEY({{index+1}}):{{ row.value }}
    </div>
    <el-button @click="goToKeyConfig" type="success">配置我的API_KEY</el-button>
</el-form-item>
        <el-form-item style="padding-top: 20px">
          <el-button type="primary" icon="el-icon-edit" @click="onCheck">更新基本信息</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align: center;">
        <img style="padding-left: 150px;width: 150px; height: 150px;margin-bottom: 10px;" alt=""
             :src="user.iconURL || defaultAvatar">
        <br>
        <el-upload
            style="padding-left: 150px;display:inline-block"
            class="upload-demo"
            accept=".png,.jpg"
            :action="uploadAction"
            :on-success="handleUploadSuccess"
            multiple
            :limit="1">
          <el-button style="width: 150px;" size="small " type="primary">
            <i class="el-icon-upload2"></i> 点击上传
          </el-button>
          <div slot="tip" class="el-upload__tip">只能上传jpg/png文件</div>
        </el-upload>
      </div>
    </div>
  </div>
</template>

<script>
import {findById , updateUser} from "@/api/user";
import {findByUserId} from "@/api/apiConfig";
import config from "../services/conf";

export default {
  name: "UserSetting",
 data() {
    return {
      uploadAction: config.API_URL + '/upload',
      user: {
        username: 'Richard',
        tel:'13527454855',
        password: '123456',
        email: 'chendanliang793@gmail',
        iconURL: '',
      },
      checkPassword:'',
      apiKeys:[{value:'123'},{value:'12345'}],
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
    }
  },
   created() {
    if (!this.user.iconURL) {
      this.user.iconURL = this.defaultAvatar; // 如果用户没有头像，则使用默认头像
    }
  },
  mounted() {
    this.load()
  },
   methods: {
load(){
      if (localStorage.getItem("uid") !== null) {
 const id = parseInt(localStorage.getItem("uid"))
      findById(id).then(res => {
        this.user = res.data;
        this.checkPassword=this.user.password
      })
      findByUserId(id).then(res => {
        this.apiKeys = res.data;
      })
    }
},
    onSubmit() {
      updateUser(this.user).then(res => {
        if (res.success) {
          this.user = res.data;
           this.$message({
                    message:'更新成功',
                    type: 'success'
                });
          this.load()
        }
      })
    },

    handleUploadSuccess(res) {
      this.user.iconURL = res;
      updateUser(this.user).then(res => {
        if (res.success) {
          this.user = res.data;
          this.$message({
                    message:'上传成功',
                    type: 'success'
                });
         this.load()
        }
      })
    },

    onCheck() {
      if (this.user.username.length < 6) {
        this.$message({
          message: '请输入不少于6位的用户名',
          type: 'warning'
        });
        return
      }
       if (this.user.password.length < 6) {
        this.$message({
          message: '请输入不少于6位的密码',
          type: 'warning'
        });
        return
      }
             if (this.user.password !== this.checkPassword) {
        this.$message({
          message: '您两次输入的密码不同!',
          type: 'warning'
        });
        return
      }
      if (!this.isValidEmail(this.user.email)) {
     this.$message({
          message: '无效的邮箱',
          type: 'warning'
      });
      return
}
      if (!this.isValidPhoneNumber(this.user.tel)) {
        this.$message({
          message: '无效的手机号',
          type: 'warning'
      });
         return
      }
       this.onSubmit()
    },
    isValidEmail(email) {
  // 使用正则表达式匹配标准的邮箱格式
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
},
   isValidPhoneNumber(phoneNumber) {
  // 使用正则表达式匹配11位数字
  const phonePattern = /^\d{11}$/;
  return phonePattern.test(phoneNumber);
},
     goToKeyConfig(){
       this.$router.push('/keyConfig');
     }
  },
}
</script>

<style scoped>
>>> .el-form--label-top .el-form-item__label {
  padding: 0;
}

>>>.el-form-item {
  margin-bottom: 5px;
}
.api-key-item {
  margin: 10px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.dialog-footer {
  text-align: right;
  padding: 10px;
}
</style>