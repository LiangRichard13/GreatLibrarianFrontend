<template>
  <div class="main">

    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px;">
    <div style="flex: 1; display: flex; justify-content: center;">
        <h3 style="letter-spacing: 1px; font-weight: 400; margin: 0;">API_KEY配置</h3>
    </div>
    <el-button plain icon="el-icon-circle-plus" type="success" @click="showDialog = true">添加API_KEY</el-button>
</div>




    <div class="table-container">
      <el-table :data="apiKeys" style="width: 100%">
        <!-- <el-table-column prop="id" label="API_KEY ID" width="300%"></el-table-column> -->
        <el-table-column prop="name" label="大模型名称" width="300%"></el-table-column>
        <el-table-column prop="value" label="密钥"></el-table-column>
        <el-table-column  label="详细描述" width="500%">
          <template slot-scope="scope">
            <div style="height: 70px; overflow: auto;">{{ scope.row.intro }}</div>
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
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info" icon-color="red"
              @confirm="removeKey(scope.$index, scope.row)" title="确定要删除此API_KEY吗?">
              <el-button plain style="margin-left: 8px" size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
              </el-button>
            </el-popconfirm>
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
        </el-form>


      </div>
      <span slot="footer" class="dialog-footer">
        <el-button plain @click="showDialog = false">取 消</el-button>
        <el-button plain type="primary" @click="addKey">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>


<script>
import { addApiKey, deleteById, findApiKeyByUserId } from "@/api/apiConfig";

export default {
  name: "ApiConfig",
  data() {
    return {
      apiKeys: [],
      showDialog: false,
      newApiKey: { name: '', value: '', intro: '' }
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
          console.log('该用户的apikey',this.apiKeys)
        })
      }
    },
    addKey() {
      if (this.newApiKey.value.trim() && this.newApiKey.name.trim()) {
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
      } else {
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
</style>