<template>
    <div class="main">
        <el-page-header @back="goBack" content="我的项目">
        </el-page-header>
        <div class="content">
            <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
                {{ this.thisProject.id }}-{{ this.thisProject.name }}的实验列表
            </h3>
            <div style="display: flex; justify-content: flex-start; padding-bottom: 20px;">
                <el-button icon="el-icon-circle-plus" type="success" @click="showDialog = true">为该项目创建新实验
                </el-button>
            </div>
            <el-tabs v-model="currentTab" type="card" @tab-click="handleClick">
                <el-tab-pane label="待实验" name="待实验"></el-tab-pane>
                <el-tab-pane label="正在实验" name="正在实验"></el-tab-pane>
                <el-tab-pane label="待审核" name="待审核"></el-tab-pane>
                <el-tab-pane label="已完成" name="已完成"></el-tab-pane>
            </el-tabs>

            <div class="section" v-if="currentTab === '待实验'">
                <h4>待实验</h4>
                <el-table :data="expList" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="创建时间" prop="time">
                        <template slot-scope="scope">
                            <!-- 格式化时间 -->
                            <div>{{ formatDate(scope.row.time) }}</div>
                            <!-- <div>{{ scope.row.time }}</div> -->
                        </template>
                    </el-table-column>
                    <!-- <el-table-column label="进度" prop="progress">
                        <template slot-scope="scope">
                            <el-progress :percentage="scope.row.progress"></el-progress>
                        </template>
                    </el-table-column> -->
                    <!-- 协作者 列 -->
                    <el-table-column label="协作者">
                        <template slot-scope="scope">
                            <div v-if="scope.row.collaborators && scope.row.collaborators.length > 0">
                                <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
                                    {{ collaborator.name }}
                                </div>
                            </div>
                            <el-tag v-else type="danger">还没有协作者！</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="配置文件">
                        <template slot-scope="scope">
                            <div v-if="scope.row.configURL !== null">
                                <el-tag type="success">有</el-tag>
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="180" align="center">
                        <template slot-scope="scope">
                            <el-link type="primary" style="margin-right: 10px;"
                                @click="handleAddFriendsToExp(scope.row.id, scope.row.name, scope.row.collaborators)">添加协作者</el-link>
                            <!-- <el-button size="mini" type="primary"
                                            @click="handleAddFriendsToExp(scope.row.id, scope.row.name, scope.row.collaborators, index)">
                                            添加审核协作者
                                        </el-button> -->
                            <el-dropdown>
                                <el-button size="mini" type="primary">
                                    操作<i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <!-- <el-dropdown-item>
                                        <el-button size="mini" type="primary"
                                            @click="handleAddFriendsToExp(scope.row.id, scope.row.name, scope.row.collaborators, index)">
                                            添加审核协作者
                                        </el-button>
                                    </el-dropdown-item> -->
                                    <el-dropdown-item>
                                        <el-button size="mini" type="success"
                                            @click="confirmStart(scope.$index, scope.row)">
                                            开始实验
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button size="mini" type="warning" @click="initialEdit(scope.row)">
                                            修改实验配置
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button size="mini" type="primary" @click="handleEditConfigFile(scope.row)">
                                            编辑配置文件
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <!-- <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                                            </el-button>
                                        </el-popconfirm> -->
                                        <el-button size="mini" icon="el-icon-delete" type="danger"
                                            @click="confirmDelete(scope.$index, scope.row)">删除
                                        </el-button>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="section" v-if="currentTab === '正在实验'">
                <h4>正在实验</h4>
                <el-table :data="proceeding" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="创建时间" prop="time">
                        <template slot-scope="scope">
                            <!-- 格式化时间 -->
                            <div>{{ formatDate(scope.row.time) }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column label="进度" prop="progress">
                        <template slot-scope="scope">
                            <el-progress :percentage="scope.row.progress"></el-progress>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="section" v-if="currentTab === '待审核'">
                <h4>待审核</h4>
                <el-table :data="reviewList" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="创建时间" prop="time">
                        <template slot-scope="scope">
                            <!-- 格式化时间 -->
                            <div>{{ formatDate(scope.row.time) }}</div>
                        </template>
                    </el-table-column>
                    <!-- <el-table-column label="进度" prop="progress">
                        <template slot-scope="scope">
                            <el-progress :percentage="scope.row.progress"></el-progress>
                        </template>
                    </el-table-column> -->
                    <el-table-column label="协作者">
                        <template slot-scope="scope">
                            <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
                                {{ collaborator.name }}
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="总待审核条数" prop="thisExpQA">
                        <template slot-scope="scope">
                            <el-tag type="warning">{{ scope.row.thisExpQA }}</el-tag>
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
                                        <el-button size="mini" type="primary"
                                            @click.stop="handleAssignExpirement(scope.row)">
                                            分发协作
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button size="mini" type="warning"
                                            @click.stop="handleReviewExpirement(scope.row)">
                                            审核结果
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <!-- <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                                            </el-button>
                                        </el-popconfirm> -->
                                        <el-button size="mini" icon="el-icon-delete" type="danger"
                                            @click="confirmDelete(scope.$index, scope.row)">删除
                                        </el-button>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="section" v-if="currentTab === '已完成'">
                <h4>已完成</h4>
                <el-table :data="doneList" style="width: 100%">
                    <el-table-column label="实验 ID" prop="id"></el-table-column>
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="创建时间" prop="time">
                        <template slot-scope="scope">
                            <!-- 格式化时间 -->
                            <div>{{ formatDate(scope.row.time) }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column label="协作者">
                        <template slot-scope="scope">
                            <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
                                {{ collaborator.name }}
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="180" align="center">
                        <template slot-scope="scope">
                            <el-button size="mini" type="primary" slot="reference" @click.stop> <!-- 阻止冒泡 -->
                                查看记录
                            </el-button>
                            <!-- <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                title="确定要删除此实验吗？">
                                <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                                </el-button>
                            </el-popconfirm> -->
                            <el-button size="mini" icon="el-icon-delete" type="danger"
                                @click="confirmDelete(scope.$index, scope.row)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <!-- 创建实验对话框 -->
        <el-dialog title="创建新实验" :visible.sync="showDialog" width="50%" @close="resetDialog">
            <div>
                <el-form ref="form" :model="newExpirement" label-width="200px">

                    <el-form-item label="实验名称">
                        <el-input v-model="newExpirement.name"></el-input>
                    </el-form-item>

                    <el-form-item label="指定实验模型API Key">
                        <el-select v-model="newExpirement.AK1" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定评估模型API Key">
                        <el-select v-model="newExpirement.AK2" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定实验数据集">
                        <el-select v-model="newExpirement.DS" placeholder="请选择">
                            <el-option v-for="item in thisProject.dataSet" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <!-- 进行实验配置文件的编辑 -->
                    <!-- <el-form-item>
                        <el-button type="primary" @click="showCodeEditorDialog = true">编辑实验配置文件</el-button>
                    </el-form-item> -->

                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="showDialog = false">取 消</el-button>
                <el-button type="primary" @click="handleAddNewExpirement">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 修改实验对话框 -->
        <el-dialog title="修改实验配置" :visible.sync="editDialog" width="50%" @close="resetEditDialog">
            <div>
                <el-form ref="form" :model="editExperiment" label-width="200px">

                    <el-form-item label="实验名称">
                        <el-input v-model="editExperiment.name"></el-input>
                    </el-form-item>

                    <el-form-item label="指定实验模型API Key">
                        <el-select v-model="editExperiment.AK1" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定评估模型API Key">
                        <el-select v-model="editExperiment.AK2" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定实验数据集">
                        <el-select v-model="editExperiment.DS" placeholder="请选择">
                            <el-option v-for="item in thisProject.dataSet" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>


            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialog = false">取 消</el-button>
                <el-button type="primary" @click="handleEditExperiment">确定</el-button>
            </span>
        </el-dialog>

        <!-- 代码编辑器 -->
        <el-dialog title="编辑 Python实验配置文件" :visible.sync="showCodeEditorDialog" width="50%" @opened="loadTemplate">
            <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
                <h4>当前实验:{{ currentExpName }} - {{ currentExpId }}</h4>
            </div>
            <div>
                <!-- 这里放置你的代码编辑器组件 -->
                <!-- 代码组件1 -->
                <h3> 编辑实验模型call函数</h3>
                <!-- <el-form ref="form">
                    <el-form-item label="实验模型类名">
                        <el-input v-model="LL1ClassName" style="width:200px"></el-input>
                    </el-form-item>
                </el-form> -->
                <div id="python-editor_1" style="height: 300px;"></div>
            </div>

            <div>
                <!-- 代码组件2 -->
                <h3> 编辑评估模型call函数</h3>
                <!-- <el-form ref="form">
                    <el-form-item label="评估模型类名">
                        <el-input v-model="LL2ClassName" style="width: 200px;"></el-input>
                    </el-form-item>
                </el-form> -->
                <div id="python-editor_2" style="height: 300px;"></div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetCodeEditor">取消</el-button>
                <el-button type="primary" @click="savePythonFile">保存文件</el-button>
            </span>
        </el-dialog>

        <!-- 将好友加入到实验协作的对话框 -->
        <template>

            <el-dialog title="请为当前实验添加协作者" :visible.sync="friendsToExp" @close="handleDialogClose">

                <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
                    <h4>当前实验:{{ currentExpName }} - {{ currentExpId }}</h4>
                </div>

                <el-checkbox-group v-model="selectFriendsId">
                    <el-checkbox v-for="friend in userFriends" :label="friend.id" :key="friend.id">
                        {{ friend.id }} - {{ friend.name }}
                    </el-checkbox>
                </el-checkbox-group>

                <span slot="footer" class="dialog-footer">
                    <el-button @click="handleDialogClose">取消</el-button>
                    <el-button type="primary" @click="handlefriendsToExp">确定</el-button>
                </span>
            </el-dialog>
        </template>

    </div>
</template>


<script>
import { getExperimentByProjectId } from '@/api/experiment'
import { deleteById, addExpirement, editExpirement, deleteOperationFile, checkOperationFile, addOperationFile, updateOperationFile } from '@/api/experiment'
import { getUserList, addFriendsToExperiment, getFriendsByExperimentId } from '@/api/collaborate'
import { getQACount } from '@/api/qa'
import { getExperimentProgress, updateExperimentStatus } from '@/api/expOperation'
import { startExp } from '@/api/expOperation'
import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-chrome';




// import { formToJSON } from 'axios';

export default {
    name: "ExperimentList",
    data() {
        return {
            currentTab: '待实验', // 默认选中的选项卡
            friendsToExp: false,
            showCodeEditorDialog: false,
            showDialog: false,
            editDialog: false,
            experimentList: [],
            newExpirement: { name: '', AK1: '', AK2: '', DS: '' },
            expList: [], // 待实验列表数据
            proceeding: [],//正在实验列表
            reviewList: [], // 待审核列表数据
            doneList: [], // 已完成列表数据
            thisProject: {},
            editExperiment: { name: '', AK1: '', AK2: '', DS: '', tPid: '' },
            pythonCode_1: '',
            pythonCode_2: '',
            // pythonFile: null,
            editor_1: null, // 存储编辑器实例
            editor_2: null, // 存储编辑器实例
            userFriends: [],
            selectFriendsId: [],
            currentExpName: '',
            currentExpId: '',
            thisRowCollaborators: [],
            // LL1ClassName: '',
            // LL2ClassName: ''
        }
    },
    mounted() {
        let storedProject = localStorage.getItem('thisProject');
        if (storedProject) {
            this.thisProject = JSON.parse(storedProject);
        }
        else {
            // 处理没有数据的情况，可能是跳转到此页面或刷新页面
            this.$router.push("/projectsList")
        }
        this.load();
    },
    methods:
    {
        load() {
            // this.initPythonEditor();
            const id = this.thisProject.id
            getExperimentByProjectId(id).then(res => {
                this.experimentList = res.data;
                console.log('获取的所有实验数据', this.experimentList)
                // 遍历 experimentList 并发起所有请求
                if (this.experimentList.length !== 0) {
                    const collaboratorsRequests = this.experimentList.map(experiment => {
                        return getFriendsByExperimentId(experiment.id).then(res => {
                            // 将 collaborators 数组添加到对应的实验记录中
                            console.log('获取实验协作者响应信息', res)
                            return {
                                ...experiment,
                                collaborators: res.data
                            };
                        });
                    });
                    // 等待所有请求完成
                    Promise.all(collaboratorsRequests).then(updatedExperimentList => {
                        // 更新 experimentList
                        this.experimentList = updatedExperimentList;
                        this.experimentList.forEach(exp => {
                            switch (exp.status) {
                                case 0:
                                    this.expList.push(exp);
                                    break;
                                case 1:
                                    this.proceeding.push(exp);
                                    break;
                                case 2:
                                    this.reviewList.push(exp);
                                    break;
                                case 3:
                                    this.doneList.push(exp);
                                    break;
                                // 你可以根据需要添加更多的状态分类
                            }
                        });
                        //获取每个待审核实验的审核记录条数
                        Promise.all(this.reviewList.map(exp => {
                            // 对每个exp调用getQAByExpirenceId函数
                            return getQACount(exp.id).then(res => {
                                // 将结果合并回exp对象
                                return {
                                    ...exp,
                                    thisExpQA: res.count,
                                };
                            });
                        })).then(updatedExperimentList => {
                            console.log('待审核',updatedExperimentList)
                            // 这里的updatedExperimentList包含了修改后的experimentList
                            // 可以在这里处理或更新状态
                            this.reviewList = updatedExperimentList;
                        }).catch(error => {
                            // 处理任何在Promise链中发生的错误
                            console.error("Error while updating experiment list:", error);
                        });
                    }).catch(error => {
                        // 处理可能出现的错误
                        console.error("Error fetching collaborators: ", error);
                    });
                    //如果有待实验则开始轮询
                    this.proceedingExp()
                }
            })
            getUserList(localStorage.getItem('uid')).then(res => {
                this.userFriends = res.data.filter(user => user.state === 1 || user.state === -1);
            })
        },
        handleAddNewExpirement() {
            if (this.newExpirement.name.trim()) {
                if (this.newExpirement.AK1 !== '' && this.newExpirement.Ak2 !== '' && this.newExpirement.DS !== '') {
                    // if (this.pythonFile !== null) {
                    const formData = new FormData();
                    // formData.append('configFile', this.pythonFile);
                    formData.append('name', this.newExpirement.name);
                    formData.append('AK1', this.newExpirement.AK1);
                    formData.append('AK2', this.newExpirement.AK2);
                    formData.append('DS', this.newExpirement.DS);
                    formData.append('pid', this.thisProject.id)
                    addExpirement(formData).then(res => {
                        if (res.success) {
                            this.resetDialog
                            this.showDialog = false; // 关闭对话框
                            this.$message({
                                message: '添加成功',
                                type: 'success'
                            });
                            this.setExpEmpty()
                            this.load()
                        }
                    })
                    // }
                    // else {
                    //     this.$message({
                    //         message: '实验文件尚未编辑',
                    //         type: 'warning'
                    //     });
                    // }
                }
                else {
                    this.$message({
                        message: '请选择apikey和数据集',
                        type: 'warning'
                    });
                }
            }
            else {
                this.$message({
                    message: '创建新实验各字段不能为空',
                    type: 'warning'
                });
            }
        },
        handleRemoveExpirement(index, row) {
            const deleteData = { tPid: row.id }
            deleteById(deleteData).then(res => {
                if (res.success) {
                    if (row.configURL !== null) {
                        deleteOperationFile(deleteData).then(res => {
                            if (res.success) {
                                this.afterDeleteExp(row, index)
                            }
                        })
                    }
                    else {
                        this.afterDeleteExp(row, index)
                    }
                }
            })
        },
        handleStartExpirement(index, row) {
            const id = { tPid: row.id }
            startExp(id).then(res => {
                if (res.success) {
                    this.$message({
                        message: row.id + '-' + row.name + '开始执行',
                        type: 'info'
                    });
                    this.setExpEmpty()
                    this.load()
                }
            })
        },
        handleAssignExpirement(experiment) {
            // 保存到 LocalStorage
            localStorage.setItem('thisExperiment', JSON.stringify(experiment));
            this.$router.push("/assignment")

        },
        handleReviewExpirement(experiment) {
            localStorage.setItem('thisExperiment', JSON.stringify(experiment));
            this.$router.push("/review")
        },
        goBack() {
            this.$router.go(-1); // 返回上一个页面
        },
        resetDialog() {
            this.newExpirement.name = '',
                this.newExpirement.AK1 = '',
                this.newExpirement.AK2 = '',
                this.newExpirement.DS = '',
                this.resetCodeEditor()
        },
        resetEditDialog() {
            this.editExperiment.name = '',
                this.editExperiment.AK1 = '',
                this.editExperiment.AK2 = '',
                this.editExperiment.DS = ''
        },
        formatDate(dateStr) {
            const date = new Date(dateStr);

            // 使用Intl.DateTimeFormat格式化日期，保持为GMT时间
            const formattedDate = new Intl.DateTimeFormat('zh-CN', { // 这里使用'zh-CN'来得到年月日的顺序
                year: 'numeric', // 数字年份
                month: '2-digit', // 2位数字月份
                day: '2-digit', // 2位数字日期
                hour: '2-digit', // 2位数字小时
                minute: '2-digit', // 2位数字分钟
                second: '2-digit', // 2位数字秒
                timeZone: 'UTC', // 指定时区为UTC，以保持与GMT一致
                hour12: false // 使用24小时制
            }).format(date);

            return formattedDate
        },
        handleEditExperiment() {
            if (this.editExperiment.name.trim()) {
                if (this.editExperiment.AK1 !== '' && this.editExperiment.Ak2 !== '' && this.editExperiment.DS !== '') {
                    const data = {
                        name: this.editExperiment.name,
                        AK1: this.editExperiment.AK1,
                        AK2: this.editExperiment.AK2,
                        DS: this.editExperiment.DS,
                        tPid: this.editExperiment.tPid
                    }
                    console.log('进行修改的实验数据：', data)
                    editExpirement(data).then(res => {
                        if (res.success) {
                            this.$message({
                                message: '修改成功',
                                type: 'success'
                            });
                            const updateData = { tPid: this.editExperiment.tPid }
                            updateOperationFile(updateData).then(res => {
                                if (res.success) {
                                    this.$message({
                                        message: '配置文件更新成功',
                                        type: 'success'
                                    });
                                }
                            })
                            this.resetEditDialog()
                            this.editDialog = false; // 关闭对话框
                            this.setExpEmpty()
                            this.load()
                        }
                    })
                }
                else {
                    this.$message({
                        message: '请选择apikey和数据集',
                        type: 'warning'
                    });
                }
            }
            else {
                this.$message({
                    message: '实验各字段不能为空',
                    type: 'warning'
                });
            }
        },
        initialEdit(row) {
            if (row.configURL != null) {
                this.editExperiment.name = row.name
                this.editExperiment.tPid = row.id
                console.log('当前进行修改的实验id', this.editExperiment.tPid)
                this.editDialog = true
            }
            else {
                this.$message({
                    message: '请先编辑实验配置文件！',
                    type: 'warning'
                });
            }
        },
        resetCodeEditor() {
            this.pythonCode_1 = '',
                this.pythonCode_2 = '',
                // this.pythonFile = null,
                // this.LL1ClassName='',
                // this.LL2ClassName='',
                this.showCodeEditorDialog = false
        },
        initPythonEditor_1(template) {
            if (document.getElementById('python-editor_1')) {
                // 初始化 Ace Editor1
                this.editor_1 = ace.edit("python-editor_1");
                this.editor_1.setTheme("ace/theme/chrome"); // 使用亮色主题
                this.editor_1.session.setMode("ace/mode/python");
                this.editor_1.setFontSize(18); // 设置字体大小为18px
                if (localStorage.getItem(this.currentExpId + '_1') === null)
                    this.editor_1.setValue(template, 1);
                else
                    this.editor_1.setValue(localStorage.getItem(this.currentExpId + '_1'), 1);
                this.pythonCode_1 = this.editor_1.getValue()

                // 监听代码改变事件
                this.editor_1.session.on('change', () => {
                    this.pythonCode_1 = this.editor_1.getValue();
                });
            }
            else {
                console.log('The #python-editor element does not exist.')
            }
        },
        initPythonEditor_2(template) {
            if (document.getElementById('python-editor_2')) {
                // 初始化 Ace Editor2
                this.editor_2 = ace.edit("python-editor_2");
                this.editor_2.setTheme("ace/theme/chrome"); // 使用亮色主题
                this.editor_2.session.setMode("ace/mode/python");
                this.editor_2.setFontSize(18); // 设置字体大小为18px
                if (localStorage.getItem(this.currentExpId + '_2') === null)
                    this.editor_2.setValue(template, 1);
                else
                    this.editor_2.setValue(localStorage.getItem(this.currentExpId + '_2'), 1);
                this.pythonCode_1 = this.editor_1.getValue()
                this.pythonCode_2 = this.editor_2.getValue()

                // 监听代码改变事件
                this.editor_2.session.on('change', () => {
                    this.pythonCode_2 = this.editor_2.getValue();
                });
            }
            else {
                console.log('The #python-editor element does not exist.')
            }
        },
        savePythonFile() {
            // if (this.LL1ClassName !== '' && this.LL2ClassName !== '') {
            console.log('LLM1配置', this.pythonCode_1)
            console.log('LLM2配置', this.pythonCode_2)

            let checkData = { tPid: this.currentExpId, code: this.pythonCode_1, className: 'new_llm1' }
            checkOperationFile(checkData).then(res => {
                if (res.success) {
                    let checkData = { tPid: this.currentExpId, code: this.pythonCode_2, className: 'new_llm2' }
                    checkOperationFile(checkData).then(res => {
                        if (res.success) {
                            // 使用模板字符串和换行符`\n`来确保两段代码之间有一个换行
                            // const combinedCode = `${this.pythonCode_1}\n${this.pythonCode_2}`;
                            // const fileBlob = new Blob([combinedCode], { type: 'text/plain' });
                            // this.pythonFile = new File([fileBlob], "script.py");

                            addOperationFile(this.currentExpId).then(res => {
                                if (res.success) {
                                    localStorage.setItem(this.currentExpId + '_1', this.pythonCode_1)
                                    localStorage.setItem(this.currentExpId + '_2', this.pythonCode_2)
                                    this.$message({
                                        message: '编辑成功！',
                                        type: 'success'
                                    });
                                    this.setExpEmpty()
                                    this.load()
                                    this.resetCodeEditor()
                                }
                            })
                        }
                        else {
                            this.$message({
                                message: '评估模型call函数编译失败',
                                type: 'danger'
                            })
                        }
                    })
                }
                else {
                    this.$message({
                        message: '实验模型call函数编译失败',
                        type: 'danger'
                    })

                }
            })
            // }
            // else {
            //     this.$message({
            //         message: '类名不可为空！',
            //         type: 'warning'
            //     })
            // }
        },
        loadTemplate() {
            fetch('/codeTemplate_L1.txt')
                .then(response => response.text())
                .then(data => {
                    this.initPythonEditor_1(data);
                })
                .catch(error => {
                    console.error('Error loading the template:', error)
                    this.$message({
                        message: '无法加载LL1模板文件',
                        type: 'error'
                    });
                }
                );
            fetch('/codeTemplate_L2.txt')
                .then(response => response.text())
                .then(data => {
                    this.initPythonEditor_2(data);
                })
                .catch(error => {
                    console.error('Error loading the template:', error)
                    this.$message({
                        message: '无法加载LL2模板文件',
                        type: 'error'
                    });
                }
                );
        },
        handleAddFriendsToExp(id, name, collaborators) {
            this.currentExpId = id,
                this.currentExpName = name
            this.friendsToExp = true,
                this.thisRowCollaborators = collaborators
        },
        handleDialogClose() {
            this.selectFriendsId = [],
                this.friendsToExp = false
        },
        handlefriendsToExp() {
            this.selectFriendsId.forEach(id => {
                //检查id是否在thisRowCollabortors里
                const findExistOne = this.thisRowCollaborators.find(collab => collab.id === id);
                if (!findExistOne) {
                    const data = { TPid: this.currentExpId, uid: id };
                    addFriendsToExperiment(data).then(res => {
                        if (res.success) {
                            // 请求成功的处理
                            this.$message({
                                message: '加入成功！',
                                type: 'success'
                            });

                        } else {
                            // 请求失败的处理（可选）
                            this.$message({
                                message: '加入失败',
                                type: 'error'
                            });
                        }
                    })
                }
                else {
                    this.$message({
                        message: '加入失败' + findExistOne.name + '已经在该项目中',
                        type: 'error'
                    });
                }
                this.setExpEmpty()
                this.load()
            })
            this.handleDialogClose()
        },
        setExpEmpty() {
            this.reviewList = []
            this.proceeding = []
            this.doneList = []
            this.expList = []
        },
        confirmDelete(index, row) {
            this.$confirm('是否删除该实验？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.handleRemoveExpirement(index, row)
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },
        confirmStart(index, row) {
            if (row.configURL !== null) {
                this.$confirm('确定执行该实验吗？一旦执行将直至结束', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.handleStartExpirement(index, row)
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消执行'
                    });
                });
            }
            else {
                this.$message({
                    message: '请先编辑实验配置文件！',
                    type: 'warning'
                })
            }
        },
        handleEditConfigFile(row) {
            this.currentExpId = row.id
            this.currentExpName = row.name
            this.showCodeEditorDialog = true
        },
        proceedingExp() {
            const interval = setInterval(() => {
                // 如果 this.proceeding 为空，则停止轮询
                if (!this.proceeding.length || this.currentTab === '正在实验') {
                    clearInterval(interval);
                    return;
                }

                // 遍历 this.proceeding 中的每个实验
                this.proceeding.forEach((experiment, index) => {

                    getExperimentProgress(experiment.id).then(res => {

                        this.proceeding[index].progress = res.process


                        if (this.proceeding[index].progress === 100) {
                            // 更新实验状态
                            const updateExp = { TPid: experiment.id, uid: localStorage.getItem('uid') }
                            updateExperimentStatus(updateExp).then(res => {
                                if (res.success) {
                                    this.$message({
                                        type: 'info',
                                        message: experiment.id + '-' + experiment.name + '执行完成'
                                    });
                                    this.setExpEmpty()
                                    this.load()
                                }
                            });
                        }


                    });
                });
            }, 5000); // 设置轮询间隔为 5 秒
        },
        // proceedingExp() {
        //     const interval = setInterval(() => {
        //         // 如果 this.proceeding 为空，则停止轮询
        //         if (!this.proceeding.length) {
        //             clearInterval(interval);
        //             return;
        //         }

        //         // 遍历 this.proceeding 中的每个实验
        //         this.proceeding.forEach((experiment, index) => {

        //             this.proceeding[index].progress = this.proceeding[index].progress + 20


        //             if (this.proceeding[index].progress === 100) {

        //                 this.$message({
        //                     type: 'info',
        //                     message: experiment.id + '-' + experiment.name + '执行完成'
        //                 });
        //                 this.proceeding[index].progress = 0
        //             }



        //         });
        //     }, 5000); // 设置轮询间隔为 5 秒
        // },
        handleClick(tab, event) {
            console.log(tab, event);
        },
        afterDeleteExp(row, index) {
            localStorage.removeItem(row.id + '_1')
            localStorage.removeItem(row.id + '_2')
            this.$message({
                message: '删除成功',
                type: 'success',
            });
            switch (row.status) {
                case 0:
                    this.expList.splice(index, 1);
                    break;
                case 2:
                    this.reviewList.splice(index, 1);
                    break;
                case 3:
                    this.doneList.splice(index, 1);
                    break;
                // 你可以根据需要添加更多的状态分类
            }
        }
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