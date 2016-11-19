var webpack = require('webpack')
var path = require('path');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
module.exports = {
  entry: './static/entry.js',
  output: {
    path: './app/static',
    filename: 'main.bundle.js',
    publicPath:'/app/static/'
  },
  /*devServer: {
    contentBase: "./public",//本地服务器所加载的页面所在的目录
    colors: true,//终端中输出结果为彩色
    historyApiFallback: true,//不跳转
    inline: true//实时刷新
  },*/
  //devtool:"eval-source-map",
  module: {
    loaders: [
    { test: /\.js$/,loader: 'babel',exclude: /node_modules/ },
    { test: /\.css$/,exclude: /node_modules/ , loader: ExtractTextPlugin.extract("style", "css?sourceMap") },
    //{ test: /\.scss$/,exclude: /node_modules/, loader: 'style!css!sass?sourceMap'},
      //图片文件使用 url-loader 来处理，小于8kb的直接转为base64
    { test: /\.(png|jpg)$/,exclude: /node_modules/, loader: 'url?limit=8192'},
    //  { test: /\.html$/,exclude: /node_modules/, loader: 'file'},
    { test: /\.vue$/, exclude: /node_modules/,loader: 'vue'}
    ],
    babel: {  //also can extract to .babelrc
      presets: ['es2015', 'stage-0'],  
      plugins: ['transform-runtime']  
    }
  },
  plugins: [
  new ExtractTextPlugin("[name].css"),
  new webpack.ProvidePlugin({
    $: "jquery",
    jQuery: "jquery",
    "window.jQuery": "jquery"
  }),
  new webpack.optimize.OccurenceOrderPlugin() 
  ],
  //配置查找模块的路径和扩展名和别名。
  resolve: {
    //查找module的话从这里开始查找
    root: path.join(path.resolve(__dirname),'../app','static'), //绝对路径
    //自动扩展文件后缀名，意味着我们require模块可以省略不写后缀名
    extensions: ['', '.js', '.json','css'],
     //模块别名定义，方便后续直接引用别名，无须多写长长的地址
    alias: {
      Main : 'Main.bundle',
      jquery:'lib/jquery.min'
    }
  }
}