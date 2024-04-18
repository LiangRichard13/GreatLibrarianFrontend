<template>
  <div style="display: flex; flex-direction: column; align-items: center; justify-content: start; height: 100vh;">
    <div style="width: 30%; margin-top: 20px;">
      <el-form ref="form" :model="newProject" label-width="100px">
        <el-form-item label="项目名称">
          <el-input v-model="newProject.name"></el-input>
        </el-form-item>

        <el-form-item label="测试说明">
          <el-input v-model="newProject.info"></el-input>
        </el-form-item>

        <el-form-item label="API Key">
          <el-select v-model="newProject.apiKey" placeholder="请选择" multiple>
            <el-option v-for="item in apiKeys" :key="item.id" :label="`${item.id} - ${item.name}`" :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据集">
          <el-select v-model="newProject.dataset" placeholder="请选择" multiple>
            <el-option v-for="item in dataSet" :key="item.id" :label="`${item.id} - ${item.name}`" :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <div style="display: flex; justify-content: center; margin-top: 20px;">
          <el-button plain type="success" icon="el-icon-plus" size="large" @click="handleAddProject">
            创建新项目
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { addProject,addApiKeyToProject,addDataSetToProject } from "@/api/project";
import { findApiKeyByUserId } from "@/api/apiConfig";
import { findDataSetByUserId } from "@/api/dataSetConfig"

export default {
  name: "AddProject",
  data() {
    return {
      newProject: { name: '', info: '', apiKey: [], dataset: [] },
      // newProject: { name: '', info: ''},
      apiKeys: [],
      dataSet:[],
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
        findApiKeyByUserId(id).then(res => {
          this.apiKeys = res.data;
          console.log('获取的apikeys',this.apiKeys)
        })
        findDataSetByUserId(id).then(res => {
          this.dataSet = res.data;
          console.log('获取的dataSet',this.dataSet)
        })
      }
    },
    handleAddProject() {
      if (this.newProject.name.trim() && this.newProject.info.trim()) {
        if (this.newProject.apiKey.length > 0 && this.newProject.dataset.length > 0) {
          const data = {
            uid:localStorage.getItem('uid'),
            name: this.newProject.name,
            info: this.newProject.info,
            // LLM: this.newProject.apiKey, // 确保包括了 apiKey
            // DSid: this.newProject.dataset // 确保包括了 dataset
          }
          addProject(data).then(res => {
            if (res.success) {
              this.newProject.name = '';
              this.newProject.info = ''; // 清空输入框
              let projectId=res.id
              // this.newProject.apiKey = [];
              // this.newProject.dataset = [];

              //将用户选择的apiKeys加入到project里面
              Promise.all(this.newProject.apiKey.map(AK_id=>{
                const addApi={
                  pid:projectId,
                  AKid:AK_id
                }
                addApiKeyToProject(addApi)
              }))
              this.newProject.apiKey=[]//将用户选择的apikey列表置空

              //将用户选择的dataSet加入到project里面
              Promise.all(this.newProject.dataset.map(DS_id=>{
                const addDS={
                  pid:projectId,
                  DSid:DS_id
                }
                addDataSetToProject(addDS)
              }))
              this.newProject.dataset=[]//将用户选择的dataset列表置空
              this.$message({
                message: '添加成功',
                type: 'success'
              });
            }
          })
        }
        else {
          this.$message({
            message: '请选择apikey和数据集',
            type: 'warning'
          });
        }
      } else {
        this.$message({
          message: '项目名或测试说明不能为空',
          type: 'warning'
        });
      }
    }
  }
}
</script>

<style scoped></style>