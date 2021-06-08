from django.shortcuts import render
from . import models
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt
def index(request):
    next = request.GET.get('next', '/')
    if request.method=='POST':
        obj = request.POST
        st = obj.get("st")
        if st=='l':
            user = obj.get("user")
            if user==None:
                return render(request,'query/index.html',{"obj":obj,"st":"l"})
            pwd = obj.get("pwd")
            logininfo = authenticate(username=user, password=pwd)
            if logininfo != None:
                login(request,logininfo)
                data = {"tip":"登录成功，正在跳转...","class":"success","url":next}
                return HttpResponse(json.dumps(data))
            else:
                data = {"tip":"用户名或密码错误！","class":"danger"}
                return HttpResponse(json.dumps(data))
            #print(request.user.is_authenticated)
        else:
            user = obj.get("user")
            if user==None:
                return render(request,'query/index.html',{"obj":obj,"st":"r"})
            pwd = obj.get("pwd")
            sex = obj.get("sex")
            age = obj.get("age")
            name = obj.get("name")
            dep = obj.get("dep")
            hos = obj.get("hos")

            hosid = models.HospitalRecord.objects.filter(institutename=hos)
            state = models.User.objects.filter(userid__exact=user)
            if len(state)!=0:
                data = {"tip":"用户名重复，请重试！","class":"danger"}
                return HttpResponse(json.dumps(data))
            elif len(hosid)==0:
                data = {"tip":"医院未涵盖，请重试！","class":"danger"}
                return HttpResponse(json.dumps(data))
            else:
                models.User.objects.create(userid=user,age=age,departmentid=dep,username=name,gender=sex,hospitalid=hosid[0].instituteid)
                User.objects.create_user(username=user, password=pwd,first_name=name)
                data = {"tip":"注册成功,请登录!","class":"success"}
                return HttpResponse(json.dumps(data))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect("/main/")
        if next != '/':
            return render(request,'query/index.html',{"st":"l","error":"请先登录！"})
        return render(request,'query/index.html')        

def logout_d(request):
    logout(request)
    return HttpResponseRedirect("/")

@csrf_exempt
def getinfo(request):
    doc = len(models.User.objects.all())
    hos = len(models.HospitalRecord.objects.all())
    pat = len(models.Patientbasicinfos.objects.all())
    dis = len(models.DLabeledimage.objects.all())
    bz = len(models.ALabeledimage.objects.all())

    data = {"doc":doc,"hos":hos,"pat":pat,"dis":dis,"bz":bz}
    return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def getuser(request):
    if request.method == "POST":
        userid = request.user
        user = models.User.objects.get(userid=userid)
        hos = models.HospitalRecord.objects.get(instituteid=user.hospitalid).institutename
        level = request.user.is_staff

        data = {'id':user.userid,"name":user.username,"age":user.age,"gender":user.gender,"hos":hos,"dep":user.departmentid,"level":level}
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def editpass(request):
    if request.method == "POST":
        old = request.POST.get("old")
        new = request.POST.get("new")

        user = authenticate(username=request.user, password=old)
        if user == None:
            data = {"class":"danger"}
        else:
            user.set_password(new)
            user.save()
            login(request,user)
            data = {"class":"success"}
        
        return HttpResponse(json.dumps(data))
        

@csrf_exempt
@login_required
def edituser(request):
    if request.method == "POST":
        obj = request.POST
        name = obj.get("name")
        sex = obj.get("sex")
        age = obj.get("age")
        hos = obj.get("hos")
        dep = obj.get("dep")

        hosid = models.HospitalRecord.objects.get(institutename=hos).instituteid
        models.AuthUser.objects.filter(username=request.user).update(first_name=name)
        models.User.objects.filter(userid=request.user).update(username=name,gender=sex,age=age,hospitalid=hosid,departmentid=dep)
        data = {"class":"success"}
        return HttpResponse(json.dumps(data))

@login_required
def mainpage(request):
    #userid = request.user
    #user = userid.first_name
    #print(type(userid),user)
    return render(request,'query/main.html')

@csrf_exempt
def get_hos(request):
    if request.method=="POST":
        hos = models.HospitalRecord.objects.all()
        data = [i.institutename for i in hos]
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def get_doc(request):
    if request.method=="POST":
        doctor = models.User.objects.all()
        data = [i.username for i in doctor]
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def get_patient(request):
    if request.method=='POST':
        pid = request.POST.get("pid")
        patient = models.Patientbasicinfos.objects.get(id=pid)
        hos = models.HospitalRecord.objects.get(instituteid=patient.hospitalid).institutename
        checkdate = datetime.strftime(patient.checkdate,"%Y-%m-%d")
        data = {"name":patient.patientname,"sex":patient.gender,"age":patient.age,"hos":hos,"checkdate":checkdate,\
            "checkid":patient.checknumber,"pid":patient.patientid,"id":patient.id}
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def get_detail(request):
    if request.method=='POST':
        pid = request.POST.get("pid")
        bz = models.DLabeledimage.objects.get(id=pid)
        ppid = models.Patientbasicinfos.objects.get(patientid=bz.patientid).id
        doctor = models.User.objects.get(userid=bz.userid).username
        data = {"bzid":pid,"name":ppid,"areaid":bz.areaid,"imageid":bz.imageid,"bztype":bz.pathtype,"doctor":doctor}
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def get_adetail(request):
    if request.method=='POST':
        pid = request.POST.get("pid")
        bz = models.ALabeledimage.objects.get(id=pid)
        ppid = models.Patientbasicinfos.objects.get(patientid=bz.patientid).id
        doctor = models.User.objects.get(userid=bz.userid).username
        data = {"bzid":pid,"name":ppid,"areaid":bz.areaid,"imageid":bz.imageid,"bztype":bz.pathtype,"doctor":doctor}
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def del_patient(request):
    if request.method=='POST':
        pid = request.POST.get("pid") 
        patient = models.Patientbasicinfos.objects.get(id=pid)
        pid = patient.patientid
        name = patient.patientname
        patient.delete()
        models.DLabeledimage.objects.filter(patientid=pid).delete()
        models.ALabeledimage.objects.filter(patientid=pid).delete()
        data = {"class":"success","tip":f"成功删除患者{name}"}
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def query_patient(request):
    if request.method=='POST':
        obj = request.POST
        pid = obj.get("patientid")
        datefrom = obj.get("datefrom")
        dateto = obj.get("dateto")
        bz_type = obj.get("ill_bztype")
        jp_type = obj.get("jp_type")
        ill_type = obj.get("ill_type")
        aill_type = obj.get("aill_type")
        ddoctor = obj.get("doctor_name")
        adoctor = obj.get("doctor_a")
        pages = obj.get("ages")
        pagee = obj.get("agee")
        psex = obj.get("sex")
        hospital = obj.get("hospital")
        patientname = obj.get("patientname")

        patient_list=[]
        datefrom = datefrom if datefrom.strip() else "1990-01-01"
        dateto = dateto if dateto.strip() else "2050-01-01"
        date_from = datetime.strptime(datefrom, "%Y-%m-%d")
        date_to = datetime.strptime(dateto, "%Y-%m-%d")
        pages,pagee = pages if pages!='' else 0,pagee if pagee!='' else 120
        page = [int(pages),int(pagee)]
        try:
            ill = models.Diseasedict.objects.get(diseasename=ill_type).diseaseid
        except:
            ill = '-' if ill_type.strip() else ''
        area_d = [i.areaid for i in models.DArearoi.objects.filter(diseaseid__contains=ill)]

        try:
            aill = models.Anatomydict.objects.get(anatomyname=aill_type).anatomyid
        except:
            aill = '-' if aill_type.strip() else ''
        area_a = [i.areaid for i in models.AArearoi.objects.filter(anatomyid__contains=aill)]

        try:
            hos = models.HospitalRecord.objects.get(institutename=hospital).instituteid
        except:
            hos = '-' if hospital.strip() else ''

        try:
            user_d = models.User.objects.get(username=ddoctor)
            ddoctors = user_d.userid
        except:
            ddoctors = '-' if ddoctor!='' else ''

        try:
            user_a = models.User.objects.get(username=adoctor)
            adoctors = user_a.userid
        except:
            adoctors = '-' if adoctor!='' else ''
        
        patients = models.DLabeledimage.objects.filter(areaid__in=area_d,pathtype__contains=bz_type)
        if ddoctor!='':
            patients = patients.filter(userid__iexact=ddoctors) if ddoctors!='-' else [] 
        cont = [i.patientid for i in patients]
        patients = list(set(cont))
        patientids_d = patients
        dnum = dict(zip(patients,[cont.count(i) for i in patients]))      

        patients = models.ALabeledimage.objects.filter(areaid__in=area_a,pathtype__contains=jp_type)
        if adoctor!='':
            patients = patients.filter(userid__iexact=adoctors) if adoctors!='-' else [] 
        anum = len(patients)
        cont = [i.patientid for i in patients]
        patients = list(set(cont))
        patientids_a = patients         
        anum = dict(zip(patients,[cont.count(i) for i in patients])) 
        
        users = models.Patientbasicinfos.objects.filter(checkdate__range=(date_from,date_to),hospitalid__contains=hos,gender__contains=psex,age__range=page)

        if bz_type.strip() or jp_type.strip() or ill_type.strip() or ddoctor.strip() or adoctor.strip() or aill_type.strip():
            if bz_type=='' and ddoctor=='' and ill_type=='':
                patientids=patientids_a
            elif jp_type=='' and adoctor=='' and aill_type=='':
                patientids=patientids_d
            else:
                patientids=list(set([i for i in patientids_d if i in patientids_a]))
            users = users.filter(patientid__in=patientids)
        
        users = users if not pid.strip() else users.filter(id=pid)    
        users = users if not patientname.strip() else users.filter(patientname=patientname)   
        users = list(users)
        for i in users:
            u_hos = models.HospitalRecord.objects.get(instituteid=i.hospitalid).institutename
            d_num,a_num = dnum.get(i.patientid),anum.get(i.patientid)
            d_num,a_num = d_num if d_num!=None else 0 ,a_num if a_num!=None else 0
            u_content = [i.id,i.patientid,i.patientname,i.gender,i.age,u_hos,datetime.strftime(i.checkdate,"%Y-%m-%d"),i.checknumber,d_num,a_num]
            patient_list.append(u_content)

        usernum = len(users)
        print(usernum)#,len(patientids_a),len(patientids_d))
        box = "success" if usernum>0 else "warning"
        data = {'patient_id':patient_list ,'patient_num':str(usernum),'obj':obj,"class":box}
        return HttpResponse(json.dumps(data))
    else:
        return render(request,'query/query_patient.html')

@csrf_exempt
def patient_add(request):
    if request.method == 'POST':
        obj = request.POST
        name = obj.get("name")
        sex = obj.get("sex")
        date = obj.get("checkdate")
        checkid = obj.get("checkid")
        age = obj.get("age")
        patientid = obj.get("pid")
        id = obj.get("id")
        hos = obj.get("hos")

        meth = request.GET.get('me', '')
        if meth=='':
            if id.strip():
                state = models.Patientbasicinfos.objects.filter(id__exact=id)
                if len(state)!=0:
                    data = {"tip":"病人id重复！","class":"danger"}
                    return HttpResponse(json.dumps(data))
            
            state = models.Patientbasicinfos.objects.filter(patientid__exact=patientid)
            if len(state)!=0:
                    data = {"tip":"病人编号重复！","class":"danger"}
                    return HttpResponse(json.dumps(data))
        
        hosid = models.HospitalRecord.objects.filter(institutename=hos)
        if len(hosid)==0:
                data = {"tip":"医院未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        hosid = hosid[0].instituteid
        print(date)
        date = datetime.strptime(date,"%Y-%m-%d")
        if meth=='':
            try:
                if id.strip():
                    models.Patientbasicinfos.objects.create(hospitalid=hosid,patientid=patientid,id=id,gender=sex,age=age,checkdate=date,checknumber=checkid,patientname=name)
                else:
                    models.Patientbasicinfos.objects.create(hospitalid=hosid,patientid=patientid,gender=sex,age=age,checkdate=date,checknumber=checkid,patientname=name)
                data = {"tip":f"成功添加患者{name}！","class":"success"}
            except:
                data = {"tip":"添加失败，请重试！","class":"danger"}
        else:
            models.Patientbasicinfos.objects.filter(id=id).update(hospitalid=hosid,id=id,gender=sex,age=age,checkdate=date,checknumber=checkid,patientname=name)
            data = {"tip":f"成功更新患者{name}的信息！","class":"success","pid":id,"obj":obj}
        
        return HttpResponse(json.dumps(data))

@csrf_exempt
def detail_add(request):
    if request.method == 'POST':
        obj = request.POST
        name = obj.get("name")
        doctor = obj.get("doctor")
        areaid = obj.get("areaid")
        bztype = obj.get("bztype")
        imgid = obj.get("imageid")
        id = obj.get("bzid")

        meth = request.GET.get('me', '')
        if meth=='':
            if id.strip():
                state = models.DLabeledimage.objects.filter(id__exact=id)
                if len(state)!=0:
                    data = {"tip":"标注id重复！","class":"danger"}
                    return HttpResponse(json.dumps(data))
        
        doctorid = models.User.objects.filter(username=doctor)
        if len(doctorid)==0:
                data = {"tip":"医生未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        doctorid = doctorid[0].userid

        pid = models.Patientbasicinfos.objects.filter(id=name)
        if len(pid)==0:
                data = {"tip":"患者未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        pid = pid[0].patientid

        areaid = models.DArearoi.objects.filter(areaid=areaid)
        if len(areaid)==0:
                data = {"tip":"区域未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        areaid = areaid[0].areaid

        img = models.Imagepath.objects.filter(imageid=imgid)
        if len(img)==0:
                data = {"tip":"图像未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        img = imgid

        if meth=='':
            try:
                if id.strip():
                    models.DLabeledimage.objects.create(id=id,areaid=areaid,userid=doctorid,pathtype=bztype,imageid=img,patientid=pid)
                else:
                    models.DLabeledimage.objects.create(areaid=areaid,userid=doctorid,pathtype=bztype,imageid=img,patientid=pid)
                data = {"tip":f"成功添加疾病标注{id}！","class":"success"}
            except:
                data = {"tip":"添加失败，请重试！","class":"danger"}
        else:
            models.DLabeledimage.objects.filter(id=id).update(areaid=areaid,userid=doctorid,pathtype=bztype,imageid=img,patientid=pid)
            data = {"tip":f"成功更新疾病标注{id}的信息！","class":"success","pid":id,"obj":obj}
        
        return HttpResponse(json.dumps(data))

@csrf_exempt
def adetail_add(request):
    if request.method == 'POST':
        obj = request.POST
        name = obj.get("name")
        doctor = obj.get("doctor")
        areaid = obj.get("areaid")
        bztype = obj.get("bztype")
        imgid = obj.get("imageid")
        id = obj.get("bzid")

        meth = request.GET.get('me', '')
        if meth=='':
            if id.strip():
                state = models.ALabeledimage.objects.filter(id__exact=id)
                if len(state)!=0:
                    data = {"tip":"标注id重复！","class":"danger"}
                    return HttpResponse(json.dumps(data))
        
        doctorid = models.User.objects.filter(username=doctor)
        if len(doctorid)==0:
                data = {"tip":"医生未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        doctorid = doctorid[0].userid

        pid = models.Patientbasicinfos.objects.filter(id=name)
        if len(pid)==0:
                data = {"tip":"患者未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        pid = pid[0].patientid

        areaid = models.AArearoi.objects.filter(areaid=areaid)
        if len(areaid)==0:
                data = {"tip":"区域未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        areaid = areaid[0].areaid

        img = models.Imagepath.objects.filter(imageid=imgid)
        if len(img)==0:
                data = {"tip":"图像未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
        img = imgid

        if meth=='':
            try:
                if id.strip():
                    models.ALabeledimage.objects.create(id=id,areaid=areaid,userid=doctorid,pathtype=bztype,imageid=img,patientid=pid)
                else:
                    models.ALabeledimage.objects.create(areaid=areaid,userid=doctorid,pathtype=bztype,imageid=img,patientid=pid)
                data = {"tip":f"成功添加解剖标注{id}！","class":"success"}
            except:
                data = {"tip":"添加失败，请重试！","class":"danger"}
        else:
            models.ALabeledimage.objects.filter(id=id).update(areaid=areaid,userid=doctorid,pathtype=bztype,imageid=img,patientid=pid)
            data = {"tip":f"成功更新解剖标注{id}的信息！","class":"success","pid":id,"obj":obj}
        
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def query_detail(request):
    if request.method == 'POST':
        obj = request.POST
        #print(obj)
        id = obj.get('pid')
        #img_id = request.POST.get('img_id')
        dtype = obj.get('bztype')
        doctor = obj.get('doctor')
        datype = obj.get('da_type')

        try:
            daid = models.Diseasedict.objects.get(diseasename=datype).diseaseid
        except:
            daid = '-' if datype.strip() else ''
        areaid = [i.areaid for i in models.DArearoi.objects.filter(diseaseid__contains=daid)]

        pid = list(models.Patientbasicinfos.objects.filter(id=id)) if id.strip() else ['-']
        if pid == []:
            data = {'data':[],'counter':0,'name':'未指定患者','class':"warning"}
            return HttpResponse(json.dumps(data))

        name = pid[0].patientname if pid!=['-'] else '未指定患者'
        pid = pid[0].patientid if pid!=['-'] else ''

        doctors = list(models.User.objects.filter(username=doctor)) if doctor.strip() else ['-']
        if doctors == []:
            data = {'data':[],'counter':0,'name':'未指定患者','class':"warning"}
            return HttpResponse(json.dumps(data))
        doctors = doctors[0].userid if doctors!=['-'] else ''
    
        images = models.DLabeledimage.objects.filter(patientid__contains=pid,pathtype__contains=dtype,areaid__in=areaid)
        if doctors!='':
            images = images.filter(userid__iexact=doctors)
        image_list = []

        for i in images:
            try:
                patient = models.Patientbasicinfos.objects.get(patientid=i.patientid)
            except:
                return HttpResponse('数据库错误，我的代码没错', status=401)

            imgpath = models.Imagepath.objects.get(imageid=i.imageid).imgpath
            diseaseids = models.DArearoi.objects.filter(areaid=i.areaid)
            disease = '、'.join([models.Diseasedict.objects.get(diseaseid=i.diseaseid).diseasename for i in diseaseids])
            '''if datype=='':
                yzx = '请输入疾病类型以检验'
            else:
                yzx = ('一致' if datype in patient.examinationfindings else '不一致') if patient.examinationfindings!= '无' and patient.examinationfindings!='' else '-'
            '''
            content=[i.id,i.imageid,i.pathtype,models.User.objects.get(userid=i.userid).username,patient.id,patient.patientname,disease,i.areaid,imgpath] 
            image_list.append(content)

        num = len(image_list)
        sym = "success" if num>0 else "warning"
        print(name,num)

        data = {'data':image_list,'counter':str(num),'name':name,'class':sym}
        return HttpResponse(json.dumps(data))
    else:
        obj = request.GET
        return render(request,'query/detail.html',{'title':'疾病',"type":"detail","obj":obj})
    

@csrf_exempt
@login_required
def query_adetail(request):
    if request.method == 'POST':
        obj = request.POST
        print(obj)
        id = obj.get('pid')
        #img_id = request.POST.get('img_id')
        dtype = obj.get('bztype')
        doctor = obj.get('doctor')
        datype = obj.get('da_type')

        try:
            daid = models.Anatomydict.objects.get(anatomyname=datype).anatomyid
        except:
            daid = '-' if datype.strip() else ''
        areaid = [i.areaid for i in models.AArearoi.objects.filter(anatomyid__contains=daid)]

        pid = list(models.Patientbasicinfos.objects.filter(id=id)) if id.strip() else ['-']
        if pid == []:
            data = {'data':[],'counter':0,'name':'未指定患者','class':"warning"}
            return HttpResponse(json.dumps(data))

        name = pid[0].patientname if pid!=['-'] else '未指定患者'
        pid = pid[0].patientid if pid!=['-'] else ''

        doctors = list(models.User.objects.filter(username=doctor)) if doctor.strip() else ['-']
        if doctors == []:
            data = {'data':[],'counter':0,'name':'未指定患者','class':"warning"}
            return HttpResponse(json.dumps(data))
        doctors = doctors[0].userid if doctors!=['-'] else ''
    
        images = models.ALabeledimage.objects.filter(patientid__contains=pid,pathtype__contains=dtype,areaid__in=areaid)
        if doctors!='':
            images = images.filter(userid__iexact=doctors)
        image_list = []

        for i in images:
            try:
                patient = models.Patientbasicinfos.objects.get(patientid=i.patientid)
            except:
                return render(request,'query/detail.html',{'title':'解剖','error':'数据库错误，我的代码没错','ati':'a'})
            imgpath = models.Imagepath.objects.get(imageid=i.imageid).imgpath
            diseaseids = models.AArearoi.objects.filter(areaid=i.areaid)
            disease = '、'.join([models.Anatomydict.objects.get(anatomyid=i.anatomyid).anatomyname for i in diseaseids])
            content=[i.id,i.imageid,i.pathtype,models.User.objects.get(userid=i.userid).username,patient.id,patient.patientname,disease,i.areaid,imgpath] 
            image_list.append(content)

        num = len(image_list)
        sym = "success" if num>0 else "warning"
        print(name,num)

        data = {'data':image_list,'counter':str(num),'name':name,'class':sym}
        return HttpResponse(json.dumps(data))
    else:
        obj = request.GET
        return render(request,'query/detail.html',{'title':'解剖',"type":"adetail","obj":obj})


@csrf_exempt
@login_required
def detail_del(request):
    if request.method == "POST":
        pid = request.POST.get("pid")
        models.DLabeledimage.objects.get(id=pid).delete()
        data = {"class":"success","tip":f"成功删除疾病标注{pid}"}
        return HttpResponse(json.dumps(data))

@csrf_exempt
@login_required
def adetail_del(request):
    if request.method == "POST":
        pid = request.POST.get("pid")
        models.ALabeledimage.objects.get(id=pid).delete()
        data = {"class":"success","tip":f"成功删除解剖标注{pid}"}
        return HttpResponse(json.dumps(data))