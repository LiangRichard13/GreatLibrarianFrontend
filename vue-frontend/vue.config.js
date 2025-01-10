const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
   devServer: {
    proxy: {
      '/api': {
          // target: 'http://0.0.0.0:5000',
          target: 'http://192.168.70.12:5000',
        // target: 'http://localhost:5000', // 后端API的地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': '' // 重写路径，去掉/api前缀
        }
      }
    },
    client:{
    overlay:false
    }
  },
  transpileDependencies: true,
})
