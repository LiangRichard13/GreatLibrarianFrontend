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
          <el-input type="number" v-model="user.phoneNumber"></el-input>
        </el-form-item>

         <el-form-item style="padding: 0;" label="API_KEY:" >
        <div v-for="(row,index) in apiKeys" :key="index" class="api-key-item">
      API_KEY({{index+1}}):{{ row.content }}
       <el-popconfirm
                            confirm-button-text='确定'
                            cancel-button-text='不用了'
                            icon="el-icon-info"
                            icon-color="red"
                            @confirm="removeKey(index,row)"
                            title=" 确定要删除此API_KEY吗？ "
                    >
                        <el-button
                                style="margin-left: 8px"
                                size="mini"
                                icon="el-icon-delete"
                                type="danger"
                                slot="reference">删除
                        </el-button>
       </el-popconfirm>
    </div>
    <el-button @click="showDialog=true">添加API_KEY</el-button>
</el-form-item>
    <el-dialog
      title="添加 API Key"
      :visible.sync="showDialog"
      width="30%"
      @close="resetDialog">
      <div>
        <el-input v-model="newApiKey" placeholder="输入新的 API Key" />
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="addKey">确 定</el-button>
      </span>
    </el-dialog>

        <el-form-item style="padding-top: 20px">
          <el-button type="primary" @click="onCheck">更新基本信息</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align: center;">
        <img style="padding-left: 150px;width: 150px; height: 150px;margin-bottom: 10px;" alt=""
             :src="user.avatar || defaultAvatar">
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
import {findByUserId,addApiKey,deleteById} from "@/api/apiKey";
import config from "../services/conf";
import {Notification} from "element-ui";

export default {
  name: "UserSetting",
 data() {
    return {
      uploadAction: config.API_URL + '/upload',
      user: {
        username: 'Richard',
        phoneNumber:'13527454855',
        password: '123456',
        email: 'chendanliang793@gmail',
        avatar: '',
      },
      checkPassword:'',
      apiKeys:[{id:1,content:'123'},{id:2,content:'12345'}],
      newApiKey: '',
      showDialog:false,
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
    }
  },
   created() {
    if (!this.user.avatar) {
      this.user.avatar = this.defaultAvatar; // 如果用户没有头像，则使用默认头像
    }
  },
  mounted() {
    this.load()
  },
   methods: {
load(){
      if (localStorage.getItem("uid") !== null) {
      findById(localStorage.getItem("uid")).then(res => {
        this.user = res.data;
        this.checkPassword=this.user.password
      })
      findByUserId(localStorage.getItem("uid")).then(res => {
        this.apiKeys = res.data;
      })
    }
},
    onSubmit() {
      updateUser(this.user).then(res => {
        if (res.success) {
          this.user = res.data;
          Notification.success({
                    title: 'Success!',
                    message:res.message,
                    type: 'success'
                });
          this.load()
        }
      })
    },

    handleUploadSuccess(res) {
      this.user.avatar = res;
      updateUser(this.user).then(res => {
        if (res.success) {
          this.user = res.data;
         Notification.success({
                    title: 'Success!',
                    message:res.message,
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
   addKey() {

      if (this.newApiKey.trim()) {
     const data={
       newApiKey:this.newApiKey
     }
     addApiKey(data).then(res=>{
       if(res.success)
       {
         this.apiKeys.push(this.newApiKey);
        this.newApiKey = ''; // 清空输入框
        this.showDialog = false; // 关闭对话框
        this.$message({
          message: '添加成功',
          type: 'success'
        });
       }
     })
      }
      else
      {
         this.$message({
          message: 'API_KEY不能为空',
          type: 'warning'
        });
      }
    },
    removeKey(index,row) {
  const data={
    id:row.id
  }
  deleteById(data).then(res =>{
    if(res.success) {
      this.apiKeys.splice(index, 1);
      this.$message({
        message: '删除成功',
        type: 'success',
      });
    }
  })
    },
    resetDialog() {
      this.newApiKey = ''; // 重置输入框
    },
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