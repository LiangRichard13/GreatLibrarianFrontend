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
// import { fetchGet} from '@/services/ajax';
// import { URL } from '../services/conf';

export default {
  name: "NavigationTop",
  data() {
    return {
      state: '',
      user: {'username':'UserName'},
    }
  },

  mounted() {
     // const getUrl = URL.captchaURL; // 使用基本URL,需要时可进行拼接扩展
     //通过取出登录后在本地存储的用户id获取用户信息
    // if (localStorage.getItem("uid") !== null) {
    //   fetchGet(localStorage.getItem("uid"),getUrl).then(res => {
    //     this.user = res.data;
    //   })
    // }
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
>>>.el-input__inner {
  border-radius: 20px;
  height: 40px;
}
</style>
