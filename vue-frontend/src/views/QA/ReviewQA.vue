<template>
  <div class="main">
    <el-page-header @back="goBack" content="测试列表">
    </el-page-header>
    <div class="content">
      <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
       {{ this.thisExperiment.name }}的存疑记录
      </h3>
    </div>
    <template v-if="QAList.length">
      <div class="table-container">
        <el-table :data="pagedQAList" style="width: 100%">
          <!-- <el-table-column label="QA ID" prop="QAid"></el-table-column> -->
          <el-table-column label="问题" prop="Q"></el-table-column>
          <el-table-column label="打分" prop="score">
            <template slot-scope="scope">
              <el-rate v-model="scope.row.score"></el-rate>
            </template>
          </el-table-column>

          <el-table-column>
            <template slot-scope="scope">
              <div>
                <!-- 使用 el-popconfirm 包裹您的按钮 -->
                <el-popconfirm title="确定要提交打分吗？" @confirm="submitRate(scope.row, scope.$index)">
                  <!-- slot 中是触发弹出的元素 -->
                  <el-button plain icon="el-icon-finished" slot="reference" size="small" type="primary">提交打分</el-button>
                </el-popconfirm>
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
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          :page-sizes="[10, 20, 30, 50]" :page-size="pageSize" :total="QAList.length"
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
export default {
  name: "ReviewQA",
  data() {
    return {
      showDialog: false,
      QAList: [
        // { QAid: '1', Q: '世界上最高的峰是哪个峰 ?', A: '世界上最高的山峰是珠穆朗玛峰（Mount Everest），它位于喜马拉雅山脉，跨越尼泊尔和中国（西藏）的边界。珠穆朗玛峰的海拔高度是8,848.86米（29,031.7英尺），这使它成为地球上海拔最高的山峰。这座山峰也是登山者们梦寐以求的挑战之一，但攀登它极具挑战性，需要极高的技术和体能。每年都有登山者前往珠穆朗玛峰尝试征服它，但也伴随着危险和挑战。' },
        // { QAid: '2', Q: '世界上最深的湖是哪个?', A: '世界上最深的湖是贝加尔湖，位于俄罗斯。' },
        // { QAid: '3', Q: '世界上最长的山脉是什么?', A: '世界上最长的山脉是安第斯山脉，延伸南美西部海岸线。' },
        // { QAid: '4', Q: '世界上最大的热带雨林是哪里?', A: '世界上最大的热带雨林是亚马孙雨林，覆盖多个南美国家。' },
        // { QAid: '5', Q: '世界上最大的岛屿是哪个?', A: '世界上最大的岛屿是格陵兰岛，属于丹麦。' }
      ],
      thisExperiment: {},
      selectedIds: [],
      currentPage: 1,
      pageSize: 10,
      pagedQAList: [] // 用于显示当前页的数据
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
        console.log('该测试下的QA',this.QAList)
        this.updatePagedQAList(); // 初始加载
      })
    },
    goBack() {
      this.$router.go(-1); // 返回上一个页面
    },
    submitRate(row, index) {
      rateQA(row.QAid, row.score).then(res => {
        if (res.success) {
          this.$message({
            message: '打分成功!',
            type: 'success'
          });
          this.QAList.splice(index, 1)
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