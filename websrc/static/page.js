$(function() {
    var linktext = Autolinker.link($("#postContent").html(), {
        className: 'lincl',
        urls: {
            tldMatches: false
        }
    });
    $("#postContent").html(linktext);

    $('#delDialog').dialog({
        autoOpen: false,
        width: 600,
        buttons: {
            "Ok": function() {
                var url = $('#delPost').attr('href');
                location.href = url;
                //   $.post(url,{csrf_token:csrf_token},"json");
                $(this).dialog("close");
            },
            "Cancel": function() {
                $(this).dialog("close");
            }
        }
    });

    $("#delPost").click(function(e) {
        $('#delDialog').dialog('open');
        e.preventDefault();
        // e.stopPropagation();
    });

    //toc
    $('.mdwiki_toc_container h3').on('click', function() {
        $('.mdwiki_toc_container .collapse').collapse('toggle');
        //testOneAnim('.mdwiki_toc_container','pulse');
    });
    $(window).scroll(function() {
        if ($(document).scrollTop() == 0) {
            $('.mdwiki_toc_container').css('top', '165px');
        } else {
            $('.mdwiki_toc_container').css('top', '10px');
        }
        // testOneAnim('.mdwiki_toc_container','zoomOutRight');
        $('.mdwiki_toc_container .collapse').collapse('hide');
    });
    if ($(document).scrollTop() == 0) {
        $('.mdwiki_toc_container').css('top', '165px');

    }
    $('.mdwiki_toc_container').show();

    initCodeScroll();
    //animate
    // testAnim('.page-title-bg','jello');

    // testOneAnim('.main','bounce');
    function initCodeScroll() {

        $("pre").each(function(i,e) {
            $(this).wrap("<div class='codesnipshit'></div>");
            //init code tool
            var text=$(this).find('code').text();
            text=$("<div />").text(text).html();
            text=text.replace(/\"/g,'codeReplaceHolderDouble').replace(/\'/g,'codeReplaceHolderSingle');
            $(this).parent().prepend('<div class="widget-codetool" ><div class="code-tool-div widget-codetool--inner"><div class="code-tool"><span class="copy" data-text="'+text+'"><i class="fa fa-copy"></i>复制</span></div></div></div>');
            

            //init highlight
            hljs.highlightBlock(e);
            //init scroll
            var h = $(this).height()
            var maxH = 400;
            if (h > maxH) {
                $(this).css("max-height", maxH + "px");
                $(this).mCustomScrollbar({
                    setTop: 0,
                    setLeft: 0,
                    axis: "y",
                    scrollbarPosition: "inside",
                    scrollInertia: 350,
                    autoDraggerLength: !0,
                    alwaysShowScrollbar: 0,
                    snapOffset: 0,
                    mouseWheel: {
                        enable: !0,
                        scrollAmount: "auto",
                        axis: "y",
                        deltaFactor: "auto",
                        disableOver: ["select", "option", "keygen", "datalist", "textarea"]
                    },
                    scrollButtons: {
                        scrollType: "stepless",
                        scrollAmount: "auto"
                    },
                    keyboard: {
                        enable: !0,
                        scrollType: "stepless",
                        scrollAmount: "auto"
                    },
                    contentTouchScroll: 25,
                    documentTouchScroll: !0,
                    advanced: {
                        autoScrollOnFocus: "input,textarea,select,button,datalist,keygen,a[tabindex],area,object,[contenteditable='true']",
                        updateOnContentResize: !0,
                        updateOnImageLoad: "auto",
                        autoUpdateTimeout: 60
                    },
                    theme: "3d-thick",//"rounded-dots-dark",
                    callbacks: {
                        onTotalScrollOffset: 0,
                        onTotalScrollBackOffset: 0,
                        alwaysTriggerOffsets: !0
                    }
                });
            }

        });
         $(".codesnipshit .copy").on('click',function(e){
                $(this).text("已复制");
                //e.preventDefault();
                //e.stopepropagation();
        });

        $(".codesnipshit").hover(function(){
                $(this).find(".code-tool-div").show();

            },function(){
                $(this).find(".code-tool-div").hide();
                $(this).find(".copy").empty();
                $(this).find(".copy").append('<i class="fa fa-copy"></i>复制');
            });

        new Clipboard('.codesnipshit .copy',{
            text:function(e){
               return  $(e).data('text').replace(/codeReplaceHolderDouble/g,'"').replace(/codeReplaceHolderSingle/g,"'");
            }
        });
            
    }

});
