<template lang="">
<div style="overflow-x: hidden;">
    <el-row :gutter="20">
      <el-col :span="12" v-for="(row,index) in userFriendsRequest" :key="index" class="user-card"> 
        <el-card>
          <div style="display: flex; align-items: center;">
            <img :src="row.iconUrl" style="width: 50px; height: 50px; border-radius: 50%;" />
            <div style="margin-left: 10px;">
              <p>用户名:{{ row.username }}</p>
              <p>用户ID:{{ row.userId }}</p>
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
// import { getFriendsRequest } from '@/api/collaborate'
import { handleFriendRequest} from '@/api/collaborate'
import config from "@/services/conf"
export default {
    name: "FriendsRequests",
    data() {
        return {
            defaultAvatar: require('@/assets/avatar.png'), // 设置默认头像路径
            userFriendsRequest:
                [
                    {
                        id: '1',
                        userId: '3',
                        username: "Alice",
                        iconUrl: null,
                    },
                    {
                        id: '2',
                        userId: '4',
                        username: "Bob",
                        iconUrl: null,
                    },
                    {
                        id: '3',
                        userId: '5',
                        username: "Jack",
                        iconUrl:null,
                    },
                    {
                        id: '4',
                        userId: '6',
                        username: "Rose",
                        iconUrl: null,
                    },
                ]
        }
    },
    mounted() {
        this.load()
    },
    methods: {
        load() {
            // const id = localStorage.getItem('uid')
            // getFriendsRequest(id).then(res => {
            //     this.userFriendsRequest = res.data;
            // })

            //设置用户头像
            this.userFriendsRequest = this.userFriendsRequest.map(user => {
                if (!user.iconUrl) {
                    let iconUrl = user.iconUrl.replace(/\\/g, '/'); // 替换所有反斜杠为斜杠
                    iconUrl = `${config.API_URL}/${iconUrl}`; // 拼接完整的 URL
                    return { ...user, iconUrl }; // 返回更新后的用户对象
                }
                else {
                    return { ...user, iconUrl: this.defaultAvatar };
                }
            });
        },
    },
    handleAgree(row) {
        const requestId = row.id
        handleFriendRequest(requestId).then(res => {
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
      handleFriendRequest(row.id).then(res => {
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