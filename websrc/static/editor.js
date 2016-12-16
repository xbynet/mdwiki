$(function() {
    window.isCloseHint = true;
    //初始化关闭
    window.addEventListener("beforeunload", function(e) {
        if (window.isCloseHint) {
            var confirmationMessage = "要记得保存！你确定要离开我吗？";
            (e || window.event).returnValue = confirmationMessage; // 兼容 Gecko + IE
            return confirmationMessage; // 兼容 Gecko + Webkit, Safari, Chrome
        }
    });

    $("form:eq(1)").validate({
        submitHandler: function(form) {
            window.isCloseHint=false;
            
            form.submit();
        },
        rules: {
            title: "required"
        },
        messages: {
            title: "必填"
        }
    });
    var simplemde = new SimpleMDE({
        element: document.getElementById("textArea1"),
        indentWithTabs: false,
        tabSize:4,
        placeholder: "请书写文章吧",
        renderingConfig: {
            singleLineBreaks: false,
            codeSyntaxHighlighting: true,
        },
        spellChecker: false,
        insertTexts: {
               // horizontalRule: ["", "\n\n-----\n\n"],
               // image: ["![](http://", ")"],
                link: ["[", "](/pages/)"]
               // table: ["", "\n\n| Column 1 | Column 2 | Column 3 |\n| -------- | -------- | -------- |\n| Text     | Text      | Text     |\n\n"],
        },
        // styleSelectedText: false,
        status: ["autosave", "lines", "words", "cursor"],
        toolbar: ["bold", "italic", "strikethrough", "heading", "heading-1", "heading-2", "heading-3", "code", "quote", "unordered-list", "ordered-list", "clean-block", "link", "image", "table", "horizontal-rule", "side-by-side", "preview", "fullscreen", "guide", {
            name: "save",
            action: function(editor) {
                if ($('form:eq(1)').valid()) {
                    window.isCloseHint=false;
                    $('form:eq(1)').submit();
                } else {
                    toastr.error("标题必须填写");
                }

            },
            className: "fa fa-save",
            title: "保存",
        }, ]
    });
    //simplemde.toggleSideBySide();
    simplemde.codemirror.on("paste", function(editor, e) {
        // console.log(e.clipboardData)
        if (!(e.clipboardData && e.clipboardData.items)) {
            alert("该浏览器不支持操作");
            return;
        }
        for (var i = 0, len = e.clipboardData.items.length; i < len; i++) {
            var item = e.clipboardData.items[i];
            // console.log(item.kind+":"+item.type);
            if (item.kind === "string") {
                item.getAsString(function(str) {
                    // str 是获取到的字符串
                })
            } else if (item.kind === "file") {
                var blob = item.getAsFile();
                // pasteFile就是获取到的文件
                // console.log(blob);
                // console.log(blob instanceof File);
                var file = new File([blob], Math.random() * 1000 + ".png");
                // console.log(file);
                fileUpload(file);
            }
        }
    });
    simplemde.codemirror.on("drop", function(editor, e) {
        // console.log(e.dataTransfer.files[0]);
        if (!(e.dataTransfer && e.dataTransfer.files)) {
            alert("该浏览器不支持操作");
            return;
        }
        for (var i = 0; i < e.dataTransfer.files.length; i++) {
            // console.log(e.dataTransfer.files[i]);
            fileUpload(e.dataTransfer.files[i]);
        }
        e.preventDefault();
    });
    //文件上传
    /* function fileUpload(fileObj) {
         var data = new FormData();
         data.append("file", fileObj);
         var xhr = new XMLHttpRequest();
         xhr.open("post", "", true);
         xhr.onreadystatechange = function() {
             if (xhr.readyState == 4) {
                 // alert(xhr.responseText);
             }
         };
         xhr.send(data);
     }*/
    //阻止浏览器默认打开拖拽文件的行为
    window.addEventListener("drop", function(e) {
        e = e || event;
        e.preventDefault();
        if (e.target.tagName == "textarea") { // check wich element is our target
            e.preventDefault();
        }
    }, false);
    if (!WebUploader.Uploader.support()) {
        alert('Web Uploader 不支持您的浏览器！如果你使用的是IE浏览器，请尝试升级 flash 播放器');
        throw new Error('WebUploader does not support the browser you are using.');
    }
    //console.log(WebUploader);
    var uploader = WebUploader.create({
        swf: 'lib/webuploader/Uploader.swf',
        // 文件接收服务端。
        server: "/upload",
        formData: {
            csrf_token: $("#csrf_token").val()
        }

        // 开起分片上传。
        // chunked: true
    });

    function fileUpload(file) {
        uploader.addFiles(file);
        uploader.upload();
    }
    // 当有文件被添加进队列的时候
    uploader.on('fileQueued', function(file) {
        if (!file.id) {
            file.id = guid();
        }
        var $list = $("#showProgress");
        $list.show();
        $list.append('<div id="' + file.id + '" class="item">' +
            '<h4 class="info">' + file.name + '</h4>' +
            '<p class="state">等待上传...</p>' +
            '</div>');
    });

    // 文件上传过程中创建进度条实时显示。
    uploader.on('uploadProgress', function(file, percentage) {
        var $li = $('#' + file.id),
            $percent = $li.find('.progress .progress-bar');
        // 避免重复创建
        if (!$percent.length) {
            $percent = $('<div class="progress progress-striped active">' +
                '<div class="progress-bar" role="progressbar" style="width: 0%">' +
                '</div>' +
                '</div>').appendTo($li).find('.progress-bar');
        }

        $li.find('p.state').text('上传中');
        $percent.css('width', percentage * 100 + '%');
    });
    uploader.on('uploadSuccess', function(file, data) {
        $('#' + file.id).find('p.state').text('已上传');
        var text = '![' + data.filename + '](' + data.link + ')';
        insertTextAtCursor(simplemde.codemirror, text);
    });

    uploader.on('uploadError', function(file) {
        $('#' + file.id).find('p.state').text('上传出错');
        alert(file.name + "上传出错");
    });
    uploader.on('uploadComplete', function(file) {
        $('#' + file.id).fadeOut();
        $('#' + file.id).remove();
    });

    function insertTextAtCursor(editor, text) {
        var doc = editor.getDoc();
        var cursor = doc.getCursor();
        doc.replaceRange(text, cursor);
    }

    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }

    function guid() {
        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    }

    initTag();
    keepaliveAndCheckLock(); 

    function keepaliveAndCheckLock(){

        var url=$("#checkLock").data("url");
        var location=$("#location").val(); 
        //var modifyAt=$("#modifyAt").val();
        window.unlockNotify=false;
        test();
        function test(){
            $.get(url,{location:location},function(data){
                if(data.status=='unlock' && (!window.unlockNotify)){
                    window.unlockNotify=true;
                    debugger;
                    alert("请注意，文章已经解除占用，请及时保存以免发生冲突！");
                }
            },'json');
            console.log('test');
            setTimeout(test, 30*1000); 
        }
    }
    function initTag() {

        /*tag input init taggle.js*/
        var initTags = $('#tags').val() ? $('#tags').val() : '';
        var toggleTag = new Taggle($('.tagsDiv')[0], {
            placeholder: '请输入标签，逗号分隔',
            tags: initTags ? initTags.split(',') : [],

            onTagAdd: function(event, tag) {
                // text.innerHTML = 'You just added ' + tag;
                var tmp = toggleTag.getTagValues().join(',');
                $('#tags').val(tmp);
            },
            onTagRemove: function(event, tag) {
                // text.innerHTML = 'You just removed ' + tag;
                var tmp = toggleTag.getTagValues().join(',');
                $('#tags').val(tmp);

            }
        });
        var tagContainer = toggleTag.getContainer();
        var input = toggleTag.getInput();
        $.ajax({
            url: '/tags/input',
            dataType: 'json',
            success: function(data) {
                $(input).autocomplete({
                    source: data,
                    appendTo: tagContainer,
                    position: { at: "left bottom", of: tagContainer },
                    select: function(event, data) {
                        event.preventDefault();
                        //Add the tag if user clicks
                        if (event.which === 1) {
                            toggleTag.add(data.item.value);
                        }
                    }
                });
            }
        });
    }
});
