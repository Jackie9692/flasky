$(document).ready(function () {
    /***登入页面动画***/
    $('#mobile').focus(function () {
        var value =$('#mobile').val();
        if(value == "请输入正确手机号"){
            $(this).val(null);
        };150
    })
    $('#mobile').blur(function () {
        var mobile = $('#mobile').val();
         if(!/^(13[0-9]|14[0-9]|15[0-9]|18[0-9])\d{8}$/i.test(mobile))
        {
          $('#mobile').val("请输入正确手机号");
        }
    });
    /****注册页面动画****/
    $('#loan').hover(function () {
        $('#mynav').show();
        $('#mynav').hover(function () {
            $('#mynav').show();
        },function () {
            $('#mynav').hide();
        })
    },function () {
        $('#mynav').hide();
    })
})