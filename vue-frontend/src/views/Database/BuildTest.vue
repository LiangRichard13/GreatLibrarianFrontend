<template>
  <div>
    <h3 style="letter-spacing: 1px;font-weight: 400;padding-bottom: 20px;text-align: center">测试集构建</h3>
    <el-steps :active="active" finish-status="success" align-center>
      <el-step title="步骤 1" description="设定抽取数据数量并选择数据抽取方式"></el-step>
      <el-step title="步骤 2" description="选择数据配比"></el-step>
      <el-step title="步骤 3" description="进行数据检索与抽取" process-status="wait"></el-step>
      <el-step title="步骤 4" description="构建测试集" process-status="wait"></el-step>
      <!-- <el-step title="步骤 5" description="测试集构建完成" process-status="success"></el-step> -->
    </el-steps>
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: start; height: 100vh;">
      <div style="width: 30%; margin-top: 20px;">
        <el-form ref="form" label-width="150px" v-loading="submitLoading">
          <!-- 设定抽取的数据数量 -->
          <el-form-item label="设定抽取数据数量">
            <el-tooltip placement="right" effect="dark" content="抽取总数范围为100~10000">
              <el-input-number @change="showCaseNumber()" v-model="total_case_number" :min="100" :max="10000"
                label="设定数据数量"></el-input-number>
            </el-tooltip>
          </el-form-item>
          <!-- 选择数据的抽取方式 -->
          <el-form-item label="选择数据抽取方式">
            <el-select v-model="choose_type" placeholder="选择数据抽取方式">
              <el-option label="按数据集抽取" value="resource"></el-option>
              <el-option label="按测试维度抽取" value="test_dimension"></el-option>
            </el-select>
          </el-form-item>

          <!-- 数据集抽取项 -->
          <div v-if="choose_type === 'resource'">
            <div v-for="(item, index) in composition" :key="index">
              <el-form-item :label="'数据集抽取项' + (index + 1)">
                <el-select v-model="item.resource_name" placeholder="数据来源">
                  <el-option v-for="option in resource_options" :key="option.value" :label="option.label"
                    :value="option.value">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-tooltip placement="right" effect="dark">
                  <div slot="content">数量范围为0~{{ getMaxCaseNumber(index) }}</div>
                  <el-input-number @change="updateCaseNumbers()" v-model="item.case_number" :min="0"
                    :max="getMaxCaseNumber(index)" :label="'设定数据数量' + (index + 1)">
                  </el-input-number>
                </el-tooltip>
              </el-form-item>
            </div>
            <!-- <p>剩余可分配的数量：{{ remainingCaseNumber }}</p> -->
            <el-form-item>剩余可分配的数量：<el-tag type="warning">{{ remainingCaseNumber }}</el-tag></el-form-item>
          </div>

          <!-- 测试维度抽取项 -->
          <div v-if="choose_type === 'test_dimension'">
            <div v-for="(item, index) in composition" :key="index">
              <el-form-item :label="'测试维度抽取项' + (index + 1)">
                <el-select v-model="item.test_dimension_name" placeholder="数据来源">
                  <el-option v-for="option in test_demension_options" :key="option.value" :label="option.label"
                    :value="option.value">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-tooltip placement="right" effect="dark">
                  <div slot="content">数量范围为0~{{ getMaxCaseNumber(index) }}</div>
                  <el-input-number @change="updateCaseNumbers()" v-model="item.case_number" :min="0"
                    :max="getMaxCaseNumber(index)" :label="'设定数据数量' + (index + 1)">
                  </el-input-number>
                </el-tooltip>
              </el-form-item>
            </div>
            <el-form-item>剩余可分配的数量：<el-tag type="warning">{{ remainingCaseNumber }}</el-tag></el-form-item>
          </div>

          <!-- 增加、减少抽取项 -->
          <div v-if="choose_type">
            <el-form-item label="增加/减少抽取项数量">
              <el-button-group>
                <el-button plain type="primary" icon="el-icon-plus" @click="item_number_change(1)">增加抽取项</el-button>
                <el-button plain type="primary" icon="el-icon-minus" @click="item_number_change(0)">减少抽取项</el-button>
              </el-button-group>
            </el-form-item>
            <el-form-item>
              <el-button plain type="success" style="margin-top: 10px" @click="confirmSubmit()">确认</el-button>
            </el-form-item>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { buildTest } from "@/api/dataList"
import JSZip from "jszip";

export default {
  name: "BuildTest",
  data() {
    return {
      active: 0,
      choose_type: null,
      // item_number: 1,
      total_case_number: 100,
      remainingCaseNumber: 100,
      composition: [],
      resource_options: [
        { value: 'C-Eval', label: 'C-Eval' },
        { value: 'CMMLU', label: 'CMMLU' },
        { value: 'https://github.com/cambridgeltl/visual-spatial-reasoning', label: 'Visual-Spatial Reasoning' },
        { value: 'https://huggingface.co/datasets/SakanaAI/JA-VG-VQA-500', label: 'JA-VG-VQA-500' },
        { value: 'https://huggingface.co/datasets/lmms-lab/TempCompass', label: 'TempCompass' },
        { value: 'https://huggingface.co/datasets/terryoo/TableVQA-Bench', label: 'TableVQA' },
        { value: 'https://textvqa.org/dataset/', label: 'TextVQA' },
        { value: 'https://www.youtube.com/', label: 'YouTuBe' },
        { value: '自筹', label: '自筹' },
        { value: 'HalluQA', label: 'HalluQA' },

      ],
      test_demension_options: [
        { value: '常识推理', label: '常识推理' },
        { value: '逻辑推理', label: '逻辑推理' },
        { value: '数学推理', label: '数学推理' },
        { value: '文本问答', label: '文本问答' },
        { value: '信息抽取', label: '信息抽取' },
        { value: '因果推理', label: '因果推理' },
        { value: '摘要总结', label: '摘要总结' },
        { value: '长文本理解', label: '长文本理解' },
        { value: '知识与常识', label: '知识与常识' },
        { value: '专业知识', label: '专业知识' },
        { value: '视觉空间关系', label: '视觉空间关系' },
        { value: '视觉语言推理', label: '视觉语言推理' },
        { value: '视觉蕴含', label: '视觉蕴含' },
        { value: '视频检索', label: '视频检索' },
        { value: '图表推理', label: '图表推理' },
        { value: '图片问答', label: '图片问答' },
        { value: '有声视频问答', label: '有声视频问答' },
        { value: '幻觉', label: '幻觉' },
        { value: '鲁棒性', label: '鲁棒性' },
        { value: '公平性', label: '公平性' },
        { value: '安全性', label: '安全性' }
      ],
      submitLoading: false,
      build_data:[]
    }
  },
  // mounted() {
  // },
  watch: {
    choose_type(newValue) {
      if (newValue === "resource" || newValue === "test_dimension") {
        // if (this.active === 0)
          this.active=1 // 如果选择的是 resource 或 test_dimension，activate++
        if (newValue === "resource")
          this.composition.push({ resource_name: null, case_number: 0 });
        else if (newValue === "test_dimension")
          this.composition.push({ test_dimension_name: null, case_number: 0 });
      }
    }
  },
  methods:
  {
    item_number_change(option) {
      if (option) {
        if (this.composition.length < 11) {
          if (this.choose_type === "resource")
            this.composition.push({ resource_name: null, case_number: 0 });
          else if (this.choose_type === "test_dimension")
            this.composition.push({ test_dimension_name: null, case_number: 0 });
        }
        else {
          this.$message({
            type: 'warning',
            message: '抽取项数量不能大于10'
          });
        }
      }
      else {
        if (this.composition.length > 1) {
          this.composition.pop();
          this.updateCaseNumbers()
        }
        else {
          this.$message({
            type: 'warning',
            message: '抽取项数量不能小于1'
          });
        }
      }
    },
    showCaseNumber() {
      this.updateCaseNumbers()
      this.$message({
        type: 'info',
        message: "当前设定抽取用例总数:" + this.total_case_number
      });
    },
    updateCaseNumbers() {
      // 计算剩余的 case_number
      const totalAllocated = this.composition.reduce((sum, item) => sum + item.case_number, 0);
      this.remainingCaseNumber = this.total_case_number - totalAllocated;
    },
    getMaxCaseNumber(index) {
      // 动态计算每个输入框的最大值，确保总和不超过 total_case_number
      const totalAllocated = this.composition.reduce((sum, item, idx) => idx === index ? sum : sum + item.case_number, 0);
      return this.total_case_number - totalAllocated;
    },
    confirmSubmit() {
      this.$confirm('即将进行测试集构建', '提示', {
        confirmButtonText: '继续',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.handleSubmit()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消执行'
        });
      });
    },
    handleSubmit() {
      // 检查resource_name或者test_dimension_name是否为空
      if (this.checkNull()) {
        this.$message({
          type: 'warning',
          message: '还有未选择数据来源的抽取项'
        });
        return
      }
      // 检查是否还有未分配完的用例数
      if (this.remainingCaseNumber > 0) {
        this.$message({
          type: 'warning',
          message: '还有未分配完的用例数量'
        });
        return
      }
      //将case_number为0的抽取项删除
      this.composition = this.composition.filter(item => item.case_number !== 0);
      //发送请求
      this.submitAndget()
    },
    checkNull() {
      if (this.choose_type === 'resource') {
        return this.composition.some(item => item.resource_name === null);
      }
      else if (this.choose_type === 'test_dimension') {
        return this.composition.some(item => item.test_dimension_name === null);
      }
    },
    submitAndget() {
      if (this.active === 1)
        this.active++
      this.submitLoading = true
      const sendData = { choose_type: this.choose_type, composition: this.composition }
      buildTest(sendData).then(res => {
        if (res.success) {
          if (!res.data.length) { 
            // 成功响应但没有任何数据返回
            this.$message({
              type: 'warning',
              message: '未检索出任何数据，请重新筛选'
            });
            this.submitLoading = false
            this.active = 1
            return
          }
          else{
          // 成功响应且有数据返回
            if(this.active===2)
            this.active++
          this.build_data=res.data
          this.exportZip()
          }
        }
        else {
          // 响应失败
          this.submitLoading = false
          this.active = 1
        }
      })
      // console.log(sendData)
    },
    processBuildData() {
      return this.build_data.map(input_data => {
        let prompt_array = [];
        let answers_array = [];

        input_data.data.forEach((data) => {
          let prompt 
          if(data.file_url)
        {
            prompt = {
            file_url: data.file_url,
            text: data.question
          };
        }
        else
        { 
          prompt=data.question
        }
          prompt_array.push(prompt);
          answers_array.push(data.keywords);
        });

        let template = {
          name: "Name of this dataset",
          description: "Description of this dataset",
          field: input_data.field,
          prompts: prompt_array,
          evaluation: {}
        };

        answers_array.forEach((keywords, i) => {
          template["evaluation"][i] = [
            {
              keywords: [keywords]  // 确保 keywords 是二维数组
            }
          ];
        });
        return template;
      });
    },
    exportZip() {
      const zip = new JSZip();
      const processedData = this.processBuildData();

      // 为每个template生成一个单独的JSON文件，并用field字段命名
      processedData.forEach((template) => {
        const jsonData = JSON.stringify(template, null, 2);
        const fileName = `${template.field}.json`; // 使用 field 字段作为文件名
        zip.file(fileName, jsonData);  // 将文件添加到压缩包中
      });
      // 生成压缩包并触发下载
      zip.generateAsync({ type: "blob" }).then(content => {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(content);
        link.download = "datasets.zip";  // 压缩包的名称
        link.click();
        if(this.active===3)
        this.active++
        this.choose_type=null
        this.total_case_number=100
        this.submitLoading=false
        // 释放内存
        URL.revokeObjectURL(link.href);
      });
    }
  },
}
</script>

<style scoped></style>