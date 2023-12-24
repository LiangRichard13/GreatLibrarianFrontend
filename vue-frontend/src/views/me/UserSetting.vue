<template>
  <div>
    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">基本设置</h3>
    <div style="display: flex; justify-content: center; align-items: flex-start;">
      <el-form style="width: 350px;float: left;margin-right: 20px;" label-position="top" ref="form" :model="user"
        label-width="80px">
        <el-form-item style="padding: 0" label="用户名">
          <el-input v-model="user.name"></el-input>
        </el-form-item>
        <!-- <el-form-item style="padding: 0" label="修改密码">
          <el-input type="password" v-model="password" show-password></el-input>
        </el-form-item>
        <el-form-item style="padding: 0" label="确认密码">
          <el-input type="password" v-model="checkPassword" show-password></el-input>
        </el-form-item> -->
        <el-form-item>
          <el-button size="small" icon="el-icon-edit" type="danger" @click="showDialog = true">
            <i></i>修改密码
          </el-button>
        </el-form-item>
        <el-form-item style="padding: 0" label="邮箱">
          <!-- <el-input type="email" v-model="user.email"></el-input> -->
          <div>{{ user.email }}</div>
        </el-form-item>
        <el-form-item style="padding: 0" label="电话号码">
          <!-- <el-input type="number" v-model="user.tel"></el-input> -->
          <div>{{ user.tel }}</div>
        </el-form-item>

        <el-form-item style="padding: 0;" label="API_KEY">
          <div v-for="(row, index) in apiKeys" :key="index" class="api-key-item"
            style="box-shadow: 0px 0px 10px rgba(0,0,0,0.1); padding: 10px; margin-bottom: 10px;">
            API_KEY({{ index + 1 }}): {{ row.name }}--{{ row.value }}
          </div>

          <el-button @click="goToKeyConfig" type="success">配置我的API_KEY</el-button>
        </el-form-item>
        <el-form-item style="padding-top: 20px">
          <el-button type="primary" icon="el-icon-edit" @click="onCheck">更新基本信息</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align: center;">
        <img style="padding-left:100px;width: 150px; height: 150px;margin-bottom: 10px;" alt="" :src="user.iconUrl">
        <br>
        <el-upload class="upload-demo" :before-upload="beforeUpload" multiple :limit="1" accept=".png,.jpg">
          <el-button size="small" type="primary" style="margin-left:50px">
            <i class="el-icon-upload2"></i> 点击上传
          </el-button>
          <div slot="tip" class="el-upload__tip">只能上传 jpg/png 文件</div>
        </el-upload>
      </div>
    </div>
    <el-dialog title="修改密码" :visible.sync="showDialog" width="50%" @close="resetDialog">
      <div>
        <el-form ref="form" :model="newApiKey" label-width="100px">

          <el-form-item label="修改的密码">
            <el-input v-model="password"></el-input>
          </el-form-item>

          <el-form-item label="确认密码">
            <el-input v-model="checkPassword"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="passwordOnCheck">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { updateUser, uploadAvatar, editPassword } from "@/api/user";
// import {getUserIconUrl}from "@/api/user"
import { findById } from "@/api/user";
import { findApiKeyByUserId } from "@/api/apiConfig";
import config from "@/services/conf"

export default {
  name: "UserSetting",
  data() {
    return {
      showDialog: false,
      user: {
        name: '',
        tel: '',
        email: '',
        iconUrl: null,
      },
      password: '',
      checkPassword: '',
      apiKeys: [],
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      const id = { id: localStorage.getItem("uid") }
      findById(id).then(res => {
        this.user = res.data;
        this.checkPassword = this.user.password
        if (!this.user.iconUrl) {
          this.user.iconUrl = this.defaultAvatar; // 如果用户没有头像，则使用默认头像
        }
        else {
          this.user.iconUrl = this.user.iconUrl.replace(/\\/g, "/");
          this.user.iconUrl = this.user.iconUrl.replace(/App/g, "");
          // this.user.iconUrl = config.API_URL + '/' + this.user.iconUrl;
          this.user.iconUrl = config.API_URL + this.user.iconUrl;
        }
        console.log("用户信息",this.user)
      })
      const uid = localStorage.getItem('uid')
      findApiKeyByUserId(uid).then(res => {
        this.apiKeys = res.data;
      })
    },
    onSubmit() {
      const UpdateData = { id: localStorage.getItem('uid'), name: this.user.name }
      updateUser(UpdateData).then(res => {
        if (res.success) {
          this.$message({
            message: '更新成功',
            type: 'success'
          });
          this.load()
        }
      })
    },

    handleUploadSuccess(res) {
      // const uid = { id: localStorage.getItem('uid') }
      // getUserIconUrl(uid).then(res => {
      //   this.user.iconUrl = res.url;
      //   this.$message({
      //     message: '上传成功',
      //     type: 'success'
      //   });
      // })
      this.user.iconUrl = res.url
      this.$message({
        message: '上传成功',
        type: 'success'
      });
    this.load()

  },
  passwordOnCheck() {
    if (this.password.length < 6) {
      this.$message({
        message: '请输入不少于6位的密码',
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
    this.handleEditPassword
  },
  onCheck() {
    if (this.user.name.length < 6) {
      this.$message({
        message: '请输入不少于6位的用户名',
        type: 'warning'
      });
      return
    }
    // if (!this.isValidEmail(this.user.email)) {
    //   this.$message({
    //     message: '无效的邮箱',
    //     type: 'warning'
    //   });
    //   return
    // }
    // if (!this.isValidPhoneNumber(this.user.tel)) {
    //   this.$message({
    //     message: '无效的手机号',
    //     type: 'warning'
    //   });
    //   return
    // }
    this.onSubmit()
  },
  handleEditPassword() {
    const updatePassoword = { id: localStorage.getItem('uid'), password: this.password }
    editPassword(updatePassoword).then(res => {
      if (res.success) {
        this.$message({
          message: '你已成功修改密码！',
          type: 'success'
        });
      }
    })
  },
  goToKeyConfig() {
    this.$router.push('/keyConfig');
  },
  beforeUpload(file) {
    const formData = new FormData();
    formData.append('iconFile', file); // 使用 'iconFile' 作为键
    // formData.append('uid', localStorage.getItem('uid'));

    // 发起自定义的上传请求
    this.uploadFile(formData);

    // 阻止组件的默认上传行为
    return false;
  },
  uploadFile(formData) {
    const uid = localStorage.getItem('uid')
    uploadAvatar(formData, uid).then(res => {
      if (res.success) {
        this.handleUploadSuccess(res)
      }
    })
  },
  resetDialog() {
    this.password = '',
      this.checkPassword = ''
  },
},
}
</script>

<style scoped>
.el-form--label-top .el-form-item__label {
  padding: 0;
}

.el-form-item {
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

.el-upload__tip {
  margin-left: 50px;
}
</style>