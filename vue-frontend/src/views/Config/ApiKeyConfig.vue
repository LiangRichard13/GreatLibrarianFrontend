<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">API_KEY配置</h3>

    <div style="display: flex; justify-content: flex-end; padding-bottom: 20px;">
      <el-button
          icon="el-icon-circle-plus"
          type="success"
          @click="showDialog=true">添加API_KEY
      </el-button>
    </div>

    <div class="table-container">
      <el-table :data="apiKeys" style="width: 100%">
        <el-table-column prop="id" label="API_KEY ID"></el-table-column>
        <el-table-column prop="name" label="接口"></el-table-column>
        <el-table-column prop="value" label="内容"></el-table-column>
        <el-table-column prop="auth" label="认证token"></el-table-column>


        <!-- 操作列 -->
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-popconfirm
                confirm-button-text="确定"
                cancel-button-text="不用了"
                icon="el-icon-info"
                icon-color="red"
                @confirm="removeKey(scope.$index, scope.row)"
                title="确定要删除此API_KEY吗?"
            >
              <el-button
                  style="margin-left: 8px"
                  size="mini"
                  icon="el-icon-delete"
                  type="danger"
                  slot="reference">删除
              </el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加API_KEY的对话框 -->
    <el-dialog
        title="添加 API Key"
        :visible.sync="showDialog"
        width="30%"
        @close="resetDialog">
      <div>
        <el-form ref="form" :model="newApiKey" label-width="100px">

          <el-form-item label="接口来源">
            <el-input v-model="newApiKey.name"></el-input>
          </el-form-item>

          <el-form-item label="KEY内容">
            <el-input v-model="newApiKey.value"></el-input>
          </el-form-item>

            <el-form-item label="认证token">
            <el-input v-model="newApiKey.auth"></el-input>
          </el-form-item>
        </el-form>


      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="addKey">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>


<script>
import {addApiKey, deleteById, findApiKeyByUserId} from "@/api/apiConfig";

export default {
  name: "ApiConfig",
  data() {
    return {
      apiKeys: [],
      showDialog: false,
      newApiKey: {name: '', value: '',auth:''}
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
            })
          }
        },
        addKey() {
          if (this.newApiKey.value.trim() && this.newApiKey.name.trim()&&this.newApiKey.auth) {
            const data = {
              uid:localStorage.getItem('uid'),
              name: this.newApiKey.name,
              value: this.newApiKey.value,
              auth:this.newApiKey.auth
            }
            addApiKey(data).then(res => {
              if (res.success) {
                this.newApiKey.name = '';
                this.newApiKey.value = ''; // 清空输入框
                this.newApiKey.auth='';
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
          const deleteId={id:row.id}
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
          this.newApiKey.auth='';
        },
      }
}


</script>

<style scoped>
.table-container {
  max-width: 2000px; /* 设置你希望的最大宽度 */
  margin: auto; /* 这将使得表格居中 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 可选：添加阴影效果 */
  padding: 20px; /* 可选：添加一些内边距 */
  border: 1px solid #ebeef5;
}

.main {
  padding: 20px;
}
</style>