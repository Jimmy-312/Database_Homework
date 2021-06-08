$(function () {
    $('[data-toggle="popover"]').popover()
  })
var userinfo = ''
$.getUser = function () {
    $.ajax({
        url: "/getUser/",
        method: "POST",
        success: function (data) {
            data = JSON.parse(data)
            userinfo = data            
        }
    })    
}
$.getUser()
$.getHospital = function () {
    $.ajax({
        url:'/get_hos/',
        type:'POST',
        success: function(data){
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

$.getinfo = function () {
    $.ajax({
        url:'/get_info/',
        type:'POST',
        success: function(data){
            data = JSON.parse(data)
            $("#doc_num").text(data.doc)
            $("#pat_num").text(data.pat)
            $("#hos_num").text(data.hos)
            $("#dis_num").text(data.dis)
            $("#jp_num").text(data.bz)
        },
    })
}
$.getinfo()
$.getDoc = function () {
    $.ajax({
        url:'/get_doc/',
        type:'POST',
        success: function(data){
            data = JSON.parse(data)
            var st=''
            for (var i = 0; i < data.length; i++){
                st = st + '<option>' + data[i] + '</option>\n'
            }
            //console.log(st)
            $(".doctor").append(st)
        },
    })
}
$.getDoc()

$.selectpage = function (num) {
    $('.page'+pnow).hide();
    $("#ap"+pnow).attr("class","lpage")
    pnow=num;
    $("#ap"+pnow).attr("class","active lpage")
    $('.page'+pnow).show();
}

$.nextpage = function(num){
    if(pnow+num>page|pnow+num<1){
        return false
    }
    $('.page'+pnow).hide();
    $("#ap"+pnow).attr("class","lpage")
    pnow+=num;
    $("#ap"+pnow).attr("class","active lpage")
    $('.page'+pnow).show();
}

$("#add_form").submit(function () {
    //console.log(userinfo.level)
    if (userinfo.level!=true) {
        $("#tip").attr("class","alert alert-warning")
        $("#tip").removeAttr("hidden")
        $('#addpatient').modal('hide')
        $("#tip_c").text("权限不足，请联系管理员！")
        setTimeout(function(){$("#tip").attr("hidden","")},5000);
        return false;
    }
     $.ajax({
         url:'/patient_add/',
         type:'POST',
         data:$('#add_form').serialize(),
         success: function(data){
             data = JSON.parse(data)
             if(data.class == "success"){
                 $("#add_form")[0].reset()
             }
             $("#tip").attr("class","alert alert-"+data.class)
             $("#tip").removeAttr("hidden")
             $('#addpatient').modal('hide')
             $("#tip_c").text(data.tip)
             setTimeout(function(){$("#tip").attr("hidden","")},5000);
             $.getContent()
         },
     });
     return false;
 })

$("#edit_form").submit(function () {
    //console.log(userinfo)
    if (userinfo.level!=true) {
        $("#tip").attr("class","alert alert-warning")
        $("#tip").removeAttr("hidden")
        $('#editpatient').modal('hide')
        $("#tip_c").text("权限不足，请联系管理员！")
        $('#editpatient').modal('hide')
        setTimeout(function(){$("#tip").attr("hidden","")},5000);
        return false;
    }
     $.ajax({
         url:'/patient_add/?me=edit',
         type:'POST',
         data:$('#edit_form').serialize(),
         success: function(data){
             data = JSON.parse(data)
             $("#tip").attr("class","alert alert-"+data.class)
             if(data.class == "success"){
                 $("#edit_form")[0].reset()
             }
             $("#tip").removeAttr("hidden")
             $('#editpatient').modal('hide')
             $("#tip_c").text(data.tip)
             setTimeout(function(){$("#tip").attr("hidden","")},5000);
             var obj = data.obj
             $("#row" + data.pid).children().eq(1).text(obj.id)
             $("#row" + data.pid).children().eq(2).text(obj.pid)
             $("#row" + data.pid).children().eq(3).text(obj.name)
             $("#row" + data.pid).children().eq(4).text(obj.sex)
             $("#row" + data.pid).children().eq(5).text(obj.age)
             $("#row" + data.pid).children().eq(6).text(obj.hos)
             $("#row" + data.pid).children().eq(7).text(obj.checkdate)
             $("#row" + data.pid).children().eq(8).text(obj.checkid)

             //$.getContent()
         },
     });
     return false;
 })
 
 $.getPatient = function(ppid) {
     $.ajax({
         url:'/get_patient/',
         type:'POST',
         data:{pid:ppid},
         success: function(data){
             data = JSON.parse(data)
             Object.keys(data).map(function(key){
                 $('#edit_form  input').filter(function(){
                     //console.log(this.name,key)
                     return key == this.name;
                 }).val(data[key]);
                 $("#sex_edit").val(data.sex)
                 $("#hos_edit").val(data.hos)
             });
         }
     })
 };

$.delpa = function (pid) {
    if (userinfo.level!=true) {
        $("#tip").attr("class","alert alert-warning")
        $("#tip").removeAttr("hidden")
        $('#addpatient').modal('hide')
        $("#tip_c").text("权限不足，请联系管理员！")
        setTimeout(function(){$("#tip").attr("hidden","")},5000);
        return false;
    }
    $.ajax({
         url:'/del_patient/',
         type:'POST',
         data:{'pid':pid},
         success: function(data){
            data = JSON.parse(data)
            $("#tip").attr("class","alert alert-"+data.class)
            $("#tip").removeAttr("hidden")
            $("#tip_c").text(data.tip)
            $.getContent()
         }
     })
 }

 
 var page=1
 var pnow=1
$("#query").submit($.getContent = function () {
    $.getinfo()
     $("#bquery").attr("disabled","disabled")
     $("#bquery").val("查询中")
     $.ajax({
         url:'/query_patient/',
         type:'POST',
         data:$('#query').serialize(),
         success: function(data){
            $("#bquery").val("查询")
            $("#bquery").removeAttr("disabled")
             data = JSON.parse(data)
             $("#tip2").attr("class","alert alert-"+data.class)
             $("#tip2").removeAttr("hidden")
             $("#tip_c2").text("总共查询到"+data.patient_num+"个符合条件的病人")
             $("#result").attr("hidden",'')
             if(data.patient_num>0){$("#result").removeAttr("hidden")}
             var st=''
             page=1
             for(var i=0;i<data.patient_num;i++){
                 if((i+1)%20==0){
                     page+=1
                 }
                 var pa=data.patient_id[i]
             st=st+'<tr class="contentcol page'+page+'" id="row'+pa[0]+'" hidden>\
    <td style="text-align: center;">\
        <a class="btn btn-info" href="javascript:$('+"'#editpatient'"+').modal('+"'show'"+');$.getPatient('+pa[0]+')">编辑</a>\
        &nbsp;\
        <a class="btn btn-danger" href="javascript:$.delpa('+pa[0]+')">删除</a>\
    </td>\
    <td>'+pa[0]+'</td>\
    <td>'+pa[1]+'</td>\
    <td>'+pa[2]+'</td>\
    <td>'+pa[3]+'</td>\
    <td>'+pa[4]+'</td>\
    <td>'+pa[5]+'</td>\
    <td>'+pa[6]+'</td>\
    <td>'+pa[7]+'</td>\
    <td>\
        '+pa[8]+'\
        <a href="/query_detail/?id='+pa[0]+'&doctor='+$("#doctor_name").val()+'&type='+$("#illness_type").val()+'&ptype='+$("#d_type option:selected").val()+'">查看</a>\
    </td>\
    <td>\
        '+pa[9]+'\
        <a href="/query_adetail/?id='+pa[0]+'&doctor='+$("#doctor_a").val()+'&type='+$("#aill_type").val()+'&ptype='+$("#a_type option:selected").val()+'">查看</a>\
    </td>"'    
             }
            $(".contentcol").remove()
            $("#retable").append(st)
            $(".page1").show()
            pnow = 1
            console.log(page)

            st=''
             $(".lpage").remove()
            for(var i=1;i<page+1;i++){
                st+='<li class="lpage" id="ap'+i+'"><a href="javascript:$.selectpage('+i+')">'+i+'</a></li>'
            }
            st+='<li class="lpage">\
        <a href="javascript:$.nextpage(1)" aria-label="Next">\
          <span aria-hidden="true">&raquo;</span>\
        </a>\
      </li>'
            $(".pagination").append(st)
            $("#ap1").attr("class","active lpage")
         },
     });
     return false;
 })