<template>
  <el-container style="height: 100vh;">
    <el-container>
      <!-- 主体部分 -->
      <el-main>
        <el-row :gutter="20">
          <!-- 左侧项目列表区域 -->
          <el-col :span="18">
            <div class="project-section">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span>我的项目</span>
                </div>
                <el-table :data="myProjects">
                  <!-- 表格内容 -->
                </el-table>
              </el-card>

              <el-card class="box-card" style="margin-top: 20px;">
                <div slot="header" class="clearfix">
                  <span>我参与的项目</span>
                </div>
                <el-table :data="participatedProjects">
                  <!-- 表格内容 -->
                </el-table>
              </el-card>
            </div>
          </el-col>

          <!-- 右侧好友列表区域 -->
          <el-col :span="6">
            <el-badge :value="friendRequestNumebr" class="item" style="margin-top: 20px;">
              <el-button size="large" @click="pushToFriendRequest">待处理的好友请求</el-button>
            </el-badge>
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>我的好友</span>
              </div>
              <template v-if="userFriends.length">
                <div v-for="(friend, index) in userFriends" :key="index" class="friend-card">
                  <el-avatar :src="friend.icon"></el-avatar>
                  <div class="friend-info">
                    <span>{{ friend.name }}</span>
                  </div>
                </div>
              </template>
              <div v-else class="empty-friends">
                暂无好友
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { getUserList,getFriendsRequest } from "@/api/collaborate";
import config from "@/services/conf"
export default {
  name: "userHome",
  data() {
    return {
      userFriends: [],
      myProjects:[],
      participatedProjects:[],
      friendRequestNumebr:0
    }
  },
  methods: {
    load() {
      const uid=localStorage.getItem('uid')
      //获取好友列表
      getUserList(uid).then(res => {
        this.userFriends = res.data.filter(user => user.state !== 0)
        this.userFriends = this.userFriends.map(user => {
          if (user.icon) {
            let icon = user.icon.replace(/\\/g, '/'); // 替换所有反斜杠为斜杠
            icon = user.icon.replace(/App/g, '');
            icon = config.API_URL + icon; // 拼接完整的 URL
            return { ...user, icon }; // 返回更新后的用户对象
          }
          else {
            return { ...user, icon: this.defaultAvatar };
          }
        });
      })
      //获取好友请求信息
      getFriendsRequest(uid).then(res=>{
        this.friendRequestNumebr=res.length
      })
      //获取项目信息
    
    },
    //跳转处理好友请求
    pushToFriendRequest(){
      this.$router.push('/FriendRequests')
    }
  },
  mounted() {
    this.load()
  },
}
</script>
<style scoped></style>