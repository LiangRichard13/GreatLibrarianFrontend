<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的项目</h3>

    <div class="table-container">
      <el-table :data="projectList" style="width: 100%">
        <el-table-column label="项目 ID" prop="id"></el-table-column>
        <el-table-column label="项目名称" prop="name"></el-table-column>
        <el-table-column label="测试说明" prop="info"></el-table-column>

         <!-- 协作者 列 -->
         <!-- <el-table-column label="协作者">
          <template slot-scope="scope">
            <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
              {{collaborator.name}}
            </div>
          </template>
        </el-table-column> -->

        <!-- LLM 列 -->
        <el-table-column label="LLM">
          <template slot-scope="scope">
            <div v-for="apiKey in scope.row.apiKey" :key="apiKey.id">
              {{ apiKey.id }} - {{ apiKey.name }}
            </div>
          </template>
        </el-table-column>

        <!-- 数据集 列 -->
        <el-table-column label="数据集">
          <template slot-scope="scope">
            <div v-for="data in scope.row.dataSet" :key="data.id">
              {{ data.id }} - {{ data.name }}
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180" align="center">
  <template slot-scope="scope">
    <el-dropdown>
      <el-button size="mini" type="primary">
        操作<i class="el-icon-arrow-down el-icon--right"></i>
      </el-button>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>
          <el-button
            size="mini"
            type="primary"
            @click.stop="handleExperiment(scope.row)"> <!-- 阻止冒泡 -->
            实验列表
          </el-button>
        </el-dropdown-item>
        <!-- <el-dropdown-item>
          <el-button
            size="mini"
            type="success"
            @click.stop="setCurrentProjectID(scope.row.id, scope.row.name)">
            好友协作
          </el-button>
        </el-dropdown-item> -->
        <el-dropdown-item>
          <!-- <el-popconfirm
            confirm-button-text="确定"
            cancel-button-text="不用了"
            icon="el-icon-info"
            icon-color="red"
            @confirm.stop="removeProject(scope.$index, scope.row)"
            title="确定要删除此项目吗？">
            <el-button
            icon="el-icon-delete"
              size="mini"
              type="danger"
              slot="reference"
              @click.stop>
              删除
            </el-button>
          </el-popconfirm> -->
          <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info" icon-color="red"
              @confirm="removeProject(scope.$index, scope.row)" title="确定要删除此项目吗？">
              <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
              </el-button>
            </el-popconfirm>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </template>
</el-table-column>
      </el-table>
    </div>
    <!-- 将好友加入到项目协作的对话框 -->
    <!-- <template>
  
      <el-dialog title="请为当前项目添加协作者" :visible.sync="showDialog" @close="handleDialogClose">

        <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
          <h4>当前项目：{{ currentProjectId }} - {{ currentProjectName }}</h4>
        </div>

        <el-checkbox-group v-model="selectFriendsId">
          <el-checkbox v-for="friend in userFriends" :label="friend.id" :key="friend.id">
            {{ friend.id }} - {{ friend.username }}
          </el-checkbox>
        </el-checkbox-group>

        <span slot="footer" class="dialog-footer">
          <el-button @click="handleDialogClose">取消</el-button>
          <el-button type="primary" @click="friendsToProject">确定</el-button>
        </span>
      </el-dialog>
    </template> -->

  </div>
</template>


<script>

import {getProjectsByUserId, deleteById } from '@/api/project'
// import {addFriendsToProject} from '@/api/project' 
// import { getUserList } from '@/api/collaborate'
export default {
  name: "ProjectList",
  data() {
    return {
      showDialog: false,
      currentProjectId: '',
      currentProjectName: '',
      projectList: [],
      // userFriends: [],
      // selectFriendsId: []
    }
  },
  mounted() {
    this.load()
  },
  methods:
  {
    load() {
      if (localStorage.getItem("uid") !== null) {
        const id = localStorage.getItem("uid")
        getProjectsByUserId(id).then(res => {
          this.projectList = res.data;
        })
        //获取用户列表
        // getUserList(id).then(res => {
        //   this.userFriends = res.data;
        // })
      }
    },
    removeProject(index, row) {
      const data={
        id:row.id
      }
      deleteById(data).then(res => {
        if (res.success) {
          this.projectList.splice(index, 1);
          this.$message({
            message: '删除成功',
            type: 'success',
          });
        }
      })
    },
    setCurrentProjectID(projectId, projectName) {
      this.currentProjectId = projectId
      this.currentProjectName = projectName
      this.showDialog = true
    },
    handleDialogClose() {
      this.selectFriendsId = []; // 清除选择
      this.showDialog = false; // 关闭对话框
    },

    //将好友加入到项目协作
    // friendsToProject() {
    //   const data = { id: this.currentProjectId, uid: this.selectFriendsId }
    //   addFriendsToProject(data).then(res => {
    //     if (res.success) {
    //       this.$message({
    //         message: '已为项目添加协作者！',
    //         type: 'success',
    //       });
    //       this.load()
    //     }
    //   })
    //   this.handleDialogClose(); // 关闭对话框
    // },
    handleExperiment(project){
      localStorage.setItem('thisProject', JSON.stringify(project));
      this.$router.push("/experimentList")
    }
  }
}


</script>

<style scoped>
.table-container {
  max-width: 2000px;
  /* 设置你希望的最大宽度 */
  margin: auto;
  /* 这将使得表格居中 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  /* 可选：添加阴影效果 */
  padding: 20px;
  /* 可选：添加一些内边距 */
  border: 1px solid #ebeef5;
  /* 根据你的截图，看起来你需要一个边框 */
}

.main {
  padding: 20px;
}
</style>