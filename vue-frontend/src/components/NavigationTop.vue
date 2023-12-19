<template>
  <el-container>
    <el-header style="padding: 0">
      <div class="header">
        <div style="height: 70px;width: 100%">
          <div class="header-logo">
            <img style="width: 50px; height: 50px;float: left" src="../assets/logo.png" alt="" />
            <div class="header-logo-text">大模型测评工具箱</div>
          </div>
          <div class="header-links">
            <el-link style="color: white" href="/Home" class="header-link" :underline="false">主页</el-link>
            <el-link style="color: white" href="/keyConfig" class="header-link" :underline="false">配置</el-link>
            <el-link style="color: white" href="/userList" class="header-link" :underline="false">合作</el-link>
            <el-link style="color: white" href="/addProject" class="header-link" :underline="false">项目</el-link>
          </div>

          <el-dropdown style="float: right;padding-right: 10px">
            <el-button type="text">
              <div class="header-name">Welcome!{{ this.user.name }}
                <i class="el-icon-caret-bottom"></i>
              </div>
              <img alt="" style="width: 45px;height: 45px;border-radius: 50%" :src="user.iconUrl">
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <el-link :underline="false" href="/FriendRequests" style="padding-right: 7px">
                  <i style="font-size: 15px; padding-right: 3px" class="el-icon-bell"></i>我的好友申请
                </el-link>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-link :underline="false" href="/userFriendsList" style="padding-right: 7px">
                  <i style="font-size: 15px; padding-right: 3px" class="el-icon-user
"></i>我的好友
                </el-link>
              </el-dropdown-item>
              <el-dropdown-item>
                <el-link :underline="false" href="/setting" style="padding-right: 7px">
                  <i style="font-size: 15px; padding-right: 3px" class="el-icon-setting"></i>个人设置
                </el-link>
              </el-dropdown-item>
              <el-dropdown-item divided>
                <el-button type="text" @click="handleLogout" :underline="false">
                  <i style="font-size: 15px; padding-right: 3px" class="el-icon-switch-button"></i>退出登录
                </el-button>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
    </el-header>
    <el-main style="padding: 0">
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
// import {findById, isExpired,removeUserIp,setUserIp} from '@/api/user';
// import{config} from "@/services/conf"

export default {
  name: "NavigationTop",
  data() {
    return {
      user: { name: '新用户', iconUrl: null },
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
    }
  },

  mounted() {
    // //如果本地有存储的用户id则说明有登录
    // if (localStorage.getItem("uid") !== null) {

    //   //检查token是否过期
    //   const token = localStorage.getItem('loginToken')
    //   isExpired(token).then(res => {
    //     if (!res.success) {
    //       this.$message({
    //         message: '您的令牌已过期请重新登录',
    //         type: 'warning'
    //       });
    //       localStorage.removeItem("uid");
    //       localStorage.removeItem("loginToken");
    //       this.handleRemoveUserIp;  //令牌过期则移除用户IP
    //       this.$router.push("/login");
    //     }
    //   });

    //   const id = localStorage.getItem("uid")
    //   this.handleSetUserIp
    //   window.addEventListener('beforeunload', this.handleRemoveUserIp);//添加事件监听，如果用户关闭浏览器则请求移除用户ip
    //   //如果令牌没过期
    //   //通过取出登录后在本地存储的用户id获取用户信息
    //   findById(id).then(res => {
    //     this.user = res.data;
    //     console.log(res.data)
    //   })
    // if (!this.user.iconUrl) {
    //   this.user.iconUrl = this.defaultAvatar; // 如果用户没有头像，则使用默认头像
    //   this.user.iconUrl = this.user.iconUrl.replace(/\\/g, "/");
    //   this.user.iconUrl = config.API_URL + '/' + this.user.iconUrl;
    // }
    // else {
    //   this.iconUrl = this.defaultAvatar; // 如果用户没有头像，则使用默认头像

    // }
    // }
    // //如果本地没有存储的用户id则说明没有登录，跳转到登录页面
    // else {
    //   this.$message({
    //     message: '检测到您尚未登录，请登录',
    //     type: 'warning' // 设置消息类型为警告
    //   });
    //   this.$router.push("/login")
    // }
  },

  //使用过程需要去掉，仅作为展示
  created() {
    if (!this.user.iconUrl) {
      this.user.iconUrl = this.defaultAvatar; // 如果用户没有头像，则使用默认头像
    }
  },
  methods: {

    handleLogout() {
      localStorage.removeItem("uid")
      localStorage.removeItem("loginToken")
      // this.handleRemoveUserIp
      this.$router.push('/login')
    },

    // handleRemoveUserIp() {
    //   const uid = localStorage.getItem("uid")
    //   removeUserIp(uid)
    // },
    // handleSetUserIp() {
    //   const id = {
    //     id: localStorage.getItem('uid')
    //   }
    //   setUserIp(id)

    // }

  },
  // beforeDestroy() {
  //   // 在组件销毁前移除事件监听
  //   window.removeEventListener('beforeunload', this.handleRemoveUserIp);
  // },

}
</script>

<style scoped>
#loginButton:hover {
  color: white;
  transform: scale(1.0, 1.0);
}

.header-link:hover {
  color: #ffffff;
  text-shadow: 0 0 10px #ffffff,
    0 0 20px #ffffff,
    0 0 40px #ffffff,
    0 0 80px #ffffff,
    0 0 120px #ffffff,
    0 0 160px #ffffff;
}

.header {
  height: 70px;
  background: black;
  box-shadow: 1px 1px 5px #330867;

}

.header-links {
  float: left;
  padding-left: 50px;
  padding-top: 23px;
}

.header-link {
  color: #FFFFFF;
  letter-spacing: 3px;
  font-size: 20px;
  padding-right: 50px;
}

.header-name {
  color: white;
  float: right;
  padding-top: 15px;
  padding-left: 15px;
  font-weight: bolder;
  font-size: 15px;
  letter-spacing: 2px;
}

.el-main {
  overflow: auto;
}
.header-logo {
  padding-top: 10px;
  padding-left: 2%;
  float:left;
  letter-spacing: 2px;
}

.header-logo-text {
  font-size: 25px;
  padding-top: 3px;
  font-weight: bolder;
  padding-left: 15px;
  float: left;
  color: #FFFFFF;
}
</style>
