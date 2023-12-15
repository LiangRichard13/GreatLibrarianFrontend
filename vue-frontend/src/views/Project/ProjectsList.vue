<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的项目</h3>

    <div class="table-container">
      <el-table :data="projectList" style="width: 100%">
        <el-table-column label="项目 ID" prop="id"></el-table-column>
        <el-table-column label="项目名称" prop="name"></el-table-column>
        <el-table-column label="测试说明" prop="description"></el-table-column>

         <!-- 协作者 列 -->
         <el-table-column label="协作者">
          <template slot-scope="scope">
            <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
              {{collaborator.name}}
            </div>
          </template>
        </el-table-column>

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
        <el-dropdown-item>
          <el-button
            size="mini"
            type="success"
            @click.stop="setCurrentProjectID(scope.row.id, scope.row.name)"> <!-- 阻止冒泡 -->
            好友协作
          </el-button>
        </el-dropdown-item>
        <el-dropdown-item>
          <el-popconfirm
            confirm-button-text="确定"
            cancel-button-text="不用了"
            icon="el-icon-info"
            icon-color="red"
            @confirm.stop="removeDataSet(scope.$index, scope.row)"
            title="确定要删除此项目吗？">
            <el-button
            icon="el-icon-delete"
              size="mini"
              type="danger"
              slot="reference"
              @click.stop> <!-- 阻止冒泡 -->
              删除
            </el-button>
          </el-popconfirm>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </template>
</el-table-column>
      </el-table>
    </div>
    <template>
      <!-- 对话框 -->
      <el-dialog title="请为当前项目添加协作者" :visible.sync="showDialog" @close="handleDialogClose">

        <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
          <h4>当前项目：{{ currentProjectId }} - {{ currentProjectName }}</h4>
        </div>

        <!-- 复选框列表 -->
        <el-checkbox-group v-model="selectFriendsId">
          <el-checkbox v-for="friend in userFriends" :label="friend.id" :key="friend.id">
            {{ friend.id }} - {{ friend.username }}
          </el-checkbox>
        </el-checkbox-group>

        <!-- 操作按钮 -->
        <span slot="footer" class="dialog-footer">
          <el-button @click="handleDialogClose">取消</el-button>
          <el-button type="primary" @click="friendsToProject">确定</el-button>
        </span>
      </el-dialog>
    </template>

  </div>
</template>


<script>

import { addFriendsToProject, getProjectsByUseId, deleteById } from '@/api/project'
import { getUserFriendsById } from '@/api/collaborate'
export default {
  name: "ProjectList",
  data() {
    return {
      showDialog: false,
      currentProjectId: '',
      currentProjectName: '',
      projectList: [
        {
          id: '1',
          name: 'FirstProject',
          description: 'This is a test',
          collaborators:[{id:'1',name:'Alice'},{id:'2',name:'Bob'}],
          apiKey: [{ id: '1', name: '文心一言', value: '123', auth: 'xxx' }, { id: '2', name: 'openAI', value: '12345', auth: 'xxx' }],
          dataSet: [
            {
              id: '1',
              name: '文心一言',
              info: '文心一言的测试数据集',
              fileURL: 'http://localhost:8080/dataSetFile/1'
            },
            {
              id: '2',
              name: 'chatGpt',
              info: 'chatGPT的测试数据集',
              fileURL: 'http://localhost:8080/dataSetFile/2'
            }],

        }
      ],
      userFriends: [
        {
          id: '1',
          username: "Alice",
          iconUrl: "",
          ip: "192.168.1.1"
        },
        {
          id: '2',
          username: "Bob",
          iconUrl: "",
          ip: ""
        },
        {
          id: '3',
          username: "Charlie",
          iconUrl: "",
          ip: "192.168.1.3"
        },],
      selectFriendsId: []
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
        getProjectsByUseId(id).then(res => {
          this.projectList = res.data;
        })
        getUserFriendsById(id).then(res => {
          this.userFriends = res.data;
        })
      }
    },
    removeProject(index, row) {
      const deleteId = row.id
      deleteById(deleteId).then(res => {
        if (res.success) {
          this.dataSet.splice(index, 1);
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
    friendsToProject() {
      const data = { id: this.currentProjectId, uid: this.selectFriendsId }
      addFriendsToProject(data).then(res => {
        if (res.success) {
          this.$message({
            message: '已为项目添加协作者！',
            type: 'success',
          });
          this.load()
        }
      })
      this.handleDialogClose(); // 关闭对话框
    },
    handleExperiment(project){
      this.$router.push({ path: `/experimentList`,query: project});
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