<template>
  <el-container>
    <el-header style="padding: 0">
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="/keyConfig">APIKEY</el-menu-item>
        <el-menu-item index="/dataSetConfig">数据集</el-menu-item>
      </el-menu>
    </el-header>
    <el-main style="padding: 0">
      <router-view/>
    </el-main>
  </el-container>
</template>


<script>
export default {
  name: "ConfigureNavigation",
 data() {
      return {
        activeIndex: '1',
      };
},
methods: {
      handleSelect(key) {
         if (this.$route.path !== key)
           this.$router.push(key);
      }
    }
}
</script>

<style scoped>

</style>