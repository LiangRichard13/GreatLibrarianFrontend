<template>
  <div style="overflow-x: hidden">
    <el-row :gutter="20">
      <el-col :span="24" v-for="user in userList" :key="user.id">
        <el-card>
          <div style="display: flex; align-items: center;">
            <img :src="user.iconUrl" style="width: 50px; height: 50px; border-radius: 50%;"/>
            <div style="margin-left: 10px;">
              <p>用户名：{{ user.username }}</p>
              <p>用户ID：{{ user.id }}</p>
              <p>IP地址：{{ user.ip }}</p>

              <!-- Conditional rendering for online/offline status -->
              <p v-if="user.ip" style="color: green;">在线</p>
              <p v-else style="color: red;">离线</p>
            </div>
          </div>
          <el-button type="primary" @click="handleAddFriend(user.id)">添加好友</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {getUserList, addFriend} from "@/api/collaborate";

export default {
  name: "UserList",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userList: [
        {
          id:'1',
          username: "Alice",
          iconUrl: "",
          ip: "192.168.1.1"
        },
        {
          id:'2',
          username: "Bob",
          iconUrl: "",
          ip: ""
        },
        {
          id:'3',
          username: "Charlie",
          iconUrl: "",
          ip: "192.168.1.3"
        },]
    }
  },
  methods: {
    load() {
      const id = localStorage.getItem('uid')
      getUserList(id).then(res => {
        this.userList = res.data;
      })
    },
    handleAddFriend(id) {

      const data = {id: id,uid:localStorage.getItem('uid')}
      addFriend(data).then(res => {
        if (res.success) {
          this.$message({
            message: '好友请求发送成功！',
            type: 'success'
          });
        }
      })
      this.load()
    }
  },
  mounted() {
    // this.load()
  },
  created() {
    // 设置默认头像
    this.userList = this.userList.map(user => ({
      ...user,
      iconUrl: user.iconUrl || this.defaultAvatar
    }));
  }

}
</script>

<style scoped>

</style>