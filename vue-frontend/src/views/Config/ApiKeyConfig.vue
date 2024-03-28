<template>
  <div class="main">

    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">API_KEY配置</h3>

    <div style="display: flex; justify-content: flex-end; padding-bottom: 20px;">
      <el-button
          icon="el-icon-circle-plus"
          type="success"
          @click="showDialog=true">添加API_KEY
      </el-button>
    </div>

    <div class="table-container">
      <el-table :data="apiKeys" style="width: 100%">
        <!-- <el-table-column prop="id" label="API_KEY ID"></el-table-column> -->
        <el-table-column prop="name" label="接口"></el-table-column>
        <el-table-column prop="value" label="内容"></el-table-column>
        <!-- <el-table-column prop="intro" label="介绍"></el-table-column> -->
        <el-table-column type="expand" label="介绍">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="介绍:">
                <span>{{ props.row.intro }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>


        <!-- 操作列 -->
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-popconfirm
                confirm-button-text="确定"
                cancel-button-text="不用了"
                icon="el-icon-info"
                icon-color="red"
                @confirm="removeKey(scope.$index, scope.row)"
                title="确定要删除此API_KEY吗?"
            >
              <el-button
                  style="margin-left: 8px"
                  size="mini"
                  icon="el-icon-delete"
                  type="danger"
                  slot="reference">删除
              </el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加API_KEY的对话框 -->
    <el-dialog
        title="添加 API Key"
        :visible.sync="showDialog"
        width="30%"
        @close="resetDialog">
      <div>
        <el-form ref="form" :model="newApiKey" label-width="100px">

          <el-form-item label="接口来源">
            <el-input v-model="newApiKey.name"></el-input>
          </el-form-item>

          <el-form-item label="KEY内容">
            <el-input v-model="newApiKey.value"></el-input>
          </el-form-item>

            <el-form-item label="LLM介绍">
            <el-input v-model="newApiKey.intro"></el-input>
          </el-form-item>
        </el-form>


      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="addKey">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>


<script>
import {addApiKey, deleteById, findApiKeyByUserId} from "@/api/apiConfig";

export default {
  name: "ApiConfig",
  data() {
    return {
      apiKeys: [
        {id:'4f658b0e',name:'qwen_turbo',value:'sk-9ca2ad73e7d34bd4903eedd6fc70d0d8',intro:'通义千问是一个由阿里云开发的AI助手。它使用了最新的自然语言处理技术，包括深度学习和神经网络模型，能够理解和生成高质量的自然语言文本。\n\n通义千问的功能非常强大。它可以回答各种问题，包括但不限于科学、历史、文化、娱乐等领域的问题。此外，它还可以提供新闻摘要、天气预报、菜谱推荐等各种实用信息。除了回答问题外，通义千问还可以进行对话和聊天，帮助用户排解无聊和孤独。\n\n通义千问的设计理念是“以用户为中心”。它的目标是为用户提供最准确、最有用的信息，并且在与用户的交互中不断学习和改进。通义千问采用了先进的机器学习算法，可以根据用户的反馈和行为数据调整自己的模型和策略，从而更好地满足用户的需求。\n\n总的来说，通义千问是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。'},
        {id:'76478a99',name:'chatglm',value:'f118b48f5559e4e3ccdd3a5c30712aef.c5uSVYS1k4PGoNGC',intro:'ChatGLMpro 是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。\n\nChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。\n\n相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。总的来说，chatglm是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。\n\n'},
      ],
        showDialog: false,
      newApiKey: {name: '', value: '',intro:''}
    }
  },
  mounted() {
    // this.load()
  },
  methods:
      {
        load() {
          if (localStorage.getItem("uid") !== null) {
            const id = localStorage.getItem("uid")
            findApiKeyByUserId(id).then(res => {
              this.apiKeys = res.data;
            })
          }
        },
        addKey() {
          if (this.newApiKey.value.trim() && this.newApiKey.name.trim()) {
            const data = {
              uid:localStorage.getItem('uid'),
              name: this.newApiKey.name,
              value: this.newApiKey.value,
              intro:this.newApiKey.intro
            }
            addApiKey(data).then(res => {
              if (res.success) {
                this.newApiKey.name = '';
                this.newApiKey.value = ''; // 清空输入框
                this.newApiKey.intro='';
                this.showDialog = false; // 关闭对话框
                this.$message({
                  message: '添加成功',
                  type: 'success'
                });
                this.load()
              }
            })
          } else {
            this.$message({
              message: '添加API_KEY各字段不能为空',
              type: 'warning'
            });
          }
        },
        removeKey(index, row) {
          const deleteId={id:row.id}
          deleteById(deleteId).then(res => {
            if (res.success) {
              this.apiKeys.splice(index, 1);
              this.$message({
                message: '删除成功',
                type: 'success',
              });
            }
          })
        },
        resetDialog() {
          this.newApiKey.name = '';
          this.newApiKey.value = '';// 重置输入
          this.newApiKey.intro='';
        },
      }
}


</script>

<style scoped>
.table-container {
  max-width: 2000px; /* 设置你希望的最大宽度 */
  margin: auto; /* 这将使得表格居中 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 可选：添加阴影效果 */
  padding: 20px; /* 可选：添加一些内边距 */
  border: 1px solid #ebeef5;
}

.main {
  padding: 20px;
}
</style>