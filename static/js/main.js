var userinfo=''
$.getUser = function () {
    $.ajax({
        url: "/getUser/",
        method: "POST",
        success: function (data) {
            data = JSON.parse(data)
            userinfo = data
            //console.log(userinfo)
            $("#info_name").text(userinfo.name)
            $("#info_gender").text(userinfo.gender)
            $("#info_age").text(userinfo.age)
            $("#info_hos").text(userinfo.hos)
            $("#info_dep").text(userinfo.dep)
            $("#topname").text(userinfo.name+",欢迎您")
        }
    })    
}
$.getUser()
$.edituser = function () {
    $(".edit").attr("type", "text")
    $("#edit_sex").attr("style","height: 30px;width: 150px;")
    $(".display").attr("hidden", "")
    $(".bzd").removeAttr("style")//"margin-top: -10px;"
    $("#edit_s").attr("style", "display:none;")
    $("#edit_p").removeAttr("style")
    $("#edit_pass").attr("style", "display:none;")
    

    $("#edit_name").val(userinfo.name)
    $("#edit_sex").val(userinfo.gender)
    $("#edit_age").val(userinfo.age)
    $("#edit_hos").val(userinfo.hos)
    $("#edit_dep").val(userinfo.dep)
}

$("#edit_user").submit(function () {
    $.ajax({
        url: "/edit_user/",
        type: "POST",
        data: $("#edit_user").serialize(),
        success: function (data) {
            data = JSON.parse(data)
            console.log(data)
            $.getUser()
            $(".edit").attr("type", "hidden")
            $("#edit_sex").attr("style","display:none;")
            $(".display").removeAttr("hidden")
            $(".bzd").attr("style", "margin-top: -10px;")
            $("#edit_p").attr("style", "display:none;")
            $("#edit_s").removeAttr("style")
            $("#edit_pass").attr("style","margin-left: 10px;")
        }
    })
    return false;
})

$("#edit_form").submit(function () {
    if ($("#edit_new").val() != $("#edit_newr").val()) {
        return false;
    }
    $.ajax({
        url: "/edit_pass/",
        type: "POST",
        data: $("#edit_form").serialize(),
        success: function (data) {
            data = JSON.parse(data)
            //console.log(data)
            $("#edit_form")[0].reset()
            $("#editpass").modal("hide")
        }
    })
    return false;
})

$.checkpass = function () {
    if ($("#edit_new").val() != $("#edit_newr").val()) {
        $("#edit_newr_d").attr("class", "form-group has-error")
        $("#edit_sub").attr("disabled","disabled")
    } else {
        $("#edit_newr_d").attr("class", "form-group")
        $("#edit_sub").removeAttr("disabled")
    }
}