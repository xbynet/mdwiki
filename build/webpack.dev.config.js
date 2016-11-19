var config = require('./webpack.base.config')
config.devtool = 'eval-source-map' //'cheap-module-eval-source-map'构建速度更快，但是不利于调试，推荐在大型项目考虑da时间成本是使用。
module.exports = config
