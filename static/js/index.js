
$(function () {
    $('[data-toggle="popover"]').popover()
})
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

$.toreg = function () {
    $('.register').removeAttr('hidden');
    $('.login').attr('hidden','');

    $("#blog").removeAttr('class')
    $("#breg").attr('class',"active")
}

$.tologin = function () {
    $('.login').removeAttr('hidden');
    $('.register').attr('hidden','');

    $("#breg").removeAttr('class')
    $("#blog").attr('class',"active")
}

$("#regp").submit(function() {
    $.ajax({
        url:'',
        type:'POST',
        data:$('#regp').serialize(),
        success: function(data){
            data = JSON.parse(data)
            //console.log(data)
            $("#tip").attr("class","alert alert-"+data.class)
            if(data.class == "success"){
                $("#regp")[0].reset()
                $.tologin()
            }
            $("#tip").removeAttr("hidden")
            $("#tip_c").text(data.tip)
        },
    });
    return false;
})

$("#logp").submit(function() {
    $.ajax({
        url:'',
        type:'POST',
        data:$('#logp').serialize(),
        success: function(data){
            data = JSON.parse(data)
            console.log(data)
            $("#tip").attr("class","alert alert-"+data.class)
            if(data.class == "success"){
                $("#logp")[0].reset()
                setTimeout(window.location.href=data.url,8000)
            }
            $("#tip").removeAttr("hidden")
            $("#tip_c").text(data.tip)
        },
    });
    return false;
})