$(function() {
    $('pre').each(function(i, e) {
        hljs.highlightBlock(e);
    });
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
         testOneAnim('.mdwiki_toc_container','pulse');
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

    //animate
    // testAnim('.page-title-bg','jello');
    
    testOneAnim('.main','bounce');
});
