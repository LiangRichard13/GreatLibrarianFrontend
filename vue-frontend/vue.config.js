const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
   devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 后端API的地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': '' // 重写路径，去掉/api前缀
        }
      }
    }
  },
  transpileDependencies: true,
})
