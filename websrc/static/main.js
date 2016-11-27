$(function() {
    // Back to top
    $('#back-to-top').click(function(e) {
        e.preventDefault();
        //$(document.body).scrollTop(0);
        $(document.body).animate({ scrollTop: 0 }, 500);
    });
    window.testOneAnim = function(elSel, cls) {
        $(elSel).addClass(cls + ' animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass(cls + ' animated');
        });
    };
    $('a,.page-title-bg h2,.colorgraph').on('mouseenter', function(e) {
        testOneAnim(this, 'pulse');
    });
    $("#searchBtn").on('click', function() {
        $("#searchForm").submit();
    });
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
});
