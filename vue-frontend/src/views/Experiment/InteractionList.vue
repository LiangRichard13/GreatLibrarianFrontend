<template>
  <div class="main">
    <el-page-header @back="goBack" content="测试列表">
    </el-page-header>
    <div class="content">
      <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
        {{ this.thisExperiment.name }}的交互记录
      </h3>
    </div>
    <template v-if="interactionList && interactionList.length">
      <div class="table-container">
        <el-table :data="pageList" style="width: 100%" v-loading="loading" stripe>
          <!-- <el-table-column label="QA ID" prop="QAid"></el-table-column> -->
          <el-table-column label="打分" type="expand" width="150px">
            <template slot-scope="scope">
              <div>
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="规则化打分:">
                    <span>{{ scope.row.method_scored }}</span>
                  </el-form-item>
                  <el-form-item label="大模型打分:">
                    <span>{{ scope.row.llm_score }}</span>
                  </el-form-item>
                  <el-form-item label="最终打分:">
                    <span>{{ scope.row.fin_score }}</span>
                  </el-form-item>
                </el-form>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="问题">
            <template slot-scope="scope">
              <div style="height: 50px; overflow: auto;">{{ scope.row.Q }}</div>
            </template>
          </el-table-column>
          <el-table-column label="问题">
            <template slot-scope="scope">
              <div style="height: 50px; overflow: auto;">{{ scope.row.A }}</div>
            </template>
          </el-table-column>
          <el-table-column label="关键字" prop="keyword">
          </el-table-column>
          <!-- <el-table-column label="规则化打分" prop="method_scored">
            </el-table-column>
            <el-table-column label="大模型打分" prop="llm_score">
            </el-table-column>
            <el-table-column label="最终打分" prop="fin_score">
            </el-table-column> -->
        </el-table>
      </div>
      <div class="pagination-container" style="margin-top: 20px;">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          :page-sizes="[5, 10, 20, 30, 50]" :page-size="pageSize" :total="interactionList.length"
          layout="total, sizes, prev, pager, next, jumper">
        </el-pagination>
      </div>
    </template>
    <!-- <div class="button-container" style="text-align: right; margin-top: 20px;">
        <el-button plain type="primary" @click="submitRate()">提交打分</el-button>
      </div> -->
    <div v-else>
      <el-empty description="暂无交互记录"></el-empty>
    </div>
  </div>
</template>

<script>
import { getInteraction } from "@/api/expOperation"

export default {
  name: "interactionList",
  data() {
    return {
      thisExperiment: {},
      interactionList: [
        {
          "Q": "什么是机器学习？",
          "A": "机器学习是一种使计算机能够在没有明确编程的情况下学习的科学。",
          "keyword": "机器学习, 计算机, 编程",
          "method_scored": 85,
          "llm_score": 90,
          "fin_score": 88
        },
        {
          "Q": "全球变暖的主要原因是什么？",
          "A": "全球变暖的主要原因是大量温室气体，如二氧化碳，由于人类活动而排放到大气中。",
          "keyword": "全球变暖, 温室气体, 二氧化碳",
          "method_scored": 78,
          "llm_score": 81,
          "fin_score": 80
        },
        {
          "Q": "如何制作披萨？",
          "A": "制作披萨首先需要准备面团和配料，如奶酪、番茄酱和你喜欢的其他配料，然后在烤箱中烘烤。",
          "keyword": "披萨, 面团, 奶酪",
          "method_scored": 90,
          "llm_score": 88,
          "fin_score": 89
        }
      ],
      currentPage: 1,
      pageSize: 10,
      pageList: [], // 用于显示当前页的数据
      loading: false
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
    // this.load()
    this.updatePageList()
    setTimeout(() => {
      this.loading = false
    }, 300);
    console.log("交互记录", this.interactionList)
  },
  methods: {
    load() {
      getInteraction(this.thisExperiment.id).then(res => {
        if (res.success)
          this.interactionList = res.data
      })
    },
    goBack() {
      this.$router.go(-1); // 返回上一个页面
    },
    // 用于处理每页显示条目数变化
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.updatePageList();
    },
    // 用于处理当前页变化
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.updatePageList();
    },
    // 更新当前页的 QA 列表
    updatePageList() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      this.pageList = this.interactionList.slice(startIndex, endIndex);
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

.demo-table-expand {
    font-size: 0;
  }
  
.demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
.demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>