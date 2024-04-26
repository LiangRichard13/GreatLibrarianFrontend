<template>
  <div class="main">
    <el-page-header @back="goBack" content="测试列表">
    </el-page-header>
    <div class="content">
      <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
        {{ this.thisExperiment.name }}的存疑记录
      </h3>
    </div>
    <template v-if="QAList && QAList.length">
      <div class="table-container">
        <el-table :data="pagedQAList" style="width: 100%" v-loading="loading">
          <!-- <el-table-column label="QA ID" prop="QAid"></el-table-column> -->
          <el-table-column label="问题">
            <template slot-scope="scope">
              <div style="height: 50px; overflow: auto;">{{ scope.row.Q }}</div>
            </template>
          </el-table-column>
          <el-table-column label="打分" prop="score" width="400%">
            <template slot-scope="scope">
              <!-- <el-rate v-model="scope.row.score" :colors="colors"></el-rate> -->
              <!-- <el-slider v-model="scope.row.score" max=1 step=0.01 input-size="mini" show-input></el-slider> -->
              <el-slider v-model="scope.row.score" input-size="mini" show-input></el-slider>
            </template>
          </el-table-column>

          <el-table-column>
            <template slot-scope="scope">
              <div>
                  <el-button plain icon="el-icon-finished" slot="reference" size="small" type="primary" @click="submitRate(scope.row, scope.$index)">提交打分</el-button>
              </div>
            </template>
          </el-table-column>


          <el-table-column type="expand" label="回答">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="回答:">
                  <span>{{ props.row.A }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pagination-container" style="margin-top: 20px;">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
          :current-page="currentPage" :page-sizes="[5, 10, 20, 30, 50]" :page-size="pageSize" :total="QAList.length"
          layout="total, sizes, prev, pager, next, jumper">
        </el-pagination>
      </div>
    </template>
    <!-- <div class="button-container" style="text-align: right; margin-top: 20px;">
      <el-button plain type="primary" @click="submitRate()">提交打分</el-button>
    </div> -->
    <div v-else class="emptyQAList">
      <el-empty description="暂无审核任务"></el-empty>
    </div>
  </div>
</template>

<script>
import { getQAByExpirenceId, rateQA } from '@/api/qa'
import { updateReport } from '@/api/expOperation'
export default {
  inject: ['isUpdate'],
  name: "ReviewQA",
  data() {
    return {
      loading: true,
      showDialog: false,
      QAList: [],
      thisExperiment: {},
      selectedIds: [],
      currentPage: 1,
      pageSize: 10,
      pagedQAList: [], // 用于显示当前页的数据
      // colors: ['#99A9BF', '#F7BA2A', '#FF9900']
    }
  },
  mounted() {
    let storedExperiment = localStorage.getItem('thisExperiment');
    if (storedExperiment) {
      this.thisExperiment = JSON.parse(storedExperiment);
    }
    else {
      // 处理没有数据的情况，可能是跳转到此页面或刷新页面
      this.$router.push("/projectsList")
    }
    this.load()
    setTimeout(() => {
      this.loading = false
    }, 300);
  },
  methods: {
    load() {
      getQAByExpirenceId(this.thisExperiment.id, localStorage.getItem('uid')).then(res => {
        this.QAList = res.data
        this.QAList = this.QAList.map(QA => {
          return {
            ...QA, // 复制原有的对象
            score: 0 // 添加新的字段score，并设其值为0
          };
        });
        // console.log('该测试下的QA', this.QAList)
        this.updatePagedQAList(); // 初始加载
      })
    },
    goBack() {
      this.$router.go(-1); // 返回上一个页面
    },
    submitRate(row, index) {
      if(row.score===0)
      {
        this.$message({
          message: '不能打0分,请打分再提交',
            type: 'warning'
        });
        return
      }
      const score=(row.score / 100).toFixed(2)
      console.log('打分',score)
      rateQA(row.QAid,score).then(res => {
        if (res.success) {
          this.QAList.splice(index, 1)
          this.$message({
            message: '打分成功',
            type: 'success'
          });
          setTimeout(() => {
            this.QAList.splice(index, 1)
            this.load()
          }, 500);
          if (res.lastOne) {
            this.$message({
              message: '已完成该测试所有存疑记录的审核',
              type: 'success',
              offset:100
            });
            this.isUpdate=true
            updateReport(this.thisExperiment.id).then(res => {
              if (res.success) {
                this.$message({
                  type: 'success',
                  message: this.thisExperiment.id + '-' + this.thisExperiment.name + '测试报告更新成功'
                });
              }
              this.isUpdate=false
            })
          }
          // this.load()
        }
      })
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
    // formatTooltip(val) {
    //     return val / 100;
    //   },
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