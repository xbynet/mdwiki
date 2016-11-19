//es6加载模块 ,需要babel-loader支持
import Vue from 'vue'  
 
//require('vue')
//require('./views/index.vue')
 
//创建一个vue实例,挂载在body上面  
export default new Vue({   
    el: 'body',  
    components: {  }  
})


