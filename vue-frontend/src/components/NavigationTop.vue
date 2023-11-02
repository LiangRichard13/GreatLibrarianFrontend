<template>
  <div class="header">
    <div style="height: 70px;width: 100%">
      <div class="header-links">
        <el-link style="color: white" href="/Home" class="header-link" :underline="false">首页</el-link>
      </div>

      <el-dropdown style="float: right;padding-right: 10px">
        <el-button type="text">
          <div class="header-name">{{ this.user.username }}
            <i class="el-icon-caret-bottom"></i>
          </div>
        </el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item divided>
            <el-button type="text" @click="handleLogout" :underline="false">
              <i style="font-size: 15px; padding-right: 3px" class="el-icon-switch-button"></i>退出登录
            </el-button>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>

    </div>
  </div>
</template>

<script>
import {findById} from '@/api/user';

export default {
  name: "NavigationTop",
  data() {
    return {
      user: {'username':'UserName'},
    }
  },

  mounted() {
     //通过取出登录后在本地存储的用户id获取用户信息
    if (localStorage.getItem("uid") !== null) {
      findById(localStorage.getItem("uid")).then(res => {
        this.user = res.data;
      })

    }
    //如果本地没有存储的用户id则说明没有登录，跳转到登录页面
    else{
       this.$message({
        message: '检测到您尚未登录，请登录',
        type: 'warning' // 设置消息类型为警告
      });
        this.$router.push("/login")
    }
  },

  methods: {

    handleLogout() {
      localStorage.removeItem("uid")
      localStorage.removeItem("token")
      this.$router.push('/login')
    },

  },

}
</script>

<style scoped>

#loginButton:hover{
  color: white;
  transform: scale(1.0,1.0);
}
  .header-link:hover{
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
  letter-spacing: 2px;
  font-size: 17px;
  padding-right: 40px;
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

</style>
