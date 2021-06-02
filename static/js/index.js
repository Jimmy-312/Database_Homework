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
$.getHospital()