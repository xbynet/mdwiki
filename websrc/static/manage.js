$(function() {
    $(".progress").hide();
    $("#rebuildIndex").on('click', function() {
        if (window.myInterId) {
            clearInterval(window.myInterId);
            window.myInterId = null;
        }
        $(".progress").show();
        window.myInterId = setInterval(function() {
            var value = $(".progress-bar").data('value');
            var widthInt = parseInt(value);
            if ((widthInt + 10) >= 80) {
                widthInt += 1;
            } else {
                widthInt += 2;
            }
            $(".progress-bar").data('value', '' + widthInt);
            $(".progress-bar").css('width', widthInt + '%');
        }, 2000);
        $.get($("#rebuildIndex").data('url'), function(data) {
            if (data.status == 'ok') {
                toastr.success('索引重建成功');
                $(".progress-bar").css('width', '100%');
                $(".progress").hide();
                clearInterval(window.myInterId);
                window.myInterId = null;
            }
        }, 'json');

    });
    $(".delbakBtn").on('click', function(e) {
        var url = $(this).data('url');
        var _this=this;
        $.get(url, function(data) {
            if (data.status == 'ok') {
                toastr.success('删除成功');
                $(_this).parent().parent().remove();
            }
        }, 'json');
    });
    $(".downbakBtn").on('click', function(e) {
        var url = $(this).data('url');
        $.get(url, function(data) {
            if (data.status == 'ok') {
                var downloadUrl = data.url;
                //toastr.success('删除成功');
                //$(this).parent().parent().remove();
                window.open(downloadUrl);
            }
        }, 'json');
    });
});
