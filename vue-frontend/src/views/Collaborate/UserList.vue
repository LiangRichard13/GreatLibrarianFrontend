<template>
  <div style="overflow-x: hidden">
    <el-row :gutter="20">
      <el-col :span="24" v-for="user in userList" :key="user.id">
        <el-card>
          <div style="display: flex; align-items: center;">
            <img :src="user.icon" style="width: 50px; height: 50px; border-radius: 50%;" />
            <div style="margin-left: 10px;">
              <p>用户名:{{ user.name }}</p>
              <p>用户ID:{{ user.id }}</p>
              <p>IP地址:{{ user.ip }}</p>

              <!-- Conditional rendering for online/offline status -->
              <!-- <p v-if="user.ip" style="color: green;">在线</p>
              <p v-else style="color: red;">离线</p> -->
            </div>
          </div>
          <el-button type="primary" @click="handleAddFriend(user.id)">添加好友</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { addFriend } from "@/api/collaborate";
import { getUserList } from "@/api/collaborate";
import config from "@/services/conf"

export default {
  name: "UserList",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userList: []
    }
  },
  methods: {
    load() {
      const id = localStorage.getItem('uid')
      getUserList(id).then(res => {
        // this.userList = res.data;
        this.userList = res.data.filter(user => user.state === 0);
        //设置用户头像
        this.userList = this.userList.map(user => {
          if (user.icon) {
            let icon = user.icon.replace(/\\/g, '/'); // 替换所有反斜杠为斜杠
            icon = user.icon.replace(/App/g, '');
            icon = `${config.API_URL}/${icon}`; // 拼接完整的 URL
            return { ...user, icon }; // 返回更新后的用户对象
          }
          else {
            return { ...user, icon: this.defaultAvatar };
          }
        });
      })
    },
    handleAddFriend(id) {

      const data = { fid: id, uid: localStorage.getItem('uid') }
      addFriend(data).then(res => {
        if (res.success) {
          this.$message({
            message: '好友请求发送成功！',
            type: 'success'
          });
          this.load()
        }
      })
    }
  },
  mounted() {
    this.load()
  },
}
</script>

<style scoped></style>