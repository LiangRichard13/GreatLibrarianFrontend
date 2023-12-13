<template>
    <div class="main">
      <el-page-header @back="goBack" content="实验列表">
      </el-page-header>
      <div class="content">
        <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
          {{ this.thisExperiment.id }}-{{ this.thisExperiment.name }} 实验的QA记录
        </h3>
      </div>
      <div class="table-container">
        <el-table :data="QAList" style="width: 100%" ref="multipleTable" tooltip-effect="dark"
          @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55">
          </el-table-column>
          <el-table-column label="QA ID" prop="id"></el-table-column>
          <el-table-column label="问题" prop="question"></el-table-column>
  
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="回答:">
                  <span>{{ props.row.answer }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
  
        </el-table>
        <div style="margin-top: 20px">
          <el-button @click="toggleSelection()">取消选择</el-button>
        </div>
      </div>
      <div class="button-container" style="text-align: right; margin-top: 20px;">
        <el-button type="primary" @click="showDialog=true">分发给协作者</el-button>
        <el-button type="warning" @click="handleReview(thisExperiment,thisProject)">审核实验记录</el-button>
      </div>
  
      <!-- 添加API_KEY的对话框 -->
      <el-dialog title="选择分发协作者" :visible.sync="showDialog" width="30%" @close="resetDialog">
  
        <div>
          <el-form ref="form"  label-width="100px">
  
            <el-form-item label="选择协作者">
              <el-select v-model="distributeUserId" placeholder="请选择">
                <el-option v-for="item in thisProject.collaborators" :key="item.id" :label="`${item.id} - ${item.name}`"
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
  
    </div>
  </template>
     
  <script>
  import { getQAByExpirenceId, distributeToOthers } from '@/api/qa'
  export default {
    name: "AssignmentQA",
    data() {
      return {
        showDialog: false,
        QAList: [{ id: '1', question: '世界上最高的峰是哪个峰 ?', answer: '世界上最高的山峰是珠穆朗玛峰（Mount Everest），它位于喜马拉雅山脉，跨越尼泊尔和中国（西藏）的边界。珠穆朗玛峰的海拔高度是8,848.86米（29,031.7英尺），这使它成为地球上海拔最高的山峰。这座山峰也是登山者们梦寐以求的挑战之一，但攀登它极具挑战性，需要极高的技术和体能。每年都有登山者前往珠穆朗玛峰尝试征服它，但也伴随着危险和挑战。',rate:0 }
                ],
        thisExperiment: {},
        thisProject:{},
        selectedIds: [],
        distributeUserId: '',
      }
    },
    mounted() {
      this.thisExperiment = this.$route.query.experiment,
      this.thisProject=this.$route.query.project
      // this.load()
    },
    methods: {
      load() {
        getQAByExpirenceId(this.thisExperiment.id, localStorage.getItem('uid')).then(res => {
          this.QAList = res.data
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
        this.selectedIds = selectedRows.map(row => row.id);
      },
      distributeToCollaborators() {
        const data = {
            uid:this.distributeUserId,
            distributeIds:this.selectedIds
        }
        distributeToOthers(data).then(res => {
          if (res.success) {
            this.resetDialog
            this.showDialog=false
            this.$message({
              message: '分发成功！',
              type: 'success'
            });
            this.load()
          }
        })
      },
      resetDialog() {
        this.distributeUserId = ''
      },
      handleReview(experiment,project){
        this.$router.push({ path: `/review`,query:{experiment,project}});
      }
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