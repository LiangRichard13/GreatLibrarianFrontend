<template>
    <div class="main">

        <el-page-header @back="goBack" content="我的协作项目">
        </el-page-header>
        <div class="content">
            <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
                {{ this.thisProject.id }}-{{ this.thisProject.name }}项目的实验列表
            </h3>
            <div class="section">
                <h4>待审核</h4>
                <el-table :data="reviewList" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="时间" prop="time"></el-table-column>
                    <el-table-column label="用例数" prop="caseNum"></el-table-column>
                    <el-table-column label="大模型" prop="LLMName"></el-table-column>
                    <el-table-column label="进度" prop="progress">
                        <template slot-scope="scope">
                            <el-progress :percentage="scope.row.progress"></el-progress>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="180" align="center">
                        <template slot-scope="scope">
                            <el-button size="mini" type="warning"
                                @click.stop="handleReviewExpirement(scope.row)">
                                开始审核
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>
  
  
<script>
// import { getExperimentByProjectId } from '@/api/experiment'


export default {
    name: "ExperimentList",
    data() {
        return {
            showDialog: false,
            experimentList:
                [
                    {
                        "id": 1,
                        "name": "实验一",
                        "time": "2023-01-01",
                        "caseNum": 10,
                        "LLMName": "模型A",
                        "status": "待实验",
                        "progress": 0
                    },
                    {
                        "id": 2,
                        "name": "实验二",
                        "time": "2023-01-02",
                        "caseNum": 20,
                        "LLMName": "模型B",
                        "status": "待审核",
                        "progress": 100
                    },
                    {
                        "id": 3,
                        "name": "实验三",
                        "time": "2023-01-03",
                        "caseNum": 15,
                        "LLMName": "模型C",
                        "status": "已完成",
                        "progress": 100
                    },
                    {
                        "id": 4,
                        "name": "实验四",
                        "time": "2023-01-04",
                        "caseNum": 25,
                        "LLMName": "模型D",
                        "status": "待实验",
                        "progress": 0
                    },
                    {
                        "id": 5,
                        "name": "实验五",
                        "time": "2023-01-05",
                        "caseNum": 30,
                        "LLMName": "模型E",
                        "status": "待审核",
                        "progress": 100
                    },
                    {
                        "id": 6,
                        "name": "实验六",
                        "time": "2023-01-06",
                        "caseNum": 12,
                        "LLMName": "模型F",
                        "status": "已完成",
                        "progress": 100
                    }
                ],
            reviewList: [], // 待审核列表数据
            thisProject: {}
        }
    },
    mounted() {
        this.thisProject = this.$route.query
        this.load()
    },
    methods:
    {
        load() {
            // const id = this.thisProject.id
            // getExperimentByProjectId(id).then(res => {
            //     this.experimentList = res.data;
            // })
            this.experimentList.forEach(exp => {
                switch (exp.status) {
                    case '待审核':
                        this.reviewList.push(exp);
                        break;
                }
            });
        },
        handleReviewExpirement(experiment) {
            this.$router.push({ path: `/review`,query:experiment});
        },
        goBack() {
            this.$router.go(-1); // 返回上一个页面
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

.main .section {
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    /* 阴影线条 */
}

.main .section h4 {
    margin-bottom: 10px;
}

.back-button {
    position: absolute;
    top: 10px;
    left: 10px;
}
</style>