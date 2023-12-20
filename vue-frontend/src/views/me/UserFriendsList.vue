<template>
  <div style="overflow-x: hidden;">
    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的好友</h3>
    <el-row :gutter="20">
      <el-col :span="12" v-for="(row, index) in userFriends" :key="index"  class="user-card">
        <el-card>
          <div style="display: flex; align-items: center;">
            <img :src="row.iconUrl" style="width: 50px; height: 50px; border-radius: 50%;" />
            <div style="margin-left: 10px;">
              <p>用户名:{{ row.username }}</p>
              <p>用户ID:{{ row.id }}</p>
              <p>IP地址:{{ row.ip }}</p>

              <!-- Conditional rendering for online/offline status -->
              <p v-if="row.ip" style="color: green;">在线</p>
              <p v-else style="color: red;">离线</p>
            </div>
          </div>
          <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info" icon-color="red"
            @confirm="handleDeleteFriend(row.id, index)" title="确定要删除此好友吗？">
            <el-button type="danger" slot="reference">删除好友</el-button>
          </el-popconfirm>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script>
// import { getUserFriendsById} from "@/api/collaborate";
import {  deleteById } from "@/api/collaborate";
import config from "@/services/conf"

export default {
  name: "UserList",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userFriends: [
        {
          id: '1',
          username: "Alice",
          iconUrl: null,
          ip: "192.168.1.1"
        },
        {
          id: '2',
          username: "Bob",
          iconUrl: null,
          ip: ""
        },
        {
          id: '3',
          username: "Charlie",
          iconUrl: null,
          ip: "192.168.1.3"
        },]
    }
  },
  methods: {
    load() {
      // const id = localStorage.getItem('uid')
      // getUserFriendsById(id).then(res => {
      //   this.userFriends = res.data;
      // })

      // 更新 userFriends 列表中每个用户的 iconUrl
      this.userFriends = this.userFriends.map(user => {
        if(user.iconUrl){
          let iconUrl = user.iconUrl.replace(/\\/g, '/'); // 替换所有反斜杠为斜杠
          iconUrl = `${config.API_URL}/${iconUrl}`; // 拼接完整的 URL
          return { ...user, iconUrl }; // 返回更新后的用户对象
        }
        else
        {
          return { ...user, iconUrl: this.defaultAvatar };
        }
      });
    },
    handleDeleteFriend(id, index) {
      const uid = localStorage.getItem('uid')
      deleteById(id, uid).then(res => {
        if (res.success) {
          this.userFriends.splice(index, 1);
          this.$message({
            message: '好友已删除！',
            type: 'warning'
          });
        }
      })
    },
  },
  mounted() {
    this.load()
  },

}
</script>

<style scoped>
.user-card {
  margin-top: 20px; /* 设置顶部外边距 */
  margin-bottom: 10px; /* 设置底部外边距 */
}
</style>