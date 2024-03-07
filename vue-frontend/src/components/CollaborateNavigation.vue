<template>
  <el-container>
    <el-header style="padding: 0">
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="/experimentCollaborate">我的协作实验</el-menu-item>
        <el-menu-item index="/userList">添加好友</el-menu-item>
      </el-menu>
    </el-header>
    <el-main style="padding: 0">
      <router-view/>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: "CollaborateNavigation",
  data() {
    return {
      activeIndex: '', // 初始化为空字符串或者根据你的路由设置一个默认值
    };
  },
  mounted() {
    this.setActiveIndex(); // 当组件挂载时设置activeIndex
  },
  watch: {
    // 监听路由变化以更新菜单激活状态
    '$route.path': {
      immediate: true, // 立即触发，确保刷新页面时也能获取正确的状态
      handler() {
        this.setActiveIndex();
      }
    }
  },
  methods: {
    handleSelect(key){
      if (this.$route.path !== key)
        this.$router.push(key);
    },
    setActiveIndex() {
      // 将activeIndex设置为当前路由的路径
      this.activeIndex = this.$route.path;
    }
  }
}
</script>

<style scoped>

</style>
