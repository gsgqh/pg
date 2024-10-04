const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// module.exports = {
//   devServer: {
//     proxy: {
//       '/api': {
//         target: 'http://127.0.0.1:5000', // 后端 Flask 服务的地址
//         changeOrigin: true,
//         pathRewrite: {
//           '^/api': '' // 将/api前缀重写为空
//         }
//       }
//     }
//   }
// }
