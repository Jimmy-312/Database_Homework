    $.selectpage = function(num){
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

    $.getbz = function(ppid) {
         $.ajax({
             url:'/get_'+type+'/',
             type:'POST',
             data:{pid:ppid},
             success: function(data){
                 data = JSON.parse(data)
                 Object.keys(data).map(function(key){
                     $('#edit_form  input').filter(function(){
                         //console.log(this.name,key)
                         return key == this.name;
                     }).val(data[key]);
                     $("#bztype_edit").val(data.bztype)
                 });
             }
         })
     };

     $("#edit_form").submit(function() {
         $.ajax({
             url:'/'+type+'_add/?me=edit',
             type:'POST',
             data:$('#edit_form').serialize(),
             success: function(data){
                 data = JSON.parse(data)
                 $("#tip").attr("class","alert alert-"+data.class)
                 if(data.class == "success"){
                     $("#edit_form")[0].reset()
                 }
                 $("#tip").removeAttr("hidden")
                 $('#editbz').modal('hide')
                 $("#tip_c").text(data.tip)
                 $.getContent()
             },
         });
         return false;
     })

    $("#add_form").submit(function() {
         $.ajax({
             url:'/'+type+'_add/',
             type:'POST',
             data:$('#add_form').serialize(),
             success: function(data){
                 data = JSON.parse(data)
                 $("#tip").attr("class","alert alert-"+data.class)
                 if(data.class == "success"){
                     $("#add_form")[0].reset()
                 }
                 $("#tip").removeAttr("hidden")
                 $('#addbz').modal('hide')
                 $("#tip_c").text(data.tip)
                 $.getContent()
             },
         });
         return false;
     })

     $.delbz = function(pid){
         $.ajax({
             url:'/'+type+'_del/',
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

    $("#query").submit($.getContent = function() {
         $("#bquery").attr("disabled","disabled")
         $("#bquery").val("查询中")
         $.ajax({
             url:'/query_'+type+'/',
             type:'POST',
             data:$('#query').serialize(),
             success: function(data){
                $("#bquery").val("查询")
                $("#bquery").removeAttr("disabled")
                 data = JSON.parse(data)
                 $("#tip2").attr("class","alert alert-"+data.class)
                 $("#tip2").removeAttr("hidden")
                 $("#tip_c2").text("总共查询到"+data.counter+"个符合条件的标注")
                 $("#result").attr("hidden",'')
                //console.log(data)
                if(data.counter>0){$("#result").removeAttr("hidden")}
                 var st=''
                 page=1
                 for(var i=0;i<data.counter;i++){
                     if((i+1)%20==0){
                         page+=1
                     }
                     var pa=data.data[i]
                    st+='<tr class="contentcol page'+page+'" hidden>\
                        <td style="text-align: center;">\
            <a href="javascript:$('+"'#editbz'"+').modal('+"'show'"+');$.getbz('+pa[0]+')">编辑</a>\
            &nbsp;\
            <a href="javascript:$.delbz('+pa[0]+')">删除</a>\
        </td>\
                        <td>'+pa[0]+'</td>\
                        <td>'+pa[1]+'</td>\
                        <td>'+pa[2]+'</td>\
                        <td>'+pa[3]+'</td>\
                        <td>'+pa[4]+'</td>\
                        <td>'+pa[5]+'</td>\
                        <td>'+pa[6]+'</td>\
                        <td>'+pa[7]+'</td>\
                        <td>'+pa[8]+'</td>\
                    </tr>'
                }
                $(".contentcol").remove()
                $("#retable").append(st)
                $(".page1").show()
                pnow = 1
                //console.log(page)

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
                $("#ptname").text(data.name)
            },
            error: function(data){
                $("#tip").attr("class","alert alert-danger")
                $("#tip").removeAttr("hidden")
                $("#tip_c").text("数据库错误，我的代码没错")
            }
        })
            return false;
        })

