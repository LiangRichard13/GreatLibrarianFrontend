<template>
    <div class="main">
        <!-- <el-page-header @back="goBack" content="我的协作项目">
        </el-page-header> -->
        <div class="content">
            <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
                我参与协作的实验
            </h3>
            <div class="section">
                <h4>待审核</h4>
                <el-table :data="reviewList" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="时间" prop="time">
                        <template slot-scope="scope">
                            <!-- 格式化时间 -->
                            <div>{{ formatDate(scope.row.time) }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="180" align="center">
                        <template slot-scope="scope">
                            <el-button size="mini" type="warning" @click.stop="handleReviewExpirement(scope.row)">
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
import {getExperimentsByUserId} from "@/api/collaborate"


export default {
    name: "ExperimentList",
    data() {
        return {
            showDialog: false,
            experimentList: [],
            reviewList: [], // 待审核列表数据
            // thisProject: {}
        }
    },
    mounted() {
        // let storedProject = localStorage.getItem('thisCoProject');
        // if (storedProject) {
        //     this.thisProject = JSON.parse(storedProject);
        // } else {
        //     this.$router.push("/myCollaborate")
        // }
        this.load();
    },
    methods:
    {
        load() {
            if (localStorage.getItem("uid") !== null) {
                const id = localStorage.getItem("uid")
                getExperimentsByUserId(id).then(res => {
                    this.experimentList = res.data;
                })
            }
            this.experimentList.forEach(exp => {
                switch (exp.status) {
                    case '待审核':
                        this.reviewList.push(exp);
                        break;
                }
            });
        },
        handleReviewExpirement(experiment) {
            // this.$router.push({ path: `/review`, query: experiment });
            localStorage.setItem('thisExperiment', JSON.stringify(experiment));
            this.$router.push("/review")
        },
        // goBack() {
        //     this.$router.go(-1); // 返回上一个页面
        // },
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