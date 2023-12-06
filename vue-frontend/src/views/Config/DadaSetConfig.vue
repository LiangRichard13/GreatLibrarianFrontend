<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">数据集配置</h3>

    <div style="display: flex; justify-content: flex-end; padding-bottom: 20px;">
      <el-button
          icon="el-icon-circle-plus"
          type="success"
          @click="showDialog=true">添加数据集数据
      </el-button>
    </div>

    <div class="table-container">
      <el-table :data="dataSet" style="width: 100%">
        <el-table-column type="expand">
      <template slot-scope="props">
        <el-form label-position="left" inline class="demo-table-expand">
          <el-form-item label="详细描述">
            <span>{{ props.row.info}}</span>
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
    <el-table-column
      label="数据集 ID"
      prop="id">
    </el-table-column>
    <el-table-column
      label="接口"
      prop="name">
    </el-table-column>

        <!-- 操作列 -->
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-popconfirm
                confirm-button-text="确定"
                cancel-button-text="不用了"
                icon="el-icon-info"
                icon-color="red"
                @confirm="removeDataSet(scope.$index, scope.row)"
                title="确定要删除此API_KEY吗？"
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
        title="添加 数据集"
        :visible.sync="showDialog"
        width="30%"
        @close="resetDialog">
      <div>
        <el-form ref="form" :model="newDataItem" label-width="100px">
          <el-form-item label="接口来源">
            <el-input v-model="newDataItem.name"></el-input>
          </el-form-item>

          <el-form-item label="数据集内容">
            <el-input v-model="newDataItem.value"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="addDataSet">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>


<script>
import {addDateSet, deleteById, findByUserId} from "@/api/dataSetConfig";

export default {
  name: "DataSetConfig",
  data() {
    return {
      dataSet: [{id: '1', name: '文心一言', info: '123'}, {id: '1', name: 'chatGpt', info: '123'}],
      showDialog: false,
      newDataItem: {name: '', info: ''}
    }
  },
  mounted() {
    this.load()
  },
  methods:
      {
        load() {
          if (localStorage.getItem("uid") !== null) {
            const id = parseInt(localStorage.getItem("uid"))
            findByUserId(id).then(res => {
              this.dataSet = res.data;
            })
          }
        },
        addDataSet() {
          if (this.newDataItem.info.trim() && this.newDataItem.name.trim()) {
            const data = {
              name: this.newDataItem.name,
              info: this.newDataItem.info
            }
            addDateSet(data).then(res => {
              if (res.success) {
                this.newDataItem.name = '';
                this.newDataItem.info = ''; // 清空输入框
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
              message: 'API_KEY不能为空',
              type: 'warning'
            });
          }
        },
        removeDataSet(index, row) {
          const deleteId=row.id
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
        resetDialog() {
          this.newDataItem.name = '';
          this.newDataItem.value = '';// 重置输入
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
  border: 1px solid #ebeef5; /* 根据你的截图，看起来你需要一个边框 */
}

.main {
  padding: 20px;
}
</style>