const { defineConfig } = require('@vue/cli-service')
module.exports = {
  publicPath: './',  // 使用相对路径
  outputDir: 'dist', // 输出目录
  productionSourceMap: false, // 生产环境不生成 source map
}
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
