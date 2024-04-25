<template>
  <div style="overflow-x: hidden;">
    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的好友</h3>
    <template v-if="userFriends&&userFriends.length">
      <el-row :gutter="20">
        <el-col :span="12" v-for="(row, index) in userFriends" :key="index" class="user-card">
          <!-- <div v-for="(item, index) in friendsInfo" :key="index"> -->
          <el-card>
            <div style="display: flex; align-items: center;">
              <img :src="row.icon" style="width: 50px; height: 50px; border-radius: 50%;" @error="handleImageError" />
              <div style="margin-left: 10px;">
                <p>用户名:{{ row.name }}</p>
                <!-- <p>用户ID:{{ row.id }}</p> -->
                <p>IP地址:{{ row.ip }}
                  <span v-if="row.ip == null" style="color: red; margin-right: 10px;">用户已登出</span>
                  <span v-else-if="row.ip != null && row.state == -1" style="color: red;">用户不在同一局域网下</span>
                </p>
                <p>电话号码:{{ friendsInfo[index].data.tel }}</p>
                <p>邮箱:{{ friendsInfo[index].data.email }}</p>

                <!-- <el-descriptions title="用户信息">
                  <el-descriptions-item label="用户名">{{  row.name }}</el-descriptions-item>
                  <el-descriptions-item label="用户ID">{{ row.id }}</el-descriptions-item>
                  <el-descriptions-item label="IP地址">{{ row.ip  }}</el-descriptions-item>
                  <el-descriptions-item label="电话号码">{{ item.data.tel }}</el-descriptions-item>
                  <el-descriptions-item label="邮箱">{{ item.data.email }}</el-descriptions-item>
                </el-descriptions> -->

                <!-- Conditional rendering for online/offline status -->
                <!-- <p v-else style="color: red;">离线</p> -->
              </div>
            </div>
            <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info" icon-color="red"
              @confirm="handleDeleteFriend(row.id, index)" title="确定要删除此好友吗？">
              <el-button plain type="danger" slot="reference">删除好友</el-button>
            </el-popconfirm>
          </el-card>
          <!-- </div> -->
        </el-col>
      </el-row>
    </template>
    <div v-else class="emptyFriendsRequests">
      <el-empty description="暂无好友"></el-empty>
    </div>
  </div>
</template>


<script>
// import { getUserFriendsById} from "@/api/collaborate";
import { getUserList } from "@/api/collaborate";
import { deleteById } from "@/api/collaborate";
import { findById } from "@/api/user"
import config from "@/services/conf"

export default {
  name: "UserList",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userFriends: [],
      friendsInfo: []
    }
  },
  methods: {
    load() {
      const id = localStorage.getItem('uid')
      getUserList(id).then(res => {
        this.userFriends = res.data.filter(user => user.state === 1||user.state === -1);
        console.log('我的好友', this.userFriends)
        // 更新 userFriends 列表中每个用户的 iconUrl
        this.userFriends = this.userFriends.map(user => {
          if (user.icon) {
            let icon = user.icon.replace(/\\/g, '/'); // 替换所有反斜杠为斜杠
            icon = icon.replace(/App/g, '');
            icon = config.API_URL + icon; // 拼接完整的 URL
            return { ...user, icon }; // 返回更新后的用户对象
          }
          else {
            return { ...user, icon: this.defaultAvatar };
          }
        });
        Promise.all(this.userFriends.map(friend => {
          const fidObject = { id: friend.id };
          return findById(fidObject);
        }))
          .then(res => {
            this.friendsInfo = res
            // console.log('用户好友信息:',this.friendsInfo)
          })
      })
    },
    handleDeleteFriend(id, index) {
      const uid = localStorage.getItem('uid')
      deleteById(id, uid).then(res => {
        if (res.success) {
          this.userFriends.splice(index, 1);
          this.$message({
            message: '好友已删除',
            type: 'warning'
          });
          this.load()
        }
      })
    },
    handleImageError(event){
      event.target.src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"
    }
  },
  mounted() {
    this.load()
  },

}
</script>

<style scoped>
.user-card {
  margin-top: 20px;
  /* 设置顶部外边距 */
  margin-bottom: 10px;
  /* 设置底部外边距 */
}
</style>