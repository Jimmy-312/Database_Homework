var userinfo = ''
$(function () {
    $('[data-toggle="popover"]').popover()
  })
$.getUser = function () {
    $.ajax({
        url: "/getUser/",
        method: "POST",
        async:true,
        success: function (data) {
            data = JSON.parse(data)
            userinfo = data
            //console.log(userinfo)
            $("#info_name").text(userinfo.name)
            $("#info_gender").text(userinfo.gender)
            $("#info_age").text(userinfo.age)
            $("#info_hos").text(userinfo.hos)
            $("#info_dep").text(userinfo.dep)
            $("#topname").text(userinfo.name + ",欢迎您")
            if (userinfo.level==1) {
                $("#user_level").attr("class", "label label-primary")
                $("#user_level").text("管理员")
            }
            if (userinfo.level==2) {
                $("#user_level").attr("class", "label label-warning")
                $("#user_level").text("站长")
            }
            
        }
    })    
}
var tou = 0;
$.changetou = function () {
    tou = (tou + 1) % 5 
    $("#tou").attr("src","/static/img/"+tou+".jpg")
}
$.getUser()
$.getHospital = function () {
    $.ajax({
        url:'/get_hos/',
        type: 'POST',
        success: function (data) {
            //console.log(data)
            data = JSON.parse(data)
            var st=''
            for (var i = 0; i < data.length; i++){
                st = st + '<option>' + data[i] + '</option>\n'
            }
            //console.log(st)
            $(".hospital").append(st)
        },
    })
}
$.getHospital();
$.getUsers = function () {
    $.ajax({
        url: "/get_users/",
        type: "POST",
        success:function (data) {
            data = JSON.parse(data)
            var users = data.users
            $("#retable").html("")
            for (var i = 0; i < users.length; i++){
                u=users[i]
                var st="<tr style='height:36px' id='"+u.id+"'>\
                <td style='width:80px'>"+ u.name +"</td>\
                <td style='width:90px'>"+ u.level +"</td>\
                <td style='width:43px'>"+ u.sex +"</td>\
                <td style='width:43px'>"+ u.age +"</td>\
                <td style='width:255px'>"+ u.hos +"</td>\
                <td style='width:76px'>"+ u.dep +"</td>\
                <td style='width:160px'>"
                if (userinfo.level == 1) {
                    if (u.level == "普通用户") {
                        st += "<a href=\'javascript:$.lchange(\"" + u.id + "\",\"1\",\"" + u.level + "\")\'> 升级 </a>"
                    }
                    else {
                        st +="<a style='color:black;'>无权限</a>"
                    }
                }
                if (userinfo.level == 2) {
                    st += "<a href=\'javascript:$.lchange(\"" + u.id + "\",\"1\",\"" + u.level + "\")\'> 升级 </a>"
                    st += "<a href=\'javascript:$.lchange(\"" + u.id + "\",\"-1\",\"" + u.level + "\")\'> 降级 </a>"
                    st += "<a href=\'javascript:$.delu(\"" + u.id + "\")\'> 删除 </a>"
                }
                if (userinfo.level == 0) {
                    st +="<a style='color:black;'>无权限</a>"
                }
                st+="</td >\
            </tr>"
                $("#retable").append(st)
            }
            //$("#ttitle").attr("style","background-color: lightgrey;position: fixed;height: 36px;")
        }
    })
}
$.delu = function (pid) {
    $.ajax({
        url: "/delu/",
        type: "POST",
        data: {"id":pid},
        success:function (data) {
            data = JSON.parse(data)
            $.getUsers()
            $.getUser()
        }
    })    
}
$.lchange = function (pid,p,ty) {
    $.ajax({
        url: "/l_change/",
        type: "POST",
        data: { "p": p ,"id":pid},
        success:function (data) {
            data = JSON.parse(data)
            $.getUsers()
            $.getUser()
        }
    })    
}
$.getUsers()
$.edituser = function () {
    $(".edit").attr("type", "text")
    $("#edit_sex").attr("style", "height: 30px;width: 150px;")
    $("#edit_hos").attr("style","height: 30px;width: 150px;")
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
            //console.log(data)
            $.getUser()
            $(".edit").attr("type", "hidden")
            $("#edit_sex").attr("style", "display:none;")
            $("#edit_hos").attr("style","display:none;")
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