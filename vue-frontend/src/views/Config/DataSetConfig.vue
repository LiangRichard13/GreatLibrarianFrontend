<template>
  <div class="main">

    <!-- <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 0px;text-align: center">数据集配置</h3>

    <div style="display: flex; justify-content: flex-end; padding-bottom: 20px;">
      <el-button plain icon="el-icon-circle-plus" type="success" @click="showDialog = true">添加数据集
      </el-button>
    </div> -->

    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px;">
    <div style="flex: 1; display: flex; justify-content: center;">
        <h3 style="letter-spacing: 1px; font-weight: 400; margin: 0;">数据集配置</h3>
    </div>
    <el-button plain icon="el-icon-circle-plus" type="success" @click="showDialog = true">添加数据集</el-button>
</div>

    <div class="table-container">
      <el-table :data="dataSet" style="width: 100%">
        <!-- <el-table-column label="数据集 ID" prop="id">
        </el-table-column> -->
        <el-table-column label="测试对象" prop="name" width="300%">
        </el-table-column>
        <el-table-column label="上传文件名称" prop="url" width="300%">
        </el-table-column>
        <el-table-column label="详细描述" prop="info">
          <template slot-scope="scope">
            <div style="height: 70px; overflow: auto;">{{ scope.row.info }}</div>
          </template>
        </el-table-column>

        <!-- 操作列 -->
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info" icon-color="red"
              @confirm="removeDataSet(scope.$index, scope.row)" title="确定要删除此数据集吗？">
              <el-button plain style="margin-left: 8px" size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
              </el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加API_KEY的对话框 -->
    <el-dialog title="添加 数据集" :visible.sync="showDialog" width="30%" @close="resetDialog">

      <div>
        <el-form ref="form" :model="newDataItem" label-width="100px">
          <el-form-item label="测试对象">
            <el-input v-model="newDataItem.name"></el-input>
          </el-form-item>

          <el-form-item label="详细描述">
            <el-input v-model="newDataItem.info"></el-input>
          </el-form-item>

          <!-- Upload button added here -->
          <template>
            <el-form-item label="上传文件">
              <el-upload class="upload-demo" accept="application/zip" :before-upload="beforeUpload" multiple :limit="1">
                <div style="display: flex; align-items: center;">
                <el-button plain size="small" type="primary">
                  <i class="el-icon-upload2"></i> 点击上传
                </el-button>
                <div slot="tip" class="el-upload__tip" style="margin-left: 20px;">只能上传zip文件</div>
                </div>
              </el-upload>
              <span class="el-upload__tip" v-if="isUpload == true" style="color: black; margin-right: 10px;">
                文件已上传
                <el-icon name="check" style="color: green;"></el-icon>
              </span>
            </el-form-item>
          </template>
        </el-form>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button plain @click="showDialog = false">取 消</el-button>
        <el-button plain type="primary" @click="handleAddDataSet">确 定</el-button>
      </span>
    </el-dialog>


  </div>
</template>


<script>
import { addDateSet, deleteById, findDataSetByUserId } from "@/api/dataSetConfig";

export default {
  name: "DataSetConfig",
  data() {
    return {
      dataSet: [],
      showDialog: false,
      newDataItem: { name: '', info: '' },
      uploadFile: null,
      isUpload: false
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
        findDataSetByUserId(id).then(res => {
          this.dataSet = res.data;
          this.dataSet.forEach(item=>{
            // item.url=item.url.replace(/App/g, '')
            // item.url=item.url.replace(/data/g, '')
            // item.url=item.url.replace(/DataSet/g, '')
            // item.url=item.url.replace(/\\/g, '')
            item.url=item.url.replace(/^App\\data\\DataSet\\/, '');

          })
        })
      }
    },
    handleAddDataSet() {
      if (!this.newDataItem.name.trim() || !this.newDataItem.info.trim()) {
        this.$message({
          message: '数据集的名称和描述不能为空',
          type: 'warning'
        });
        return;
      }

      if (!this.uploadedFile) {
        this.$message({
          message: '请上传数据集文件',
          type: 'warning'
        });
        return;
      }

      // 创建 FormData 并添加数据
      const formData = new FormData();
      formData.append('uid', localStorage.getItem('uid'));
      formData.append('name', this.newDataItem.name);
      formData.append('info', this.newDataItem.info);
      formData.append('dataSetFile', this.uploadedFile);

      // 手动上传文件
      this.uploadFileAndInfo(formData);
    },
    uploadFileAndInfo(formData) {
      addDateSet(formData).then(res => {
        if (res.success) {
          this.$message({
            message: '添加成功！',
            type: 'success'
          });
          this.resetDialog
          this.showDialog = false
          this.load()
        }
      })
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
      this.newDataItem.info = '';// 重置输入
      this.uploadFile = null
      this.isUpload = false
    },
    beforeUpload(file) {
      // 检查文件类型等逻辑...
      this.uploadedFile = file; // 保存文件引用，但不上传
      this.isUpload = true
      this.$message({
        message: '文件添加成功',
        type: 'success'
      });
      return false; // 阻止自动上传
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
  /* 根据你的截图，看起来你需要一个边框 */
}

.main {
  padding: 20px;
}
</style>