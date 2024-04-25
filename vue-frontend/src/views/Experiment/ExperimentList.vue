<template>
    <div class="main">
        <el-page-header @back="goBack" content="我的项目">
        </el-page-header>
        <div class="content">
            <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 0px; text-align: center">
                {{ this.thisProject.name }}的测试列表
            </h3>
            <div style="display: flex; justify-content: flex-start; padding-bottom: 20px;">
                <el-button plain icon="el-icon-circle-plus" type="success" @click="showDialog = true">为该项目创建新测试
                </el-button>
            </div>
            <el-tabs v-model="currentTab" type="card" @tab-click="handleClick">
                <el-tab-pane label="待测试" name="待测试"></el-tab-pane>
                <el-tab-pane label="正在测试" name="正在测试"></el-tab-pane>
                <el-tab-pane label="待审核" name="待审核"></el-tab-pane>
                <el-tab-pane label="已完成" name="已完成"></el-tab-pane>
            </el-tabs>

            <div class="section" v-if="currentTab === '待测试'">
                <h4>待测试</h4>
                <el-table :data="expList" style="width: 100%" v-loading="loading">
                    <!-- <el-table-column label="测试 ID" prop="id"></el-table-column> -->
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试类型">
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.type === 1">基础能力测试</el-tag>
                            <el-tag v-else-if="scope.row.type === 2">幻觉测试</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="被测模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK1">
                                {{ scope.row.AK1.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="评估模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK2">
                                {{ scope.row.AK2.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="数据集">
                        <template slot-scope="scope">
                            <div v-if="scope.row.dataSet">
                                {{ scope.row.dataSet.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
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
                            <el-tag v-else type="danger">无协作者</el-tag>
                        </template>
                    </el-table-column>
                    <!-- <el-table-column label="配置文件">
                        <template slot-scope="scope">
                            <div v-if="scope.row.configURL !== null">
                                <el-tag type="success">有</el-tag>
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column> -->
                    <el-table-column label="" width="180" align="center">
                        <template slot-scope="scope">
                            <el-link type="primary" style="margin-right: 10px;"
                                @click="handleAddFriendsToExp(scope.row.id, scope.row.name, scope.row.collaborators)">添加协作者</el-link>
                            <el-dropdown>
                                <el-button plain size="mini" type="primary">操作
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item>
                                        <el-button plain icon="el-icon-caret-right" size="mini" type="success"
                                            @click="confirmStart(scope.$index, scope.row)" :loading="isTesting">
                                            开始测试
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-s-tools" type="warning"
                                            @click="initialEdit(scope.row)">
                                            修改测试配置
                                        </el-button>
                                    </el-dropdown-item>
                                    <!-- <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-edit" type="primary"
                                            @click="handleGenerateConfig(scope.row)">
                                            生成配置文件
                                        </el-button>
                                    </el-dropdown-item> -->
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-delete" type="danger"
                                            @click="confirmDelete(scope.$index, scope.row)">删除
                                        </el-button>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="section" v-if="currentTab === '正在测试'">
                <h4>正在测试</h4>
                <el-table :data="proceeding" style="width: 100%" v-loading="loading">
                    <!-- <el-table-column label="测试 ID" prop="id"></el-table-column> -->
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试类型">
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.type === 1">基础能力测试</el-tag>
                            <el-tag v-else-if="scope.row.type === 2">幻觉测试</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="被测模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK1">
                                {{ scope.row.AK1.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="评估模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK2">
                                {{ scope.row.AK2.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="数据集">
                        <template slot-scope="scope">
                            <div v-if="scope.row.dataSet">
                                {{ scope.row.dataSet.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
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
                <el-table :data="reviewList" style="width: 100%" v-loading="loading">
                    <!-- <el-table-column label="测试 ID" prop="id"></el-table-column> -->
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试类型">
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.type === 1">基础能力测试</el-tag>
                            <el-tag v-else-if="scope.row.type === 2">幻觉测试</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="被测模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK1">
                                {{ scope.row.AK1.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="评估模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK2">
                                {{ scope.row.AK2.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="数据集">
                        <template slot-scope="scope">
                            <div v-if="scope.row.dataSet">
                                {{ scope.row.dataSet.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
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
                            <div v-if="scope.row.collaborators && scope.row.collaborators.length > 0">
                                <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
                                    {{ collaborator.name }}
                                </div>
                            </div>
                            <el-tag v-else type="danger">无协作者</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="" width="180" align="center">
                        <template slot-scope="scope">
                            <el-link type="primary" style="margin-right: 10px;"
                                @click="handleAddFriendsToExp(scope.row.id, scope.row.name, scope.row.collaborators)">添加协作者</el-link>
                            <el-dropdown>
                                <el-button plain size="mini" type="primary">操作
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </el-button>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-s-promotion" type="primary"
                                            @click.stop="handleAssignExperiment(scope.row)">
                                            分发协作
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-document-checked" type="warning"
                                            @click.stop="handleReviewExperiment(scope.row)">
                                            审核结果
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-refresh" type="info"
                                            @click.stop="handleUpdate(scope.row)" :loading="isUpdate">
                                            更新报告
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-download" type="success"
                                            @click.stop="handleDownload(scope.row)" :loading="isUpdate">
                                            下载报告
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <el-button plain size="mini" icon="el-icon-notebook-2"
                                            @click.stop="handleInteraction(scope.row)">
                                            交互记录
                                        </el-button>
                                    </el-dropdown-item>
                                    <el-dropdown-item>
                                        <!-- <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                            icon-color="red" @confirm="handleRemoveExperiment(scope.$index, scope.row)"
                                            title="确定要删除此测试吗？">
                                            <el-button plain size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                                            </el-button>
                                        </el-popconfirm> -->
                                        <el-button plain size="mini" icon="el-icon-delete" type="danger"
                                            @click="confirmDelete(scope.$index, scope.row)">删除
                                        </el-button>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </template>
                    </el-table-column>
                    <el-table-column label="总待审核条数" prop="thisExpQA">
                        <template slot-scope="scope">
                            <el-tag type="warning"> {{ scope.row.thisExpQA }}</el-tag>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div class="section" v-if="currentTab === '已完成'">
                <h4>已完成</h4>
                <el-table :data="doneList" style="width: 100%" v-loading="loading">
                    <!-- <el-table-column label="测试 ID" prop="id"></el-table-column> -->
                    <el-table-column label="名称" prop="name"></el-table-column>
                    <el-table-column label="测试类型">
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.type === 1">基础能力测试</el-tag>
                            <el-tag v-else-if="scope.row.type === 2">幻觉测试</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="被测模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK1">
                                {{ scope.row.AK1.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="评估模型">
                        <template slot-scope="scope">
                            <div v-if="scope.row.AK2">
                                {{ scope.row.AK2.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="数据集">
                        <template slot-scope="scope">
                            <div v-if="scope.row.dataSet">
                                {{ scope.row.dataSet.name }}
                            </div>
                            <el-tag v-else type="danger">无</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="创建时间" prop="time">
                        <template slot-scope="scope">
                            <!-- 格式化时间 -->
                            <div>{{ formatDate(scope.row.time) }}</div>
                        </template>
                    </el-table-column>
                    <el-table-column label="协作者">
                        <template slot-scope="scope">
                            <div v-if="scope.row.collaborators && scope.row.collaborators.length > 0">
                                <div v-for="collaborator in scope.row.collaborators" :key="collaborator.id">
                                    {{ collaborator.name }}
                                </div>
                            </div>
                            <el-tag v-else type="warning">无协作者</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="350" align="center">
                        <template slot-scope="scope">
                            <el-button plain size="mini" icon="el-icon-download" type="success"
                                style="margin-bottom: 10px;" @click.stop="handleDownload(scope.row)"
                                :loading="isUpdate">
                                下载报告
                            </el-button>
                            <!-- <el-popconfirm confirm-button-text="确定" cancel-button-text="不用了" icon="el-icon-info"
                                icon-color="red" @confirm="handleRemoveExperiment(scope.$index, scope.row)"
                                title="确定要删除此测试吗？">
                                <el-button plain size="mini" icon="el-icon-delete" type="danger" slot="reference">删除
                                </el-button>
                            </el-popconfirm> -->
                            <el-button plain size="mini" icon="el-icon-notebook-2"
                                @click.stop="handleInteraction(scope.row)">
                                交互记录
                            </el-button>
                            <el-button plain size="mini" icon="el-icon-delete" type="danger"
                                @click="confirmDelete(scope.$index, scope.row)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <!-- 创建测试对话框 -->
        <el-dialog title="创建新测试" :visible.sync="showDialog" width="50%" @close="resetDialog">
            <div>
                <el-form ref="form" :model="newExperiment" label-width="150px">

                    <el-form-item label="测试名称">
                        <el-input v-model="newExperiment.name"></el-input>
                    </el-form-item>

                    <el-form-item label="指定测试类型">
                        <el-switch v-model="newExperiment.type" active-color="#13ce66" inactive-color="#409EFF"
                            :active-value="2" :inactive-value="1" active-text="幻觉测试" inactive-text="基础能力测试">
                        </el-switch>
                    </el-form-item>

                    <el-form-item label="指定被测模型API Key">
                        <el-select v-model="newExperiment.AK1" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id" :label="`${item.name}`"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定评估模型API Key" v-if="newExperiment.type === 1">
                        <el-select v-model="newExperiment.AK2" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id" :label="`${item.name}`"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定测试数据集">
                        <el-select v-model="newExperiment.DS" placeholder="请选择">
                            <el-option v-for="item in thisProject.dataSet" :key="item.id" :label="`${item.name}`"
                                :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button plain @click="showDialog = false">取 消</el-button>
                <el-button plain type="primary" @click="handleAddNewExperiment">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 修改测试对话框 -->
        <el-dialog title="修改测试配置" :visible.sync="editDialog" width="50%" @close="resetEditDialog">
            <h4>当前测试:{{ editExperiment_name }}</h4>
            <div>
                <el-form ref="form" label-width="200px">

                    <el-form-item label="测试名称">
                        <el-input v-model="editExperiment_name"></el-input>
                    </el-form-item>

                    <el-form-item label="指定测试类型">
                        <el-switch v-model="editExperiment_type" active-color="#13ce66" inactive-color="#409EFF"
                            :active-value="2" :inactive-value="1" active-text="幻觉测试" inactive-text="基础能力测试">
                        </el-switch>
                    </el-form-item>

                    <el-form-item label="指定被测模型API Key">
                        <el-select v-model="editExperiment_AK1" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定评估模型API Key" v-if="editExperiment_type === 1">
                        <el-select v-model="editExperiment_AK2" placeholder="请选择">
                            <el-option v-for="item in thisProject.apiKey" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="指定测试数据集">
                        <el-select v-model="editExperiment_DS" placeholder="请选择">
                            <el-option v-for="item in thisProject.dataSet" :key="item.id"
                                :label="`${item.id} - ${item.name}`" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>


            </div>
            <span slot="footer" class="dialog-footer">
                <el-button plain @click="editDialog = false">取 消</el-button>
                <el-button plain type="primary" @click="handleEditExperiment">确定</el-button>
            </span>
        </el-dialog>

        <!-- 代码编辑器 -->
        <!-- <el-dialog title="编辑 Python测试配置文件" :visible.sync="showCodeEditorDialog" width="50%" @opened="loadTemplate">
            <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
                <h4>当前测试:{{ currentExpName }}</h4>
            </div>
            <div>
                <h3> 编辑被测模型调用函数</h3>
                <div id="python-editor_1" style="height: 300px;"></div>
            </div>

            <div>
                <h3> 编辑评估模型调用函数</h3>
                <div id="python-editor_2" style="height: 300px;"></div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button plain @click="resetCodeEditor">取消</el-button>
                <el-button plain type="primary" @click="savePythonFile">保存文件</el-button>
            </span>
        </el-dialog> -->

        <!-- 将好友加入到测试协作的对话框 -->
        <template>

            <el-dialog title="请为当前测试添加协作者" :visible.sync="friendsToExp" @close="handleDialogClose">
                <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
                    <h4>当前测试:{{ currentExpName }}</h4>
                </div>

                <div v-if="userFriends && userFriends.length > 0">
                    <el-checkbox-group v-model="selectFriendsId">
                        <el-checkbox v-for="friend in userFriends" :label="friend.id" :key="friend.id">
                            {{ friend.name }}
                        </el-checkbox>
                    </el-checkbox-group>
                </div>
                <el-empty v-else description="暂无好友"></el-empty>

                <span slot="footer" class="dialog-footer">
                    <el-button plain @click="handleDialogClose">取消</el-button>
                    <el-button plain type="primary" @click="handlefriendsToExp">确定</el-button>
                </span>
            </el-dialog>
        </template>

        <!-- 测试报告下载对话框 -->
        <template>

            <el-dialog title="下载测试报告" :visible.sync="downloader" @close="downloadClose">

                <div style="text-align:left; margin-top: 5px;margin-bottom: 10px;">
                    <h4>当前测试:{{ currentExpName }}</h4>
                </div>

                <!-- <el-select v-model="selectVersion" placeholder="请选择">
                            <el-option v-for="index in reportCount" :key="index" :label="`V-${index}`" :value="index">
                            </el-option>
                        </el-select> -->

                <el-form>
                    <el-form-item>
                        <el-table :data="downLoadTable">
                            <el-table-column prop="index" label="版本" align="center">
                                <template slot-scope="scope">
                                    <span
                                        v-if="scope.row.index === downLoadTable.length && currentExpStatus === 3">Version-final</span>
                                    <span v-else>Version-{{ scope.row.index }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="下载" align="center">
                                <template slot-scope="scope">
                                    <el-button class="down-load" icon="el-icon-download" circle style="font-size: 18px;"
                                        @click="confirmDownload(scope.row.index)"></el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button plain @click="downloadClose">取消</el-button>
                    <!-- <el-button plain type="primary" @click="confirmDownload">确定</el-button> -->
                </span>
            </el-dialog>
        </template>
    </div>
</template>


<script>
import { getExperimentByProjectId } from '@/api/experiment'
import { deleteById, addExperiment, editExperiment, deleteOperationFile, checkOperationFile, generateOperationFile } from '@/api/experiment'
import { getUserList, addFriendsToExperiment, getFriendsByExperimentId } from '@/api/collaborate'
import { getQACount } from '@/api/qa'
import { getExperimentProgress, updateExperimentStatus, genReport, getReportNum, errorHandle } from '@/api/expOperation'
import { startExp, updateReport } from '@/api/expOperation'
import { getCallFunction, testConnectivity } from "@/api/apiConfig"
import config from "@/services/conf"
// import ace from 'ace-builds/src-noconflict/ace';
// import 'ace-builds/src-noconflict/mode-python';
// import 'ace-builds/src-noconflict/theme-chrome';




// import { formToJSON } from 'axios';

export default {
    name: "ExperimentList",
    data() {
        return {
            isTesting: false,
            loading: true,
            isUpdate: false,
            downLoadTable: [],
            currentTab: '', // 默认选中的选项卡
            friendsToExp: false,
            // showCodeEditorDialog: false,
            showDialog: false,
            editDialog: false,
            downloader: false,
            experimentList: [],
            newExperiment: { name: '', AK1: null, AK2: null, DS: null, type: 1 },
            // newExperiment: { name: '', AK1: '', AK2: '', DS: ''},
            expList: [], // 待测试列表数据
            proceeding: [],//正在测试列表
            reviewList: [], // 待审核列表数据
            doneList: [], // 已完成列表数据
            thisProject: {},
            // editExperiment: { name: '', AK1:'', AK2:'', DS:'', id: '' },
            editExperiment_id: '',
            editExperiment_name: '',
            editExperiment_AK1: null,
            editExperiment_AK2: null,
            editExperiment_DS: null,
            editExperiment_type: 1,
            // pythonCode_1: '',
            // pythonCode_2: '',
            // pythonFile: null,
            // editor_1: null, // 存储编辑器实例
            // editor_2: null, // 存储编辑器实例
            userFriends: [],
            selectFriendsId: [],
            currentExpName: '',
            currentExpId: '',
            currentExpStatus: null,
            thisRowCollaborators: [],
            reportCount: null,
            // selectVersion: null,
            // LL1ClassName: '',
            // LL2ClassName: ''
        }
    },
    mounted() {
        let storedProject = localStorage.getItem('thisProject');
        if (storedProject !== null) {
            this.thisProject = JSON.parse(storedProject);
            if (localStorage.getItem('currentTab')) {
                this.currentTab = localStorage.getItem('currentTab')
            }
            else {
                this.currentTab = '待测试'
                localStorage.setItem('currentTab', '待测试')
            }
        }
        else {
            // 处理没有数据的情况，可能是跳转到此页面或刷新页面
            this.$router.push("/projectsList")
        }
        this.load();
        setTimeout(() => {
            this.loading = false
        }, 300);
    },
    methods:
    {
        load() {
            // this.initPythonEditor();
            const id = this.thisProject.id
            getExperimentByProjectId(id).then(res => {
                this.experimentList = res.data;
                console.log('获取的所有测试数据', this.experimentList)
                // 遍历 experimentList 并发起所有请求
                if (this.experimentList.length !== 0) {
                    const collaboratorsRequests = this.experimentList.map(experiment => {
                        return getFriendsByExperimentId(experiment.id).then(res => {
                            // 将 collaborators 数组添加到对应的测试记录中
                            console.log('获取测试协作者响应信息', res)
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
                        //获取每个待审核测试的审核记录条数
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
                    //开始轮询
                    this.proceedingExp()
                }
            })
            getUserList(localStorage.getItem('uid')).then(res => {
                this.userFriends = res.data.filter(user => user.state === 1 || user.state === -1);
            })
        },
        handleAddNewExperiment() {
            if (this.newExperiment.name.trim()) {
                if (this.newExperiment.AK1 !== '' && this.newExperiment.Ak2 !== '' && this.newExperiment.DS !== '') {
                    const formData = new FormData();
                    formData.append('name', this.newExperiment.name);
                    formData.append('AK1', this.newExperiment.AK1);
                    formData.append('AK2', this.newExperiment.AK2);
                    formData.append('DS', this.newExperiment.DS);
                    formData.append('pid', this.thisProject.id)
                    formData.append('type', this.newExperiment.type)
                    // const formData={
                    //     name:this.newExperiment.name,AK1:this.newExperiment.AK1,AK2:this.newExperiment.AK2,
                    //     DS:this.newExperiment.DS,pid:this.thisProject.id,type:this.newExperiment.type
                    // }

                    addExperiment(formData).then(res => {
                        if (res.success) {
                            this.resetDialog
                            this.showDialog = false; // 关闭对话框
                            this.$message({
                                message: '添加成功',
                                type: 'success'
                            });
                            this.setExpEmpty()
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
                    message: '创建新测试各字段不能为空',
                    type: 'warning'
                });
            }
        },
        handleRemoveExperiment(index, row) {
            const deleteData = { tPid: row.id }
            if (row.configURL !== null) {
                deleteOperationFile(deleteData).then(res => {
                    if (res.success) {
                        deleteById(deleteData).then(res => {
                            if (res.success) {
                                this.afterDeleteExp(row, index)
                            }
                        })
                    }
                })
            }
            else {
                deleteById(deleteData).then(res => {
                    if (res.success) {
                        this.afterDeleteExp(row, index)
                    }
                })
            }
        },
        handleStartExperiment(index, row) {
            this.isTesting = true
            this.$message({
                message: row.id + '-' + row.name + '正在准备执行,请稍等',
                type: 'info'
            });
            this.handleGenerateConfig(row).then(result => {
                if (result) {
                    const id = { tPid: row.id }
                    startExp(id).then(res => {
                        if (res.success) {
                            this.$message({
                                message: row.id + '-' + row.name + '开始执行',
                                type: 'info'
                            });
                            this.setExpEmpty()
                        }
                    })
                }

            })
        },
        handleAssignExperiment(experiment) {
            // 保存到 LocalStorage
            localStorage.setItem('thisExperiment', JSON.stringify(experiment));
            this.$router.push("/assignment")

        },
        handleReviewExperiment(experiment) {
            localStorage.setItem('thisExperiment', JSON.stringify(experiment));
            this.$router.push("/review")
        },
        goBack() {
            this.$router.go(-1); // 返回上一个页面
        },
        resetDialog() {
            this.newExperiment.name = '',
                this.newExperiment.AK1 = null,
                this.newExperiment.AK2 = null,
                this.newExperiment.DS = null,
                this.newExperiment.type = 1
            // this.resetCodeEditor()
        },
        resetEditDialog() {
            // this.editExperiment.name = '',
            // this.editExperiment.id= '',
            // this.editExperiment.AK1 = '',
            // this.editExperiment.AK2 = '',
            // this.editExperiment.DS = ''
            this.editExperiment_name = '',
                this.editExperiment_id = '',
                this.editExperiment_AK1 = null,
                this.editExperiment_AK2 = null,
                this.editExperiment_DS = null,
                this.editExperiment_type = 1
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
            if (this.editExperiment_name.trim()) {
                if (this.editExperiment_AK1 !== null && this.editExperiment_AK2 !== null && this.editExperiment_DS !== null) {
                    const data = {
                        name: this.editExperiment_name,
                        AK1: this.editExperiment_AK1,
                        AK2: this.editExperiment_AK2,
                        DS: this.editExperiment_DS,
                        tPid: this.editExperiment_id,
                        type: this.editExperiment_type
                    }
                    console.log('修改的数据', data)
                    editExperiment(data).then(res => {
                        if (res.success) {
                            this.$message({
                                message: '修改成功',
                                type: 'success'
                            });
                            this.resetEditDialog()
                            this.editDialog = false; // 关闭对话框
                            this.setExpEmpty()
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
                    message: '测试各字段不能为空',
                    type: 'warning'
                });
            }
        },
        initialEdit(row) {
            this.editExperiment_name = row.name
            this.editExperiment_id = row.id
            this.editExperiment_type = row.type
            this.editDialog = true
        },
        handleGenerateConfig(thisTest) {
            return new Promise((resolve, reject) => {
                //基础能力测试执行前的检查
                if (thisTest.type === 1) {
                    if (thisTest.AK1 !== null && thisTest.AK2 !== null) {
                        if (thisTest.dataSet !== null) {
                            this.generateConfig(thisTest).then(result => {
                                if (result)
                                    resolve(true);
                                else
                                    reject(false)
                            })
                        }
                        else {
                            this.$message({
                                message: '用于测试的数据集被删除，请重新配置测试或重新添加数据集',
                                type: 'warning',
                                offset: 100
                            });
                            this.isTesting = false
                            reject(false);
                        }
                    }
                    else {
                        this.$message({
                            message: '用于测试或评估的大模型API key被删除，请重新配置测试或重新添加API key',
                            type: 'warning',
                            offset: 100
                        });
                        this.isTesting = false
                        reject(false);
                    }
                }
                //幻觉测试执行前的检查
                else if (thisTest.type === 2) {
                    if (thisTest.AK1 !== null) {
                        if (thisTest.dataSet !== null) {
                            this.generateConfig_hallucinationTest(thisTest).then(result => {
                                if (result)
                                    resolve(true);
                                else
                                    reject(false)
                            })
                        }
                        else {
                            this.$message({
                                message: '用于测试的数据集被删除，请重新配置测试或重新添加数据集',
                                type: 'warning',
                                offset: 100
                            });
                            this.isTesting = false
                            reject(false);
                        }
                    }
                    else {
                        this.$message({
                            message: '用于测试的大模型API key被删除，请重新配置测试或重新添加API key',
                            type: 'warning',
                            offset: 100
                        });
                        this.isTesting = false
                        reject(false);
                    }
                }
            });

        },
        generateConfig(thisTest) {
            return new Promise((resolve, reject) => {
                var AK1_callFunction = this.getCode(thisTest.AK1.id);
                var AK2_callFunction = this.getCode(thisTest.AK2.id);
                Promise.all([AK1_callFunction, AK2_callFunction]).then(values => {
                    console.log("AK1 的调用函数代码：", values[0]);
                    console.log("AK2 的调用函数代码：", values[1]);
                    if (values[0] !== null && values[1] !== null) {
                        testConnectivity(thisTest.AK1.value, values[0]).then(res => {
                            if (res.success) {
                                if (!res.result) {
                                    this.$message({
                                        message: `被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK1.name + ' ' : ''}的API key连通性出了问题，请检查网络或API key`,
                                        type: 'error'
                                    });
                                    this.isTesting = false
                                    reject(false)
                                }
                                else {
                                    testConnectivity(thisTest.AK2.value, values[1]).then(res => {
                                        if (res.success) {
                                            if (!res.result) {
                                                this.$message({
                                                    message: `评估模型 ${thisTest.AK2 && thisTest.AK2.name ? thisTest.AK2.name + ' ' : ''}的API key连通性出了问题，请检查网络或API key`,
                                                    type: 'error'
                                                });
                                                this.isTesting = false
                                                reject(false)
                                            }
                                            else {
                                                let checkData = { tPid: thisTest.id, code: values[0], className: 'new_llm1',type:1 }
                                                checkOperationFile(checkData).then(res => {
                                                    if (res.success) {
                                                        checkData = { tPid: thisTest.id, code: values[1], className: 'new_llm2',type:1}
                                                        checkOperationFile(checkData).then(res => {
                                                            if (res.success) {
                                                                generateOperationFile(thisTest.id).then(res => {
                                                                    if (res.success) {
                                                                        this.$message({
                                                                            message: '已生成新配置文件',
                                                                            type: 'success'
                                                                        });
                                                                        // this.setExpEmpty()
                                                                        this.isTesting = false
                                                                        resolve(true)
                                                                    }
                                                                    else {
                                                                        this.$message({
                                                                            message: '配置文件生成错误',
                                                                            type: 'error'
                                                                        });
                                                                        this.isTesting = false
                                                                        reject(false)
                                                                    }
                                                                })
                                                            }
                                                            else {
                                                                this.$message({
                                                                    message: `评估模型 ${thisTest.AK2 && thisTest.AK2.name ? thisTest.AK2.name + ' ' : ''}的API key调用函数编译失败，请检查语法错误`,
                                                                    type: 'error'
                                                                });
                                                                this.isTesting = false
                                                                reject(false)
                                                            }
                                                        })
                                                    }
                                                    else {
                                                        this.$message({
                                                            message: `被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK1.name + ' ' : ''}的API key调用函数编译失败，请检查语法错误`,
                                                            type: 'error'
                                                        });
                                                        this.isTesting = false
                                                        reject(false)
                                                    }
                                                })
                                            }
                                        }
                                    })
                                }
                            }
                        })
                    }
                    else {
                        if (values[0] === null && values[1] !== null) {
                            this.$confirm(`还没有编辑被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK1.name + ' ' : ''}的API key的调用函数，要进行编辑吗？`, '提示', {
                                confirmButtonText: '确定',
                                cancelButtonText: '取消',
                                type: 'warning'
                            }).then(() => {
                                this.isTesting = false
                                this.$router.push("/keyConfig")
                                reject(false)
                            }).catch(() => {
                                this.isTesting = false
                                reject(false)
                            });
                        }
                        else if (values[0] !== null && values[1] === null) {
                            this.$confirm(`还没有编辑评估模型 ${thisTest.AK2 && thisTest.AK2.name ? thisTest.AK2.name + ' ' : ''}的API key的调用函数，要进行编辑吗？`, '提示', {
                                confirmButtonText: '确定',
                                cancelButtonText: '取消',
                                type: 'warning'
                            }).then(() => {
                                this.isTesting = false
                                this.$router.push("/keyConfig")
                                reject(false)
                            }).catch(() => {
                                this.isTesting = false
                                reject(false)
                            });
                        }
                        else {
                            this.$confirm(`还没有编辑被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK2.name + ' ' : ''}和评估模型 ${thisTest.AK2 && thisTest.AK2.name ? thisTest.AK1.name + ' ' : ''}的API key的调用函数，要进行编辑吗？`, '提示', {
                                confirmButtonText: '确定',
                                cancelButtonText: '取消',
                                type: 'warning'
                            }).then(() => {
                                this.isTesting = false
                                this.$router.push("/keyConfig")
                                reject(false)
                            }).catch(() => {
                                this.isTesting = false
                                reject(false)
                            });
                        }
                    }
                })
            })
        },
        generateConfig_hallucinationTest(thisTest) {
            return new Promise((resolve, reject) => {
                var AK1_callFunction = this.getCode(thisTest.AK1.id);
                AK1_callFunction.then(value => {
                    if (value !== null) {
                        testConnectivity(thisTest.AK1.value, value).then(res => {
                            if (res.success) {
                                if (!res.result) {
                                    this.$message({
                                        message: `被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK1.name + ' ' : ''}的API key连通性出了问题，请检查网络或API key`,
                                        type: 'error'
                                    });
                                    this.isTesting = false
                                    reject(false)
                                }
                                else {
                                    let checkData = { tPid: thisTest.id, code: value, className: 'new_llm1',type:2}
                                    checkOperationFile(checkData).then(res => {
                                        if (res.success) {
                                            generateOperationFile(thisTest.id).then(res => {
                                                if (res.success) {
                                                    this.$message({
                                                        message: '已生成新配置文件',
                                                        type: 'success'
                                                    });
                                                    this.isTesting = false
                                                    resolve(true)
                                                }
                                                else {
                                                    this.$message({
                                                        message: '配置文件生成错误',
                                                        type: 'error'
                                                    });
                                                    this.isTesting = false
                                                    reject(false)
                                                }
                                            })
                                        }
                                        else {
                                            this.$message({
                                                message: `被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK1.name + ' ' : ''}的API key调用函数编译失败，请检查语法错误`,
                                                type: 'error'
                                            });
                                            this.isTesting = false
                                            reject(false)
                                        }
                                    })
                                }
                            }
                        })
                    }
                    else {
                        this.$confirm(`还没有编辑被测模型 ${thisTest.AK1 && thisTest.AK1.name ? thisTest.AK1.name + ' ' : ''}的API key的调用函数，要进行编辑吗？`, '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            this.isTesting = false
                            this.$router.push("/keyConfig")
                            reject(false)
                        }).catch(() => {
                            this.isTesting = false
                            reject(false)
                        });
                    }
                })


            })
        },
        getCode(id) {
            return getCallFunction(id).then(res => {
                return res.code
            })
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
            // 使用map而不是forEach来收集所有的promise
            const promises = this.selectFriendsId.map(id => {
                // 检查id是否在thisRowCollabortors里
                const findExistOne = this.thisRowCollaborators.find(collab => collab.id === id);
                if (!findExistOne) {
                    const data = { TPid: this.currentExpId, uid: id };
                    // 直接返回addFriendsToExperiment的调用
                    return addFriendsToExperiment(data).then(res => {
                        if (res.success) {
                            // 请求成功的处理
                            this.$message({
                                message: '加入成功',
                                type: 'success'
                            });
                        } else {
                            // 请求失败的处理（可选）
                            this.$message({
                                message: '加入失败',
                                type: 'error'
                            });
                        }
                    });
                } else {
                    // 立即resolve已经存在的id，保持promise数组的一致性
                    return Promise.resolve().then(() => {
                        this.$message({
                            message: '加入失败，' + findExistOne.name + '已经在该项目中',
                            type: 'error'
                        });
                    });
                }
            });

            // 使用Promise.all等待所有的promise完成
            Promise.all(promises).then(() => {
                // 全部完成后执行
                this.setExpEmpty();
                this.handleDialogClose();
            });
        },
        async setExpEmpty() {
            this.reviewList = [];
            this.proceeding = [];
            this.doneList = [];
            this.expList = [];

            // 如果this.load()是异步的，这里等待它完成
            await this.load();
        },
        confirmDelete(index, row) {
            this.$confirm('是否删除该测试？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.handleRemoveExperiment(index, row)
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },
        confirmStart(index, row) {
            this.$confirm('确定执行该测试吗？一旦执行将直至结束', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.handleStartExperiment(index, row)
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消执行'
                });
            });
        },
        proceedingExp() {
            this.interval = setInterval(() => {
                // 如果 this.proceeding 为空，则停止轮询

                if (!this.proceeding.length) {
                    clearInterval(this.interval);
                    return;
                }
                // if (this.currentTab !== '正在测试') {
                //     clearInterval(this.interval);
                //     return;
                // }

                // 遍历 this.proceeding 中的每个测试
                this.proceeding.forEach((experiment, index) => {
                    getExperimentProgress(experiment.id).then(res => {
                        if (res.success) {
                            if (localStorage.getItem(experiment.id + 'errorTimes') !== null) {
                                localStorage.removeItem(experiment.id + 'errorTimes')
                            }
                            this.proceeding[index].progress = res.process
                            if (this.proceeding[index].progress === 100) {
                                // 更新测试状态
                                const updateExp = { TPid: experiment.id, uid: localStorage.getItem('uid') }
                                updateExperimentStatus(updateExp).then(res => {
                                    if (res.success) {
                                        this.$message({
                                            type: 'info',
                                            message: experiment.id + '-' + experiment.name + '执行完成'
                                        });
                                        // 停止当前轮询
                                        clearInterval(this.interval);
                                        this.setExpEmpty()
                                    }
                                });
                            }
                        }
                        else {
                            if (localStorage.getItem(experiment.id + 'errorTimes') !== null) {
                                let value = localStorage.getItem(experiment.id + 'errorTimes');
                                value = Number(value);
                                value++;
                                localStorage.setItem(experiment.id + 'errorTimes', value.toString());
                            }
                            else {
                                localStorage.setItem(experiment.id + 'errorTimes', '1')
                            }
                            if (Number(localStorage.getItem(experiment.id + 'errorTimes')) >= 5) {
                                errorHandle(experiment.id).then(res => {
                                    if (res.success) {
                                        this.$message({
                                            type: 'error',
                                            message: experiment.id + '-' + experiment.name + '获取进度失败，请检查测试配置再重新开始测试'
                                        });
                                        clearInterval(this.interval);
                                        this.setExpEmpty()
                                        localStorage.removeItem(experiment.id + 'errorTimes')
                                    }
                                })
                            }
                        }
                    })
                });
            }, 10000); // 设置轮询间隔为 10 秒
        },
        // proceedingExp() {
        //     const interval = setInterval(() => {
        //         // 如果 this.proceeding 为空，则停止轮询
        //         if (!this.proceeding.length) {
        //             clearInterval(interval);
        //             return;
        //         }

        //         // 遍历 this.proceeding 中的每个测试
        //         this.proceeding.forEach((experiment, index) => {

        //             this.proceeding[index].progress = this.proceeding[index].progress + 1


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
            localStorage.setItem('currentTab', this.currentTab)
            // if (this.currentTab === '正在测试') {
            //     if (this.interval) {
            //         clearInterval(this.interval)
            //     }
            //     this.proceedingExp()
            // }
        },
        afterDeleteExp(row, index) {
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
        },
        handleUpdate(row) {
            this.$message({
                type: 'info',
                message: row.id + '-' + row.name + '正在更新测试报告，请稍后'
            });
            this.isUpdate = true
            updateReport(row.id).then(res => {
                if (res.success) {
                    this.$message({
                        type: 'success',
                        message: row.id + '-' + row.name + '测试报告更新成功'
                    });
                }
                this.isUpdate = false
            })
        },
        handleDownload(row) {
            getReportNum(row.id).then(res => {
                this.reportCount = res.count
                this.initDownLoadTable()
            })
            this.currentExpId = row.id
            this.currentExpName = row.name
            this.currentExpStatus = row.status
            this.downloader = true
        },
        downloadClose() {
            this.downloader = false
        },
        confirmDownload(selectVersion) {
            genReport(this.currentExpId, selectVersion).then(res => {
                if (res.success) {
                    this.$message({
                        type: 'success',
                        message: this.currentExpId + '-' + this.currentExpName + '正在下载该测试的测试报告'
                    });
                    //处理下载链接
                    let downloadUrl = res.url;
                    downloadUrl = downloadUrl.replace(/\\/g, '/');
                    downloadUrl = downloadUrl.replace(/App/g, '');
                    downloadUrl = config.API_URL + downloadUrl;
                    console.log('下载链接', downloadUrl)

                    //获取到文件名
                    const urlParts = downloadUrl.split('/');
                    const filename = urlParts[urlParts.length - 1];

                    fetch(downloadUrl)
                        .then(response => response.blob())
                        .then(blob => {
                            const url = window.URL.createObjectURL(new Blob([blob]));
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                            document.body.removeChild(a);
                        });
                }
            })
        },
        initDownLoadTable() {
            this.downLoadTable = Array.from({ length: this.reportCount }, (_, i) => ({
                index: i + 1, // 生成从1开始的行数
            }));
        },
        handleInteraction(experiment) {
            localStorage.setItem('thisExperiment', JSON.stringify(experiment));
            this.$router.push("/interaction")
        },
    }
};

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

.down-load {
    /* background-image: linear-gradient(to right, #4facfe, #00f2fe); Gradient background */
    border-color: dodgerblue;
    /* Removes the border */
    border-width: 3px;
}
</style>