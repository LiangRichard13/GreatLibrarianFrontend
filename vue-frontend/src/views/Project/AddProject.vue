<template>
  <div>
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
      <el-button type="success" icon="el-icon-plus" size="large" @click="showDialog=true">
        创建新实验
      </el-button>
    </div>

    <el-dialog
        title="创建项目"
        :visible.sync="showDialog"
        width="30%"
        @close="resetDialog">
      <div>
        <el-form ref="form" :model="newProject" label-width="100px">
          <el-form-item label="项目名称">
            <el-input v-model="newProject.name"></el-input>
          </el-form-item>

          <el-form-item label="测试说明">
            <el-input v-model="newProject.description"></el-input>
          </el-form-item>

          <el-form-item label="API Key">
          <el-select v-model="newProject.apiKey" placeholder="请选择">
            <el-option
                v-for="item in apiKeys"
                :key="item.id"
                :label="`${item.name} - ${item.value}`"
                :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据集">
          <el-select v-model="newProject.dataset" placeholder="请选择">
            <el-option
                v-for="item in dataSet"
                :key="item.id"
                :label="`${item.name} - ${item.info}`"
                :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="handleAddProject">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {addProject} from "@/api/project";
import {findByUserId} from "@/api/apiConfig";

export default {
  name: "AddProject",
  data() {
    return {
      showDialog: false,
      newProject: {name: '', description: '', apiKey: '', dataset: ''},
      apiKeys: [{id: '1', name: '文心一言', value: '123'}, {id: 2, name: 'openAI', value: '12345'}],
      dataSet: [{id: '1', name: '文心一言', info: '123'}, {id: '1', name: 'chatGpt', info: '123'}],
    }
  },
  mounted() {

  },
  methods:
      {
        load() {
          if (localStorage.getItem("uid") !== null) {
            const id = parseInt(localStorage.getItem("uid"))
            findByUserId(id).then(res => {
              this.apiKeys = res.data;
            })
            findByUserId(id).then(res => {
              this.dataSet = res.data;
            })
          }
        },
        resetDialog() {
          this.newProject.name = '';
          this.newProject.description = '';// 重置输入
          this.newProject.apiKey = '';
          this.newProject.dataset = '';
        },
        handleAddProject() {
          if (this.newProject.name.trim() && this.newProject.description.trim()) {
            const data = {
              name: this.newProject.name,
              description: this.newProject.description,
              apiKeyId: this.newProject.apiKey, // 确保包括了 apiKey
              datasetId: this.newProject.dataset // 确保包括了 dataset
            }
            addProject(data).then(res => {
              if (res.success) {
                this.newProject.name = '';
                this.newProject.description = ''; // 清空输入框
                this.newProject.apiKey = '';
                this.newProject.dataset = '';
                this.showDialog = false; // 关闭对话框
                this.$message({
                  message: '添加成功',
                  type: 'success'
                });
              }
            })
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

<style scoped>

</style>