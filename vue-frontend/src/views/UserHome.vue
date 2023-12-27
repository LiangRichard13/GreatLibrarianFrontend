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
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>我的好友</span>
              </div>
              <template v-if="friends && friends.length">
                <div v-for="friend in friends" :key="friend.id" class="friend-card">
                  <el-avatar :src="friend.avatar"></el-avatar>
                  <div class="friend-info">
                    <span>{{ friend.username }}</span>
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
export default {
  name: "userHome"
}
</script>

<style scoped>

</style>