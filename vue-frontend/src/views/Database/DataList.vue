<template>
    <el-container style="height: 100vh; display: flex; justify-content:center">
        <el-container>
            <!-- 主体部分 -->
            <el-main>
                <!-- 用例筛选器 -->
                <el-row style="margin-top: 20px;">
                    <el-col :span="23">
                        <el-card shadow="hover" class="box-card">
                            <div slot="header" class="clearfix">
                                <span style="float: left;">
                                    <h4>用例筛选</h4>
                                </span>
                            </div>
                            <div style="display: flex; justify-content:flex-start;margin-top: 20px">
                                <el-select v-model="resource" placeholder="数据来源">
                                    <el-option v-for="item in resource_options" :key="item.value" :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>

                                <el-select v-model="test_dimension" placeholder="测试维度">
                                    <el-option v-for="item in test_dimension_options" :key="item.value"
                                        :label="item.label" :value="item.value">
                                    </el-option>
                                </el-select>

                                <el-select v-model="data_type_input" placeholder="输入数据类型">
                                    <el-option v-for="item in data_type_options" :key="item.value" :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>

                                <el-select v-model="data_type_output" placeholder="输出数据类型">
                                    <el-option v-for="item in data_type_options" :key="item.value" :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                                <el-button plain type="primary" @click="handleSearch()"
                                    style="width: 150px;">检索</el-button>
                                <el-button plain type="danger" @click="hanedleClear()"
                                    style="width: 150px;">清除</el-button>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <!-- 用例展示表 -->
                <div v-if="filterdata.length" v-loading="loading">
                    <el-card shadow="hover" class="box-card" style="margin-top: 20px;height: 800px">
                        <div slot="header" class="clearfix">
                            <span style="float: left;">
                                <h4>用例表</h4>
                            </span>
                        </div>
                        <el-table :data="filterdata">
                            <el-table-column label="问题" prop="question"></el-table-column>
                            <el-table-column label="回答" prop="answer"></el-table-column>
                            <el-table-column label="文件">
                                <template slot-scope="scope">
                                    <!-- 判断文件类型是图片还是视频 -->
                                    <div v-if="isImage(scope.row.file_url)">
                                        <img :src="scope.row.file_url" style="width: 100px; height: 100px;" />
                                    </div>
                                    <div v-else-if="isVideo(scope.row.file_url)">
                                        <video controls style="width: 200px; height: 150px;">
                                            <source :src="scope.row.file_url" type="video/mp4" />
                                            您的浏览器不支持视频标签。
                                        </video>
                                    </div>
                                    <div v-else>
                                        <el-tag type="info">无</el-tag>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column label="详情" type="expand">
                                <template slot-scope="scope">
                                    <div>
                                        <el-form label-position="left" class="table-expand">
                                            <el-form-item label="回答模式:">
                                                <el-tag v-if="scope.row.answer_mode === 'level1'">开放问答</el-tag>
                                                <el-tag v-else-if="scope.row.answer_mode === 'level2'">命题问答</el-tag>
                                                <el-tag type="info" v-else>无</el-tag>
                                            </el-form-item>
                                            <el-form-item label="更新版本:">
                                                <span>{{ scope.row.version_update.update_time }}</span>
                                            </el-form-item>
                                            <el-form-item label="更新时间:">
                                                <span>{{ scope.row.version_update.version }}</span>
                                            </el-form-item>
                                            <el-form-item label="创建者:">
                                                <span>{{ scope.row.uploader }}</span>
                                            </el-form-item>
                                            <el-form-item label="创建时间:">
                                                <span>{{ scope.row.date_note }}</span>
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-card>
                </div>
                <!-- 静态展示数据集用例 -->
                <div v-else>
                    <el-row>
                        <el-col :span="11">
                            <!-- C-EVAL -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height: 900px;">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">C-EVAL</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>超过13,000道中文考试题</li>
                                        <li><strong>类别：</strong>半结构化数据生成、代码生成、公平性、幻觉、机器翻译、鲁棒性、文本改写、常识推理、任务分解、知识与常识、合规性、摘要总结、命名实体识别、因果推理、长文本理解、代码理解、逻辑推理、数学推理、文本问答、信息抽取、专业知识</li>
                                        <li><strong>版本：</strong>2023年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span
                                                style="color: #6D6D6D;">以下是一道单项选择题，请你直接给出正确的选项，不要提及你认为的错误选项。以下是问题：税务行政复议的申请人可以在得知税务机关作出具体行政行为之日起____日内提出行政复议申请。
                                                A.60 B.30 C.7 D.3 答案：。</span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">A</span>
                                        </div>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span
                                                style="color: #6D6D6D;">以下是一道单项选择题，请你直接给出正确的选项，不要提及你认为的错误选项。以下是问题：有三个直径相同的金属小球，小球1和2带等量同号电荷，两者的距离远大于小球直径，相互作用力为F。小球3不带电，装有绝缘手柄．用小球3先和小球1碰一下，接着又和小球2碰一下，然后移去。则此时小球1和2之间的相互作用力为____。
                                                A.F/4 B.3F/8 C.F/2 D.3F/4 答案：。</span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">B</span>
                                        </div>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span
                                                style="color: #6D6D6D;">以下是一道单项选择题，请你直接给出正确的选项，不要提及你认为的错误选项。以下是问题：事物的质是指____。
                                                A.构成事物内在要素的总和 B.组成事物基本要素的内在联系 C.一事物区别与其他事物的内在规定性 D.事物的规模、发展程度和速度等规定性
                                                答案：。</span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">D</span>
                                        </div>
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                        <el-col :span="11">
                            <!-- CMMLU -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height: 900px;">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">CMMLU</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>超过12,000道中文多学科、多领域的测试题</li>
                                        <li><strong>类别：</strong>半结构化数据生成、代码生成、公平性、幻觉、机器翻译、鲁棒性、文本改写、常识推理、任务分解、知识与常识、合规性、摘要总结、命名实体识别、因果推理、长文本理解、代码理解、逻辑推理、数学推理、文本问答、信息抽取、专业知识</li>
                                        <li><strong>版本：</strong>2022年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span
                                                style="color: #6D6D6D;">以下是一道单项选择题，请你直接给出正确的选项，不要提及你认为的错误选项。以下是问题：某周的日均温分别为9°C、9°C、11°C、12°C、13°C、15°C、16°C，则对喜温作物(生物学零度为10°C)来说，这周的活动的积温为。
                                                A.67°C B.18°C C.85°C D.17°C 答案：。</span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">A</span>
                                        </div>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span
                                                style="color: #6D6D6D;">以下是一道单项选择题，请你直接给出正确的选项，不要提及你认为的错误选项。以下是问题：“心诚则灵，心不诚则不灵”的说法是。
                                                A.认为世界是绝对精神外化的客观唯心主义观点 B.主张物质和意识具有统一性的辩证唯物主义观点 C.夸大了意识能动作用的唯心主义观点
                                                D.主张思想就是物质的庸俗唯物主义观点 答案：。</span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">C</span>
                                        </div>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span
                                                style="color: #6D6D6D;">以下是一道单项选择题，请你直接给出正确的选项，不要提及你认为的错误选项。以下是问题：下⾯⼏何体中，过轴的截⾯⼀定是圆⾯的是。
                                                A.圆台 B.圆柱 C.圆锥 D.球 答案：。</span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">D</span>
                                        </div>
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                    <el-row style="display: flex;">
                        <el-col :span="11">
                            <!-- IMGE-NET -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height:1500px">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">IMAGE-NET</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>14,197,122张图像</li>
                                        <li><strong>类别：</strong>图片分类</li>
                                        <li><strong>版本：</strong>2021年度更新版</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">请判断图片中的内容是属于以上类别中的哪种，只需要回答类别所对应的数字序号，不需要做其他解释。
                                                0:analog clock
                                                1: backpack, back pack, knapsack, packsack, rucksack, haversack
                                                2: ballpoint, ballpoint pen, ballpen, Biro
                                                3: Band Aid
                                                4: barbell
                                                5: barber chair
                                                6: beer bottle
                                                7: beer glass
                                                ......
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">3</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/bandAid.jpg')"
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                    </div>
                                </div>
                            </el-card>
                        </el-col>

                        <el-col :span="11">
                            <!-- TextVQA -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height: 1500px">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">TextVQA</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>45,336张图像及相应的93,000个问题</li>
                                        <li><strong>类别：</strong>图片问答</li>
                                        <li><strong>版本：</strong>2019年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">what page is the alphabet listed on?
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">page 31</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/page31.jpg')"
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">what did the passengers in this comic avoid?
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">a cold</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/comic.jpg')"
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>

                    <el-row>
                        <el-col :span="11">
                            <!-- TableVQA -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height:1200px">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">TableVQA</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>超过18,000张包含表格的图像及相应的问答对</li>
                                        <li><strong>类别：</strong>图表推理</li>
                                        <li><strong>版本：</strong>2020年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">how many players attended wake forest
                                                university before being
                                                drafted?
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">2</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/player.jpg')"
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">what is the last type of vessel listed?
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">Lightship</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/lasttype.jpg')"
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                        <el-col :span="11">
                            <!-- Visual-Spatial Reasoning -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height:1200px">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">Visual-Spatial Reasoning</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>超过12,000张图像及相应的空间推理问题</li>
                                        <li><strong>类别：</strong>视觉空间关系</li>
                                        <li><strong>版本：</strong>2020年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">Please judge whether the following description
                                                is consistent
                                                with the spatial relationship of the objects in the picture. If it is
                                                consistent, please
                                                just answer: True. If it is not consistent, please just answer: False.
                                                No other
                                                explanation is required.Description:The sandwich is at the side of the
                                                dining table.
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">True</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/sandwich.jpg')"
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="11">
                            <!-- 视频检索和视频问答 -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height:2000px">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">TempCompass</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>超过50,000条时间序列相关的数据记录，包含视频测试数据</li>
                                        <li><strong>类别：</strong>视频问答、视频检索</li>
                                        <li><strong>版本：</strong>2022年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">Please complete the following multiple-choice
                                                questions based
                                                on the video. Please give the correct option directly and do not mention
                                                the wrong
                                                option you think:What is the man doing in the video?A. dunking a
                                                basketballB.
                                                dribbling a basketballC. passing a basketball.
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">C. dunking a basketball</span>
                                        </div>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">Please complete the following multiple-choice
                                                questions based
                                                on the video. Please give the correct option directly and do not mention
                                                the wrong
                                                option you think:Which description is a more suitable match for the
                                                video?Option 1:
                                                The man is dribbling a basketball.Option 2: A man is dunking a
                                                basketball.
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">Option 2: A man is dunking a
                                                basketball.</span>
                                        </div>
                                        <video controls
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                            <source :src="require('@/assets/data_list_video/dunking.mp4')"
                                                type="video/mp4">
                                            您的浏览器不支持视频标签。
                                        </video>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">Please complete the following multiple-choice questions based on the video. Please give the correct option directly and do not mention the wrong option you think:In what order did the man do the activities?A. showing off his car key, pulling back inside the carB. pulling back inside the car, showing off his car keyC. throwing away his car key, pulling back inside the carD. pulling back inside the car, throwing away his car key.
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">A. showing off his car key, pulling back inside the car.</span>
                                        </div>
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">Please complete the following multiple-choice questions based on the video. Please give the correct option directly and do not mention the wrong option you think:Which description is a more suitable match for the video?Option 1: The correct order of actions by the man is throwing away his car key, then pulling back inside the car.Option 2: The man first shows off his car key, then pulls back inside the car.
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">Option 2: The man first shows off his car key, then pulls back inside the car.</span>
                                        </div>
                                        <video controls
                                            style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                            <source :src="require('@/assets/data_list_video/carandman.mp4')"
                                                type="video/mp4">
                                            您的浏览器不支持视频标签。
                                        </video>
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                        <el-col :span="11">
                            <!-- 视觉语言推理和视觉蕴含 -->
                            <el-card shadow="hover" class="light-purple"
                                style="margin-top: 20px; border-radius: 12px; padding: 20px;height:2000px">
                                <!-- Card Header -->
                                <div slot="header" class="clearfix"
                                    style="border-bottom: 2px solid #E0E0E0; padding-bottom: 10px;">
                                    <span style="float: left;">
                                        <h3 style="font-size: 24px; color: #4A4A4A;">JA-VG-VQA-500</h3>
                                    </span>
                                </div>

                                <!-- Dataset Basic Information Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">基本信息</h4>
                                    <ul style="list-style-type: none; padding: 0; color: #6D6D6D; line-height: 1.8;">
                                        <li><strong>大小：</strong>500张图像及相应的问答对</li>
                                        <li><strong>类别：</strong>视觉语言推理、视觉蕴含</li>
                                        <li><strong>版本：</strong>2021年发布</li>
                                    </ul>
                                </div>

                                <!-- Q&A Section -->
                                <div style="padding: 20px 0;">
                                    <h4 style="font-size: 18px; color: #5A5A5A; margin-bottom: 10px;">用例展示</h4>
                                    <div class="block">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">给定以下对图片的描述，请你判断描述与图片间的对应关系是否一致。如果一致请仅回答True，如果不一致请仅回答False，不需要做其他任何解释。 描述：两个人正在打网球。
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">True</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/tennis.jpg')"
                                        style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                        <div
                                            style="border-radius: 8px; background-color: #F7F7F7; padding: 15px; margin-bottom: 10px;" class="QA">
                                            <strong style="color: #4A4A4A;">问：</strong>
                                            <span style="color: #6D6D6D;">基于给定的一对图片和描述，描述与图片之间的关系有：“蕴含（Entailment）”、“矛盾（Contradiction）”和“中立（Nutral）”。蕴含（Entailment）是指图片中有充分的证据证明描述是正确的。矛盾（Contradiction）是指图片中有充分的证据证明描述是错误的。中立（Nutral）是指图片中没有充分的证据证明描述是正确的还是错误的。请你判断下列描述对于图片的关系是“蕴含（Entailment）”、“矛盾（Contradiction）”还是“中立（Nutral）”，只需要说出正确答案，不要提及错误选项以及做其他任何解释。描述：有人刚刚刷完牙。
                                            </span><br>
                                            <strong style="color: #4A4A4A;">答：</strong>
                                            <span style="color: #6D6D6D;">Neutral</span>
                                        </div>
                                        <img :src="require('@/assets/data_list_image/toothbrush.jpg')"
                                        style="width: 100%; height: 30%; object-fit: cover; border-radius: 8px;">
                                    </div>
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                </div>

            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import { getDataList } from "@/api/dataList"
export default {
    name: "dataList",
    data() {
        return {
            loading: false,
            filterdata: [{ "question": "string", "answer": "string", "file_url": "http://localhost:5000/data/icon/icon_0434f2400ce9b7e.jpg", "uploader": "string", "version_update": { "version": "string", "update_time": "string" }, "answer_mode": "string(level1/level2)", "date_note": "string" },],
            // filterdata: [],
            resource: null,
            test_dimension: null,
            data_type_input: null,
            data_type_output: null,
            resource_options: [
                { value: '自筹', label: '自筹' },
                { value: 'C-eval', label: 'C-eval' },
                { value: 'CMMLU', label: 'CMMLU' }
            ],
            test_dimension_options: [
                { value: '半结构化数据生成', label: '半结构化数据生成' },
                { value: '常识推理', label: '常识推理' },
                { value: '代码理解', label: '代码理解' },
                { value: '代码生成', label: '代码生成' },
                { value: '多语言能力', label: '多语言能力' },
                { value: '公平性', label: '公平性' },
                { value: '合规性', label: '合规性' },
                { value: '幻觉', label: '幻觉' },
                { value: '机器翻译', label: '机器翻译' },
                { value: '鲁棒性', label: '鲁棒性' },
                { value: '逻辑推理', label: '逻辑推理' },
                { value: '命名实体识别', label: '命名实体识别' },
                { value: '任务分解', label: '任务分解' },
                { value: '数学推理', label: '数学推理' },
                { value: '文本分类', label: '文本分类' },
                { value: '文本改写', label: '文本改写' },
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
                { value: '图表推理', label: '图表推理' },
                { value: '图片问答', label: '图片问答' },
                { value: '视频检索', label: '视频检索' },
                { value: '有声视频问答', label: '有声视频问答' }
            ],
            data_type_options: [
                { value: 'txt', label: '文本' },
                { value: 'image', label: '图像' },
                { value: 'video', label: '视频' },
                { value: 'audio', label: '音频' }
            ],
            // images: [
            //     require('@/assets/imageNet/a.jpg'),
            //     require('@/assets/imageNet/b.jpg'),
            //     require('@/assets/imageNet/c.jpg'),
            //     require('@/assets/imageNet/d.jpg')
            // ],

        };
    },
    methods: {
        // 判断是否为图片格式
        isImage(fileUrl) {
            return /\.(jpg|jpeg|png|gif)$/i.test(fileUrl);
        },
        // 判断是否为视频格式
        isVideo(fileUrl) {
            return /\.mp4$/i.test(fileUrl);
        },
        hanedleClear() {
            this.test_dimension = null
            this.data_type_input = null
            this.data_type_output = null
            this.resource = null
            this.filterdata = []
            this.$message({
                type: 'info',
                message: '已重置'
            });
        },
        handleSearch() {
            this.loading=true
            if (this.data_type_input || this.data_type_output || this.resource || this.test_dimension) {
                if (this.data_type_input && this.data_type_output) {
                    const searchOptions = {
                        resource: this.resource,
                        data_type: { "input": this.data_type_input, "output": this.data_type_output },
                        test_dimension: this.test_dimension
                    }
                    getDataList(searchOptions).then(res => {
                        if (res.success) {
                            this.filterdata = res.data
                            this.loading=false
                        }
                        else
                        {
                            this.loading=false
                        }
                    }
                    )
                }
                else {
                    if (!this.data_type_input) {
                        this.$message({
                            type: 'warning',
                            message: '请选择输入数据类型'
                        });
                    }
                    else if (!this.data_type_ouput) {
                        if (!this.data_type_input) {
                            this.$message({
                                type: 'warning',
                                message: '请选择输出数据类型'
                            });
                        }
                    }
                }
            }
            else {
                this.$message({
                    type: 'warning',
                    message: '请先选择筛选选项'
                });
            }
        }
    }
}
</script>
<style scoped>
/* 可以根据需要调整选择器和卡片的布局 */
.box-card {
    width: 100%;
}

.QA{
    border-radius:4px ;
    border-color: black;
    border-style: dashed;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}

.el-select {
    width: 15%;
    margin-left: 20px;
    /* 设置每个选择器的宽度，根据需要调整 */
}

.el-col {
    border-radius: 4px;
    margin-left: 50px;
}

.light-purple {
    background: #f8f8f9;
}

.light-purple:hover {
    transform: scale(1.01); /* 放大5% */
}


.el-button {
    margin-left: 20px;
}

img, video {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
    border-radius: 8px; /* 可选：给图片和视频添加圆角 */
    transition: box-shadow 0.3s ease; /* 鼠标悬浮时的动画效果 */
}

img:hover, video:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4); /* 鼠标悬浮时加深阴影 */
}
</style>