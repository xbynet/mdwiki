var webpack = require('webpack')
var config = require('./webpack.base.config')
var path = require('path');
//此处先判断是否为null，然后用concat拼接数组，为什么不用push? , push 与 concat 区别:push()方法会修改原有数组，这就会影响其他环境。concat不会改变现有的数组，而仅仅会返回被连接数组的一个副本。
config.plugins = (config.plugins || []).concat([
  // this allows uglify to strip all warnings
  // from Vue.js source code.
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: '"production"'
    }
  }),
  // This minifies not only JavaScript, but also
  // the templates (with html-minifier) and CSS (with cssnano)!
  new webpack.optimize.UglifyJsPlugin({
    compress: {
      warnings: false
    }
  })
])
module.exports = config