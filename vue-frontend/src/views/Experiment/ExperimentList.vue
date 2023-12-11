<template>
    <div class="main">

        <el-page-header @back="goBack" content="我的项目">
        </el-page-header>
        <div class="content">
            <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
                {{ this.projectId }}-{{ this.projectName }}项目的实验列表
            </h3>
            <div style="display: flex; justify-content: flex-start; padding-bottom: 20px;">
                <el-button icon="el-icon-circle-plus" type="success" @click="showDialog = true">添加实验
                </el-button>
            </div>
            <div class="section">
                <h4>待实验</h4>
                <el-table :data="expList" style="width: 100%">
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
                            <el-dropdown>
                                <el-button size="mini" type="primary">
                                    操作<i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item>
                                        <el-button size="mini" type="success"
                                            @click.stop="handleStartExpirement(scope.$index, scope.row.id)">
                                            开始实验
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red"
                                            @confirm.stop="handleRemoveExpirement(scope.$index, scope.row.id)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" type="danger" slot="reference" @click.stop> <!-- 阻止冒泡 -->
                                                删除
                                            </el-button>
                                        </el-popconfirm>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

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
                            <el-dropdown>
                                <el-button size="mini" type="primary">
                                    操作<i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item>
                                        <el-button size="mini" type="warning"
                                            @click.stop="handleReviewExpirement(scope.$index, scope.row.id)">
                                            开始审核
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red"
                                            @confirm.stop="handleRemoveExpirement(scope.$index, scope.row.id)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" type="danger" slot="reference" @click.stop> <!-- 阻止冒泡 -->
                                                删除
                                            </el-button>
                                        </el-popconfirm>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="section">
                <h4>已完成</h4>
                <el-table :data="doneList" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="时间" prop="time"></el-table-column>
                    <el-table-column label="用例数" prop="caseNum"></el-table-column>
                    <el-table-column label="大模型" prop="LLMName"></el-table-column>
                    <el-table-column label="操作" width="180" align="center">
                        <template slot-scope="scope">
                            <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                icon-color="red" @confirm.stop="handleRemoveExpirement(scope.$index, scope.row.id)"
                                title="确定要删除此实验吗？">
                                <el-button size="mini" type="danger" slot="reference" @click.stop> <!-- 阻止冒泡 -->
                                    删除
                                </el-button>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <el-dialog
        title="创建新实验"
        :visible.sync="showDialog"
        width="50%"
        @close="resetDialog">
      <div>
        <!-- <el-form ref="form" :model="newApiKey" label-width="100px">

          <el-form-item label="接口来源">
            <el-input v-model="newApiKey.name"></el-input>
          </el-form-item>

          <el-form-item label="KEY内容">
            <el-input v-model="newApiKey.value"></el-input>
          </el-form-item>

            <el-form-item label="认证token">
            <el-input v-model="newApiKey.auth"></el-input>
          </el-form-item>
        </el-form> -->


      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @clic.stop>确 定</el-button>
      </span>
    </el-dialog>
    </div>
</template>
  
  
<script>
// import { getExperimentByProjectId } from '@/api/experiment'
import { deleteById } from '@/api/experiment'

export default {
    name: "ExperimentList",
    data() {
        return {
            showDialog:false,
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
            expList: [], // 待实验列表数据
            reviewList: [], // 待审核列表数据
            doneList: [], // 已完成列表数据
            projectId: '',
            projectName: ''
        }
    },
    mounted() {
        this.projectId = this.$route.params.id;
        this.projectName = this.$route.params.name;
        this.load()
    },
    methods:
    {
        load() {
            // const id = this.projectId
            // getExperimentByProjectId(id).then(res => {
            //     this.experimentList = res.data;
            // })
            this.experimentList.forEach(exp => {
                switch (exp.status) {
                    case '待实验':
                        this.expList.push(exp);
                        break;
                    case '待审核':
                        this.reviewList.push(exp);
                        break;
                    case '已完成':
                        this.doneList.push(exp);
                        break;
                    // 你可以根据需要添加更多的状态分类
                }
            });

        },
        handleRemoveExpirement(index, id) {
            const deleteId = id
            deleteById(deleteId).then(res => {
                if (res.success) {
                    this.dataSet.splice(index, 1);
                    this.$message({
                        message: '删除成功',
                        type: 'success',
                    });
                }
            })
            this.load()
        },
        handleStartExpirement(index, id) {
            console.log(index, id)
        },
        handleReviewExpirement(index, id) {
            console.log(index, id)
        },
        goBack() {
            this.$router.go(-1); // 返回上一个页面
        },
        resetDialog() {
          
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