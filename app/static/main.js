$(function() {
    // Back to top
    $('#back-to-top').click(function(e) {
        e.preventDefault();
        //$(document.body).scrollTop(0);
        $(document.body).animate({ scrollTop: 0 }, 500);
    });
     window.testOneAnim=function(elSel,cls) {
        $(elSel).addClass(cls + ' animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass(cls + ' animated');
        });
    };
    $('a,.page-title-bg h2,.colorgraph').on('mouseenter',function(e){
        testOneAnim(this,'pulse');
    });
});
