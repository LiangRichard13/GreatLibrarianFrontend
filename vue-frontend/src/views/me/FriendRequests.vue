<template lang="">
<div style="overflow-x: hidden;">
  <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的好友申请</h3>
    <el-row :gutter="20">
      <el-col :span="12" v-for="(row,index) in userFriendsRequest" :key="index" class="user-card"> 
        <el-card>
          <div style="display: flex; align-items: center;">
            <img :src="row.data.iconUrl" style="width: 50px; height: 50px; border-radius: 50%;" />
            <div style="margin-left: 10px;">
              <p>用户名:{{ row.data.name }}</p>
              <p>用户ID:{{ row.data.id }}</p>
            </div>
          </div>
          <el-button type="success" @click='handleAgree(row)'>同意申请</el-button>
          <el-button type="danger" @click='handleRefuse(row,index)'>拒绝申请</el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getFriendsRequest } from '@/api/collaborate'
import { handleFriendRequest } from '@/api/collaborate'
import { findById } from "@/api/user"
import config from "@/services/conf"
export default {
  name: "FriendsRequests",
  data() {
    return {
      defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
      userFriendsRequestID: [],
      userFriendsRequest: []
    }
  },
  mounted() {
    this.load()
  },
  methods: {
    load() {
      const id = localStorage.getItem('uid')
      getFriendsRequest(id).then(res => {
        this.userFriendsRequestID = res.fid;

        if (this.userFriendsRequestID) {
          Promise.all(this.userFriendsRequestID.map(fid => {
            const fidObject = { id: fid };
            return findById(fidObject);
          }))
            .then(res => {
              this.userFriendsRequest = res
              console.log("userFriendsRequest", this.userFriendsRequest)
            })
          //设置用户头像
          this.userFriendsRequest = this.userFriendsRequest.map(user => {
            if (user.data.iconUrl) {

              
              // 替换所有反斜杠为斜杠
              let iconUrl = user.data.iconUrl.replace(/\\/g, '/');

              // 移除 'App' 字符串
              iconUrl = iconUrl.replace(/App/g, "");

              // 拼接完整的 URL
              iconUrl = `${config.API_URL}/${iconUrl}`;
              return { ...user.data, iconUrl }; // 返回包含更新后的 iconUrl 的用户信息对象
            } else {
              return { ...user.data, iconUrl: this.defaultAvatar };
            }
          });


        }
      })
    },
  },
  handleAgree(row) {
    const agreedData = {
      fid: row.id,
      uid: localStorage.getItem('uid'),
      result: true
    }
    handleFriendRequest(agreedData).then(res => {
      if (res.success) {
        this.$message({
          message: '已同意好友请求！',
          type: 'success'
        });
        this.load()
      }
    })
  },
  handleRefuse(row, index) {
    const refuseData = {
      fid: row.id,
      uid: localStorage.getItem('uid'),
      result: false
    }
    handleFriendRequest(refuseData).then(res => {
      if (res.success) {
        this.userFriendsRequest.splice(index, 1);
        this.$message({
          message: '已拒绝好友申请！',
          type: 'warning'
        });
      }
    })

  }
}
</script>
<style scope>
.user-card {
  margin-top: 20px;
  /* 设置顶部外边距 */
  margin-bottom: 10px;
  /* 设置底部外边距 */
}
</style>