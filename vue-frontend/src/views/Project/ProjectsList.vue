<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">我的项目</h3>

    <div class="table-container">
      <el-table :data="projectList" style="width: 100%" v-loading="loading">
        <!-- <el-table-column label="项目 ID" prop="id"></el-table-column> -->
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
              <!-- {{ apiKey.id }} - {{ apiKey.name }} -->
              {{ apiKey.name }}
            </div>
          </template>
        </el-table-column>

        <!-- 数据集 列 -->
        <el-table-column label="数据集">
          <template slot-scope="scope">
            <div v-for="data in scope.row.dataSet" :key="data.id">
              <!-- {{ data.id }} - {{ data.name }} -->
              {{ data.name }}
            </div>
          </template>
        </el-table-column>

        <el-table-column label="" width="180" align="center">
          <template slot-scope="scope">
            <el-dropdown>
              <el-button plain size="mini" type="primary">
                操作<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-button plain icon="el-icon-tickets" size="mini" type="primary"
                    @click.stop="handleExperiment(scope.row)"> <!-- 阻止冒泡 -->
                    测试列表
                  </el-button>
                </el-dropdown-item>
                <!-- <el-dropdown-item>
          <el-button plain
            size="mini"
            type="success"
            @click.stop="setCurrentProjectID(scope.row.id, scope.row.name)">
            好友协作
          </el-button>
        </el-dropdown-item> -->
                <el-dropdown-item>
                  <el-button plain icon="el-icon-edit" size="mini" type="warning"
                    @click.stop="showEditDialog(scope.row)"> <!-- 阻止冒泡 -->
                    修改项目配置
                  </el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <!-- <el-popconfirm
            confirm-button-text="确定"
            cancel-button-text="不用了"
            icon="el-icon-info"
            icon-color="red"
            @confirm.stop="removeProject(scope.$index, scope.row)"
            title="确定要删除此项目吗？">
            <el-button plain
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
                    <el-button plain size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
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
      <el-dialog title="修改当前项目" :visible.sync="showDialog" @close="handleDialogClose">

        <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
          <h4>当前项目:{{ currentProjectName }}</h4>
        </div>
        <el-form ref="form" :model="editProject" label-width="100px">
          <el-form-item label="项目名称">
            <el-input v-model="editProject.name"></el-input>
          </el-form-item>

          <el-form-item label="测试说明">
            <el-input v-model="editProject.info"></el-input>
          </el-form-item>

          <el-form-item label="API Key">
            <el-select v-model="editProject.apiKey" placeholder="请选择" multiple>
              <el-option v-for="item in apiKeys" :key="item.id" :label="`${item.id} - ${item.name}`" :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="数据集">
            <el-select v-model="editProject.dataset" placeholder="请选择" multiple>
              <el-option v-for="item in dataSet" :key="item.id" :label="`${item.id} - ${item.name}`" :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button plain @click="handleDialogClose">取消</el-button>
          <el-button plain type="primary" @click="confirmEdit">确定</el-button>
        </span>
      </el-dialog>
    </template>

  </div>
</template>


<script>

import { getProjectsByUserId, deleteById } from '@/api/project'
import { getExperimentByProjectId, deleteOperationFile } from '@/api/experiment'
import { addProject, addApiKeyToProject, addDataSetToProject } from "@/api/project";
import { findApiKeyByUserId } from "@/api/apiConfig";
import { findDataSetByUserId } from "@/api/dataSetConfig"
// import {addFriendsToProject} from '@/api/project' 
// import { getUserList } from '@/api/collaborate'
export default {
  name: "ProjectList",
  data() {
    return {
      loading: true,
      showDialog: false,
      currentProjectId: '',
      currentProjectName: '',
      projectList: [],
      editProject: { name: '', info: '', apiKey: [], dataset: [] },
      apiKeys: [],
      dataSet: [],
      experimentList: [],
      // userFriends: [],
      // selectFriendsId: []
    }
  },
  mounted() {
    this.load()
    setTimeout(() => {
      this.loading = false
    }, 300);
  },
  methods:
  {
    load() {
      if (localStorage.getItem("uid") !== null) {
        const id = localStorage.getItem("uid")
        getProjectsByUserId(id).then(res => {
          this.projectList = res.data;
        })
        findApiKeyByUserId(id).then(res => {
          this.apiKeys = res.data;
          console.log('获取的apikeys', this.apiKeys)
        })
        findDataSetByUserId(id).then(res => {
          this.dataSet = res.data;
          console.log('获取的dataSet', this.dataSet)
        })
        //获取用户列表
        // getUserList(id).then(res => {
        //   this.userFriends = res.data;
        // })
      }
    },
    removeProject(index, row) {
      this.deleteConfig(row)
        .then(() => {
          // 删除配置文件成功后，进行项目删除
          const data = {
            id: row.id
          };
          deleteById(data).then(res => {
            if (res.success) {
              this.projectList.splice(index, 1);
              this.$message({
                message: '删除成功',
                type: 'success',
              });
            }
          });
        })
        .catch(error => {
          // 处理删除配置文件时发生的错误
          console.error('删除配置文件失败:', error);
        });
    },
    handleDialogClose() {
      this.editProject.name = '',
        this.editProject.info = '',
        this.editProject.apiKey = [],
        this.editProject.dataset = [],
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
    handleExperiment(project) {
      console.log('该项目', project)
      if (project.apiKey.length === 0) {
        this.$message({
          message: '请重新配置API key',
          type: 'warning'
        });
        return
      }
      else if (project.dataSet.length === 0) {
        this.$message({
          message: '请重新配置数据集',
          type: 'warning'
        });
      }
      else {
        localStorage.setItem('thisProject', JSON.stringify(project));
        this.$router.push("/experimentList")
      }
    },
    showEditDialog(row) {
      this.currentProjectId = row.id
      this.currentProjectName = row.name
      this.editProject.name = row.name
      this.editProject.info = row.info
      this.showDialog = true
    },
    confirmEdit() {
      this.$confirm('是否修改该项目？这样做会清空其中的所有测试', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.handleEditProject()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消修改'
        });
      });
    },
    handleEditProject() {
      if (this.editProject.name.trim() && this.editProject.info.trim()) {
        if (this.editProject.apiKey.length > 0 && this.editProject.dataset.length > 0) {
          this.deleteConfig(row)
            .then(() => {
              const dataDelete = {
                id: this.currentProjectId
              }
              deleteById(dataDelete).then(res => {
                if (res.success) {
                  const dataAdd = {
                    uid: localStorage.getItem('uid'),
                    name: this.editProject.name,
                    info: this.editProject.info,
                  }
                  addProject(dataAdd).then(res => {
                    if (res.success) {
                      this.editProject.name = '';
                      this.editProject.info = ''; // 清空输入框
                      let projectId = res.id
                      // this.newProject.apiKey = [];
                      // this.newProject.dataset = [];

                      //将用户选择的apiKeys加入到project里面
                      Promise.all(this.editProject.apiKey.map(AK_id => {
                        const addApi = {
                          pid: projectId,
                          AKid: AK_id
                        }
                        addApiKeyToProject(addApi)
                      }))
                      this.editProject.apiKey = []//将用户选择的apikey列表置空

                      //将用户选择的dataSet加入到project里面
                      Promise.all(this.editProject.dataset.map(DS_id => {
                        const addDS = {
                          pid: projectId,
                          DSid: DS_id
                        }
                        addDataSetToProject(addDS)
                      }))
                      this.editProject.dataset = []//将用户选择的dataset列表置空
                      this.$message({
                        message: '修改成功',
                        type: 'success'
                      });
                      this.showDialog = false
                      setTimeout(() => {
                        this.load()
                      }, 500);
                    }
                  })
                }
                else {
                  this.$message({
                    message: '修改出错',
                    type: 'error'
                  });
                }
              })
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
    },
    deleteConfig(thisProject) {
      return new Promise((resolve, reject) => {
        getExperimentByProjectId(thisProject.id).then(res => {
          this.experimentList = res.data;
          const deletePromises = this.experimentList.map(item => {
            if (item.configURL) {
              const deleteData = { tPid: item.id };
              return deleteOperationFile(deleteData).then(res => {
                if (!res.success) {
                  this.$message({
                    message: thisProject.id + '-' + thisProject.name + '测试配置文件删除出错',
                    type: 'error'
                  });
                  throw new Error('删除配置文件失败');
                }
              });
            } else {
              return Promise.resolve();  // 没有配置文件也须返回resolved promise
            }
          });

          Promise.all(deletePromises)
            .then(() => resolve())
            .catch(error => reject(error));
        });
      });
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