createAt:2016-11-22 02:18:01
author:xby@xbynet.net
modifyAt:2016-11-22 22:49:23
location:bbbb
title:默认分页

为您的网站或应用提供带有展示页码的分页组件，或者可以使用简单的翻页组件。

默认分页
受 Rdio 的启发，我们提供了这个简单的分页组件，用在应用或搜索结果中超级棒。组件中的每个部分都很大，有点事容易点击、易缩放、点击区域大。
高亮的查询结果摘要

         
　　高亮的过程如就是一个pipeline的处理过程,和4个元件相关:
　　　　Fragments : 基于匹配的term在文档中的位置，把原始的文档砍成__fragments__
　　　　Scorers: 给每个fragment赋一个分值，允许系统根据分值排出最好的fragment.
　　　　Order functions: 控制展示给用户的fragment，是展示先出现在文档里的fragment,还是展示score最高的fragment.
　　　　Formatters: 把对应的fragment格式化为用户可读格式，如html
           
　　在对文本进行高亮处理前，需要去除格式标签，比如:html,和 wiki tags.