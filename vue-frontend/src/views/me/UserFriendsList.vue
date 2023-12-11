<template>
  <div style="overflow-x: hidden;">
    <el-row :gutter="20">
      <el-col :span="24" v-for="user in userFriends" :key="user.id">
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
          <el-popconfirm
              confirm-button-text="确定"
              cancel-button-text="不用了"
              icon="el-icon-info"
              icon-color="red"
              @confirm="handleDeleteFriend(user.id)"
              title="确定要删除此好友吗？">
            <el-button type="danger" slot="reference">删除好友</el-button>
          </el-popconfirm>
          <el-button v-if="user.ip" type="warning" style="margin-left: 10px;">发消息</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import {getUserFriendsById, deleteById} from "@/api/collaborate";

export default {
  name: "UserList",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userFriends: [
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
      getUserFriendsById(id).then(res => {
        this.userFriends = res.data;
      })
    },
    handleDeleteFriend(id) {
      const uid=localStorage.getItem('uid')
      deleteById(id,uid).then(res => {
        if (res.success) {
          this.$message({
            message: '好友已删除！',
            type: 'warning'
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
    this.userFriends = this.userFriends.map(user => ({
      ...user,
      iconUrl: user.iconUrl || this.defaultAvatar
    }));
  }

}
</script>

<style scoped>

</style>