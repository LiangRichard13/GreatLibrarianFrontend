<template>
  <div class="main">

    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px;">
      <div style="flex: 1; display: flex; justify-content: center;">
        <h3 style="letter-spacing: 1px; font-weight: 400; margin: 0;">API_KEY配置</h3>
      </div>
      <el-button plain icon="el-icon-circle-plus" type="success" @click="showDialog = true">添加API_KEY</el-button>
    </div>




    <div class="table-container">
      <el-table :data="apiKeys" style="width: 100%" v-loading="loading">
        <!-- <el-table-column prop="id" label="API_KEY ID" width="300%"></el-table-column> -->
        <el-table-column prop="name" label="大模型名称" width="150%"></el-table-column>
        <el-table-column prop="value" label="密钥" width="450%"></el-table-column>
        <el-table-column label="调用函数" width="80%">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.callFunction" type="success">已保存</el-tag>
            <el-tag v-else type="warning">未编辑</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="详细描述" align="center">
          <template slot-scope="scope">
            <div style="height: 50px; overflow: auto;">{{ scope.row.intro }}</div>
          </template>
        </el-table-column>
        <!-- <el-table-column type="expand" label="介绍">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="背景介绍:">
                <span>{{ props.row.intro }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column> -->


        <!-- 操作列 -->
        <el-table-column label="操作" width="100%" align="center">
          <template slot-scope="scope">
            <el-dropdown>
              <el-button plain size="mini" type="primary">
                操作<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <el-button plain size="mini" icon="el-icon-edit" type="primary"
                    @click="handleCodeEdit(scope.row.id, scope.row.name, scope.row.callFunction)">编辑调用函数
                  </el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button plain size="mini" icon="el-icon-s-operation" type="warning" @click="handleTest(scope.row)"
                    :loading="connectivityTesting">测试连通性
                  </el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info" icon-color="red"
                    @confirm="removeKey(scope.$index, scope.row)" title="确定要删除此API key吗?">
                    <el-button plain size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                    </el-button>
                  </el-popconfirm>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column label="上次连通性测试" width="230px">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.testResult===0" type="danger" class="testResult">未通过</el-tag>
          <el-tag v-else-if="scope.row.testResult===1" type="success" class="testResult">已通过</el-tag>
          <span v-if="scope.row.testTime"> {{ scope.row.testTime }}</span>
          <el-tag v-else type="info">未测试</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加API_KEY的对话框 -->
    <el-dialog title="添加 API Key" :visible.sync="showDialog" width="30%" @close="resetDialog">
      <div>
        <el-form ref="form" :model="newApiKey" label-width="100px">

          <el-form-item label="大模型名称">
            <el-input v-model="newApiKey.name"></el-input>
          </el-form-item>

          <el-form-item label="密钥">
            <el-input v-model="newApiKey.value"></el-input>
          </el-form-item>

          <el-form-item label="背景介绍">
            <el-input v-model="newApiKey.intro"></el-input>
          </el-form-item>

          <!-- <div>
            <span>
              编辑API Key对应的调用函数
          </span>
             <el-button plain style="margin-left: 8px" size="large" icon="el-icon-s-tools" type="primary" @click="showCodeEditorDialog=true">编辑
              </el-button>
          </div> -->

        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button plain @click="showDialog = false">取 消</el-button>
        <el-button plain type="primary" @click="addKey">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 编辑API Key的调用函数的对话框 -->
    <el-dialog title="编辑API Key对应的Call函数" :visible.sync="showCodeEditorDialog" width="50%" @opened="initPythonEditor()">
      <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
        <h4>当前API Key:{{ currentAkName }}</h4>
      </div>
      <el-button plain @click="loadTemplate(1)">加载被测模型调用函数模板</el-button>
      <el-button plain @click="loadTemplate(2)">加载评估模型调用函数模板</el-button>
      <div>
        <!-- 代码组件 -->
        <h3> 编辑调用函数</h3>
        <div id="python-editor" style="height: 300px;"></div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button plain @click="resetCodeEditor">取消</el-button>
        <el-button plain type="primary" @click="savePythonFile">保存代码</el-button>
      </span>
    </el-dialog>
  </div>
</template>


<script>
import { addApiKey, deleteById, findApiKeyByUserId, getCallFunction, addCallFunction, testConnectivity } from "@/api/apiConfig";
// import {checkOperationFile} from "@/api/experiment"
import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-chrome';

export default {
  name: "ApiConfig",
  data() {
    return {
      connectivityTesting: false,
      loading: true,
      apiKeys: [],
      showDialog: false,
      newApiKey: { name: '', value: '', intro: '' },
      currentAkId: '',
      currentAkName: '',
      currentAkCallFunction: '',
      showCodeEditorDialog: false,
      pythonCode: '',
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
        findApiKeyByUserId(id).then(res => {
          this.apiKeys = res.data;
          // 使用 Promise.all 等待所有 getCallFunction 调用完成
          Promise.all(this.apiKeys.map(item => {
            return getCallFunction(item.id).then(res => {
              item.callFunction = res.code;
              if(localStorage.getItem(item.id+'_testConnectivity_normal'))
              {
                item.testTime=localStorage.getItem(item.id+'_testConnectivity_normal')
                item.testResult=1
              }
              else if(localStorage.getItem(item.id+'_testConnectivity_error'))
              {
                item.testTime=localStorage.getItem(item.id+'_testConnectivity_error')
                item.testResult=0
              }
              else
              {
                item.testTime=null
              }
              return item; // 返回更新后的 item
            });
          })).then(updatedApiKeys => {

            this.apiKeys = updatedApiKeys;
            console.log('经过处理的apikeys',this.apiKeys)
          });
        });
      }
    },
    addKey() {
      if (this.newApiKey.value.trim() && this.newApiKey.name.trim()) {
        if(!this.isValidValue(this.newApiKey.value))
        {
          this.$message({
              message: '密钥形式不符合规范，请检查',
              type: 'warning'
            });
            return
        }
        const data = {
          uid: localStorage.getItem('uid'),
          name: this.newApiKey.name,
          value: this.newApiKey.value,
          intro: this.newApiKey.intro
        }
        addApiKey(data).then(res => {
          if (res.success) {
            this.newApiKey.name = '';
            this.newApiKey.value = ''; // 清空输入框
            this.newApiKey.intro = '';
            this.showDialog = false; // 关闭对话框
            this.$message({
              message: '添加成功',
              type: 'success'
            });
            this.load()
          }
        })
      }
      else {
        this.$message({
          message: '添加API_KEY各字段不能为空',
          type: 'warning'
        });
      }
    },
    removeKey(index, row) {
      const deleteId = { id: row.id }
      deleteById(deleteId).then(res => {
        if (res.success) {
          this.apiKeys.splice(index, 1);
          // localStorage.removeItem(row.id + '_call')
          this.$message({
            message: '删除成功',
            type: 'success',
          });
        }
      })
    },
    resetDialog() {
      this.newApiKey.name = '';
      this.newApiKey.value = '';// 重置输入
      this.newApiKey.intro = '';
    },
    handleCodeEdit(id, name, code) {
      this.currentAkId = id;
      this.currentAkName = name;
      this.currentAkCallFunction = code;
      this.showCodeEditorDialog = true
    },
    loadTemplate(choose) {
      if (choose === 1) {
        fetch('/codeTemplate_L1.txt')
          .then(response => response.text())
          .then(data => {
            this.editorWithTemplate(data);
          })
          .catch(error => {
            console.error('Error loading the template:', error)
            this.$message({
              message: '加载被测模型调用函数模板文件出错',
              type: 'error'
            });
          }
          );
      }
      else if (choose === 2) {
        fetch('/codeTemplate_L2.txt')
          .then(response => response.text())
          .then(data => {
            this.editorWithTemplate(data);
          })
          .catch(error => {
            console.error('Error loading the template:', error)
            this.$message({
              message: '加载评估模型调用函数模板文件出错',
              type: 'error'
            });
          }
          );
      }
    },
    initPythonEditor(template) {
      if (document.getElementById('python-editor')) {
        // 初始化 Ace Editor1
        this.editor = ace.edit("python-editor");
        this.editor.setTheme("ace/theme/chrome"); // 使用亮色主题
        this.editor.session.setMode("ace/mode/python");
        this.editor.setFontSize(18); // 设置字体大小为18px

        if (this.currentAkCallFunction) {
          this.editor.setValue(this.currentAkCallFunction, 1);
        }
        else {
          this.editor.setValue(template, 1);
        }


        this.pythonCode = this.editor.getValue();
        this.editor.session.on('change', () => {
          this.pythonCode = this.editor.getValue();
        });
      } else {
        console.log('The #python-editor element does not exist.')
      }
    },
    editorWithTemplate(template) {
      if (document.getElementById('python-editor')) {
        // 初始化 Ace Editor1
        this.editor = ace.edit("python-editor");
        this.editor.setTheme("ace/theme/chrome"); // 使用亮色主题
        this.editor.session.setMode("ace/mode/python");
        this.editor.setFontSize(18); // 设置字体大小为18px
        this.editor.setValue(template, 1);
        this.pythonCode = this.editor.getValue();
        this.editor.session.on('change', () => {
          this.pythonCode = this.editor.getValue();
        });
      } else {
        console.log('The #python-editor element does not exist.')
      }
    },
    resetCodeEditor() {
      this.pythonCode = '',
        this.showCodeEditorDialog = false
    },
    savePythonFile() {
      if (this.pythonCode === '') {
        this.$message({
          message: '调用函数不能为空',
          type: 'warning'
        });
        return
      }
      // localStorage.setItem(this.currentAkId + '_call', this.pythonCode)
      addCallFunction(this.currentAkId, this.pythonCode).then(res => {
        if (res.success) {
          this.$message({
            message: '保存成功',
            type: 'success'
          });
          this.load()
        }
        else {
          this.$message({
            message: 'API key调用函数编译失败，请检查语法错误',
            type: 'warning'
          });
        }
      })
      this.resetCodeEditor()
    },
    handleTest(row) {
      if (!row.callFunction) {
        this.$message({
          message: '还没有编辑API key调用函数',
          type: 'warning'
        });
        return
      }
      this.$message({
          message: '正在测试，请稍等',
          type: 'info'
        });
      this.connectivityTesting = true
      testConnectivity(row.value, row.callFunction).then(res => {
        if (res.success) {
          if (res.result) {
            this.$message({
              message: '连通性良好',
              type: 'success'
            });
            const specifiedDate = new Date();
            localStorage.setItem(row.id+'_testConnectivity_normal',specifiedDate.toLocaleString())
          }
          else {
            this.$message({
              message: '连通性有问题，请检查网络或API key',
              type: 'warning'
            });
            const specifiedDate = new Date();
            localStorage.setItem(row.id+'_testConnectivity_error',specifiedDate.toLocaleString())
          }
          this.connectivityTesting = false
        }
        this.connectivityTesting = false
        this.load()
      })
    },
    isValidValue(inputString) {
      // 使用正则表达式匹配以非空内容开始，中间一个点，后面也是非空内容结束的字符串
      const formatPattern = /^[^.]+\.[^.]+$/;
      return formatPattern.test(inputString);
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
}

.main {
  padding: 20px;
}
.testResult{
  margin-right: 10px;
}
</style>