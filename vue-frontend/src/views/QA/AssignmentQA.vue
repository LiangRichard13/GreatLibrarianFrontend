<template>
  <div class="main">
    <el-page-header @back="goBack" content="测试列表">
    </el-page-header>
    <div class="content">
      <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
        {{ this.thisExperiment.id }}-{{ this.thisExperiment.name }} 测试的QA记录
      </h3>
    </div>
    <template v-if="QAList.length">
      <div class="table-container">
        <el-table :data="pagedQAList" :row-key="row => row.QAid" style="width: 100%" ref="multipleTable"
          tooltip-effect="dark" @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <!-- <el-table-column label="QA ID" prop="QAid"></el-table-column> -->
          <el-table-column label="问题" prop="Q"></el-table-column>
          <!-- <el-table-column label="回答" prop="A"></el-table-column> -->

          <el-table-column type="expand" lable="回答">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="回答:">
                  <span>{{ props.row.A }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-container" style="margin-top: 20px;">
          <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
            :current-page="currentPage" :page-sizes="[10, 20, 30, 50]" :page-size="pageSize" :total="QAList.length"
            layout="total, sizes, prev, pager, next, jumper">
          </el-pagination>
        </div>
        <div style="margin-top: 20px">
          <el-button @click="toggleSelection()">取消选择</el-button>
        </div>
      </div>
      <div class="button-container" style="text-align: right; margin-top: 20px;">
        <el-button type="primary" @click="showDialog = true">分发给协作者</el-button>
      </div>

      <!-- 分发协作者对话框 -->
      <el-dialog title="选择分发协作者" :visible.sync="showDialog" width="30%" @close="resetDialog">
        <div>
          <el-form ref="form" label-width="100px">
            <el-form-item label="选择协作者">
              <el-select v-model="distributeUserId" placeholder="请选择">
                <el-option v-for="item in this.thisCollaborators" :key="item.id" :label="`${item.id} - ${item.name}`"
                  :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <span slot="footer" class="dialog-footer">
          <el-button @click="showDialog = false">取 消</el-button>
          <el-button type="primary" @click="distributeToCollaborators">确 定</el-button>
        </span>
      </el-dialog>
    </template>
    <div v-else class="emptyQAList">
      <el-empty description="暂无审核任务"></el-empty>
    </div>
  </div>
</template>

<script>
import { getQAByExpirenceId, distributeToOthers } from '@/api/qa'
// import { getCollaboratorsByProjectId, getProjectByExpirementId } from "@/api/project"
import { getFriendsByExperimentId } from "@/api/collaborate"
export default {
  name: "AssignmentQA",
  data() {
    return {
      showDialog: false,
      QAList: [],
      thisExperiment: {},
      thisCollaborators: [],
      selectedIds: [],
      distributeUserId: null,
      currentPage: 1,
      pageSize: 10,
      pagedQAList: [], // 用于显示当前页的数据
    }
  },
  mounted() {

    let storedExperiment = localStorage.getItem('thisExperiment');
    if (storedExperiment!==null) {
      this.thisExperiment = JSON.parse(storedExperiment);
      console.log('进行分发的测试:',this,this.thisExperiment)
    }
    else {
      // 处理没有数据的情况，可能是跳转到此页面或刷新页面
      this.$router.push("/projectsList")
    }
    this.load();
    // this.thisExperiment = this.$route.query;

  },
  methods: {
    load() {
      getQAByExpirenceId(this.thisExperiment.id, localStorage.getItem('uid')).then(res => {
        this.QAList = res.data
        this.updatePagedQAList(); // 初始加载
      })

      //用于获取当前测试的项目
      // getProjectByExpirementId(this.thisExperiment.id).then(res => {
      //   this.thisProjejctId = res.data
      // })

      // 获取当前项目的协作者以便分发
      getFriendsByExperimentId(this.thisExperiment.id).then(res => {
        this.thisCollaborators = res.data
        console.log('当前测试的协作者',this.thisCollaborators)
      })
    },
    goBack() {
      this.$router.go(-1); // 返回上一个页面
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(selectedRows) {
      this.$nextTick(() => {
        this.selectedIds = selectedRows.map(row => row.QAid);
        console.log(this.selectedIds); // 现在应该显示正确的数据
      });
    },
    distributeToCollaborators() {
      if (this.distributeUserId === null) {
        this.$message({
          message: '请选择分发的对象！',
          type: 'warning'
        });
      }
      else {
        if (this.selectedIds.length === 0) {
          this.$message({
            message: '还未选择审核记录！',
            type: 'warning'
          });
        }
        else {
          // 初始化成功和失败的计数器
          let successCount = 0;
          let failCount = 0;

          // 将所有的分发请求的Promise收集到一个数组中
          const distributePromises = this.selectedIds.map(id => {
            const data = {
              uid: this.distributeUserId,
              QAid: id
            };

            // 返回每个分发请求的Promise
            return distributeToOthers(data).then(res => {
              if (res.success) {
                // 如果请求成功，增加成功计数器
                successCount++;
              } else {
                // 如果请求失败，增加失败计数器
                failCount++;
              }
            }).catch(() => {
              // 处理请求失败的情况（例如网络错误等）
              failCount++;
            });
          });

          // 使用Promise.all等待所有分发请求完成
          Promise.all(distributePromises).then(() => {
            // 所有请求处理完毕后，根据成功和失败的计数器显示消息
            if (successCount > 0) {
              this.$message({
                message: `分发成功${successCount}条！`,
                type: 'success'
              });
            }

            // 如果有失败的，显示失败的条数
            if (failCount > 0) {
              this.$message({
                message: `分发失败${failCount}条`,
                type: 'error'
              });
            }

            // 重新加载数据等后续操作
            this.load();
            this.resetDialog();
            this.showDialog=false;
          }).catch(error => {
            // 处理可能的错误（例如，某个Promise抛出的异常）
            console.error('分发过程中出现错误：', error);
          });
        }
      }
    },
    resetDialog() {
      this.distributeUserId = null
    },
    // 用于处理每页显示条目数变化
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.updatePagedQAList();
    },
    // 用于处理当前页变化
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.updatePagedQAList();
    },
    // 更新当前页的 QA 列表
    updatePagedQAList() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      this.pagedQAList = this.QAList.slice(startIndex, endIndex);
    },
  },
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

.back-button {
  position: absolute;
  top: 10px;
  left: 10px;
}

.button-container {
  /* This would right-align your button */
  text-align: right;
  /* Add other styles if needed */
}
</style>