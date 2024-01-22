<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的协作项目</h3>

    <div class="table-container">
      <el-table :data="projectList" style="width: 100%">
        <el-table-column label="项目 ID" prop="id"></el-table-column>
        <el-table-column label="项目名称" prop="name"></el-table-column>
        <el-table-column label="测试说明" prop="info"></el-table-column>

        <!-- 协作者 列 -->
        <el-table-column label="协作者">
          <template slot-scope="scope">
            <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
              {{ collaborator.name }}
            </div>
          </template>
        </el-table-column>

        <!-- LLM 列 -->
        <el-table-column label="LLM">
          <template slot-scope="scope">
            <div v-for="apiKey in scope.row.apikey" :key="apiKey.id">
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
            <el-button   style="margin-left: 8px"
              size="mini"
              type="primary"
              slot="reference" @click=" InCollaboration(scope.row)">
            参与协作
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>


<script>

import { getCollaborateProjectsByUserId } from '@/api/project'
export default {
  name: "MyCollaborate",
  data() {
    return {
      projectList: [
        {
          id: '1',
          name: 'FirstProject',
          info: 'This is a test',
          collaborators: [{ id:'1',name: 'Alice' }, { id:'2',name: 'Bob' }],
          apikey: [{ id: '1', name: '文心一言', value: '123', auth: 'xxx' }, { id: '2', name: 'openAI', value: '12345', auth: 'xxx' }],
          dataSet: [
            {
              id: '1',
              name: '文心一言',
              info: '文心一言的测试数据集',
              url: 'http://localhost:8080/dataSetFile/1'
            },
            {
              id: '2',
              name: 'chatGpt',
              info: 'chatGPT的测试数据集',
              url: 'http://localhost:8080/dataSetFile/2'
            }],

        }
      ],
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
        getCollaborateProjectsByUserId(id).then(res => {
          this.projectList = res.data;
        })
      }
    },
    InCollaboration(project){
      localStorage.setItem('thisProject', JSON.stringify(project));
      this.$router.push("experimentCollaborate")
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