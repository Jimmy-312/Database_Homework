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
        }
    })    
}
$.getUser()