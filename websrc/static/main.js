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
    $('.colorgraph').on('mouseenter', function(e) {
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
    };

    var breadcrumb=localStorage.getItem('breadcrumb');
    if(breadcrumb){
        breadcrumb=JSON.parse(breadcrumb);
    }else{
        breadcrumb=[];
    }

    var curPage={name:$(".title:first").text(),url:location.href}
    var shouldAdd=true;
    for(var i=0;i<breadcrumb.length;i++){
        if(curPage.name==breadcrumb[i].name || !curPage.name){
            shouldAdd=false;
            break;
        }
    }
    if(shouldAdd){
        if(breadcrumb.length>=5){
            breadcrumb.shift();
        }
        breadcrumb.push(curPage);
    }
    localStorage.setItem('breadcrumb',JSON.stringify(breadcrumb));
    $.each(breadcrumb,function(i,e){
        var replace='<li><a href="'+e.url+'" style="color: #017E66;">'+e.name+'</a></li>';
        $('.topbreadcrumb').append(replace);
    });
     $('.topbreadcrumb').show();
});
