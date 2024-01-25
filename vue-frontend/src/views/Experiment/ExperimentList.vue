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
            <div class="section">
                <h4>待实验</h4>
                <el-table :data="expList" style="width: 100%">
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
                    <!-- <el-table-column label="进度" prop="progress">
                        <template slot-scope="scope">
                            <el-progress :percentage="scope.row.progress"></el-progress>
                        </template>
                    </el-table-column> -->
                    <!-- 协作者 列 -->
                    <el-table-column label="协作者">
                        <template slot-scope="scope">
                            <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
                                {{ collaborator.name }}
                            </div>
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
                                            @click="handleAddFriendsToExp(scope.row.id, scope.row.name)">
                                            添加审核协作者
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button size="mini" type="success"
                                            @click="handleStartExpirement(scope.$index, scope.row.id)">
                                            开始实验
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button size="mini" type="warning" icon="el-icon-edit"
                                            @click="editDialog = true, initialEdit(scope.row, scoe.$index)">
                                            修改实验
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
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
                <h4>正在实验</h4>
                <el-table :data="proceeding" style="width: 100%">
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
                                            icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
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
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="时间" prop="time">
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
                                        <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                            title="确定要删除此实验吗？">
                                            <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
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
                    <el-table-column label="测试模型" prop="AK1.name"></el-table-column>
                    <el-table-column label="评估模型" prop="AK2.name"></el-table-column>
                    <el-table-column label="数据集" prop="dataSet.name"></el-table-column>
                    <el-table-column label="时间" prop="time">
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
                            <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                icon-color="red" @confirm="handleRemoveExpirement(scope.$index, scope.row)"
                                title="确定要删除此实验吗？">
                                <el-button size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                                </el-button>
                            </el-popconfirm>
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
                    <el-form-item>
                        <el-button type="primary" @click="showCodeEditorDialog = true">编辑 Python实验配置文件</el-button>
                    </el-form-item>

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
        <el-dialog title="编辑 Python实验配置文件" :visible.sync="showCodeEditorDialog" width="70%" @opened="loadTemplate">
            <div>
                <!-- 这里放置你的代码编辑器组件 -->
                <div id="python-editor" style="height: 700px;"></div>
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
                    <h4>当前实验{{ currentExpName }} - {{ currentExpId }}</h4>
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
import { deleteById, addExpirement, editExpirement } from '@/api/experiment'
import { getUserList, addFriendsToExperiment, getFriendsByExperimentId } from '@/api/collaborate'
import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-chrome';



// import { formToJSON } from 'axios';

export default {
    name: "ExperimentList",
    data() {
        return {
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
            editExperiment: { name: '', AK1: '', AK2: '', DS: '', tPid: '', index: '' },
            pythonCode: '',
            pythonFile: null,
            editor: null, // 存储编辑器实例
            userFriends: [],
            selectFriendsId: [],
            currentExpName: '',
            currentExpId: ''
        }
    },
    mounted() {
        let storedProject = localStorage.getItem('thisProject');
        if (storedProject) {
            this.thisProject = JSON.parse(storedProject);
        }
        else {
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
                // 遍历 experimentList 并发起所有请求
                const collaboratorsRequests = this.experimentList.map(experiment => {
                    return getFriendsByExperimentId(experiment.id).then(collaborators => {
                        // 将 collaborators 数组添加到对应的实验记录中
                        return {
                            ...experiment,
                            collaborators: collaborators
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
                }).catch(error => {
                    // 处理可能出现的错误
                    console.error("Error fetching collaborators: ", error);
                });

            })
            getUserList(localStorage.getItem('uid')).then(res => {
                this.userFriends = res.data.filter(user => user.state !== 0);
            })
        },
        handleAddNewExpirement() {
            if (this.newExpirement.name.trim()) {
                if (this.newExpirement.AK1 !== '' && this.newExpirement.Ak2 !== '' && this.newExpirement.DS !== '') {
                    if (this.pythonFile !== null) {
                        // const data = {
                        //     name: this.newExpirement.name,
                        //     AK1: this.newExpirement.AK1,
                        //     AK2: this.newExpirement.AK2,
                        //     DS: this.newExpirement.DS,
                        //     pid: this.thisProject.id
                        // }
                        const formData = new FormData();
                        formData.append('configFile', this.pythonFile);
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
                                this.load()
                            }
                        })
                    }
                    else {
                        this.$message({
                            message: '实验文件尚未编辑',
                            type: 'warning'
                        });
                    }
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
                    this.load()
                    this.$message({
                        message: '删除成功',
                        type: 'success',
                    });
                    this.load()
                }
            })
        },
        handleStartExpirement(index, id) {
            console.log(index, id)
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
                this.editExperiment.Ak2 = '',
                this.editExperiment.DS = '',
                this.editExperiment.index = ''
        },
        formatDate(dateStr) {
            // 使用 JavaScript 的 Date 对象进行解析和格式化
            // 这里是一个简单的示例，您可以根据需要调整格式
            const date = new Date(dateStr);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
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
                    editExpirement(data).then(res => {
                        if (res.success) {
                            this.resetEditDialog
                            this.editDialog = false; // 关闭对话框
                            this.$message({
                                message: '修改成功',
                                type: 'success'
                            });
                            this.expList.splice(this.editExperiment.index, 1)
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
        initialEdit(row, index) {
            this.editExperiment.name = row.name
            this.editExperiment.tPid = row.id
            this.editExperiment.index = index

        },
        resetCodeEditor() {
            this.pythonCode = '',
                this.pythonFile = null,
                this.showCodeEditorDialog = false
        },
        initPythonEditor(template) {
            if (document.getElementById('python-editor')) {
                // 初始化 Ace Editor
                this.editor = ace.edit("python-editor");
                this.editor.setTheme("ace/theme/chrome"); // 使用亮色主题
                this.editor.session.setMode("ace/mode/python");
                this.editor.setFontSize(18); // 设置字体大小为18px
                this.editor.setValue(template, 1);
                this.pythonCode = this.editor.getValue()

                // 监听代码改变事件
                this.editor.session.on('change', () => {
                    this.pythonCode = this.editor.getValue();
                });
            }
            else {
                console.log('The #python-editor element does not exist.')
            }
        },
        savePythonFile() {
            console.log('实验配置文件编辑', this.pythonCode)
            const fileBlob = new Blob([this.pythonCode], { type: 'text/plain' });
            this.pythonFile = new File([fileBlob], "script.py");
            this.$message({
                message: '编辑成功！',
                type: 'success'
            });
            this.showCodeEditorDialog = false;
        },
        loadTemplate() {
            fetch('./codeTemplate.txt')
                .then(response => response.text())
                .then(data => {
                    this.initPythonEditor(data);
                })
                .catch(error => console.error('Error loading the template:', error));
        },
        handleAddFriendsToExp(id, name) {
            this.currentExpId = id,
                this.currentExpName = name
            this.friendsToExp = true
        },
        handleDialogClose() {
            this.selectFriendsId = [],
                this.friendsToExp = false
        },
        handlefriendsToExp() {
            this.selectFriendsId.forEach(id => {
                const data = { expId: this.currentExpId, fid: id };
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
            })
            this.handleDialogClose()
            this.load()
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