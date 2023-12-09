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
              <el-form-item label="数据集文件URL:">
                <span>{{ props.row.fileURL }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
            label="数据集 ID"
            prop="id">
        </el-table-column>
        <el-table-column
            label="测试对象"
            prop="name">
        </el-table-column>
        <el-table-column
            label="详细描述"
            prop="info">
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
          <el-form-item label="测试对象">
            <el-input v-model="newDataItem.name"></el-input>
          </el-form-item>

          <el-form-item label="详细描述">
            <el-input v-model="newDataItem.info"></el-input>
          </el-form-item>

          <!-- Upload button added here -->
          <el-form-item label="上传文件">
            <el-upload
                class="upload-demo"
                accept="application/zip"
                :action="uploadAction"
                :on-success="handleUploadSuccess"
                multiple
                :limit="1">
              <el-button size="small" type="primary">
                <i class="el-icon-upload2"></i> 点击上传
              </el-button>
              <div class="el-upload__tip">只能上传zip文件</div>
            </el-upload>
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
import config from "@/services/conf";

export default {
  name: "DataSetConfig",
  data() {
    return {
      uploadAction: config.API_URL + '/upload',
      dataSet: [{id: '1', name: '文心一言', info: '123', fileURL: 'http://localhost:8080/dataSetFile/1'}, {
        id: '1',
        name: 'chatGpt',
        info: '123',
        fileURL: 'http://localhost:8080/dataSetFile/2'
      }],
      showDialog: false,
      newDataItem: {name: '', info: '', fileUrl: ''}
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
            findByUserId(id).then(res => {
              this.dataSet = res.data;
            })
          }
        },
        addDataSet() {
          if (this.newDataItem.info.trim() && this.newDataItem.name.trim()) {
            if (this.newDataItem.fileUrl !== '') {
              const data = {
                uid:localStorage.getItem('uid'),
                name: this.newDataItem.name,
                info: this.newDataItem.info,
                fileUrl: this.newDataItem.fileUrl
              }
              addDateSet(data).then(res => {
                if (res.success) {
                  this.newDataItem.name = '';
                  this.newDataItem.info = ''; // 清空输入框
                  this.newDataItem.fileUrl = '';
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
                message: '请上传数据集文件',
                type: 'warning'
              });
            }
          } else {
            this.$message({
              message: '数据集各字段不能为空',
              type: 'warning'
            });
          }
        },
        removeDataSet(index, row) {
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
        resetDialog() {
          this.newDataItem.name = '';
          this.newDataItem.value = '';// 重置输入
          this.newDataItem.fileUrl = '';
        },
        handleUploadSuccess(res) {
          if (res.success) {
            this.$message({
              message: '上传成功！',
              type: 'success',
            });
            this.newDataItem.fileUrl = res;
          }
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