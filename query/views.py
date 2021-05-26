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
                return HttpResponseRedirect(next)
            else:
                return render(request,'query/index.html',{"obj":obj,"error":"用户名或密码错误！","st":"l"})
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
                return render(request,'query/index.html',{"obj":obj,"error":"用户名重复，请重试！","st":"r"})
            elif len(hosid)==0:
                return render(request,'query/index.html',{"obj":obj,"error":"医院未涵盖，请重试！","st":"r"})
            else:
                models.User.objects.create(userid=user,age=age,departmentid=dep,username=name,gender=sex,hospitalid=hosid[0].instituteid)
                User.objects.create_user(username=user, password=pwd,first_name=name)
                return render(request,'query/index.html',{"tip":"注册成功,请登录!","st":"l"})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect("/main/")
        if next != '/':
            return render(request,'query/index.html',{"st":"l","error":"请先登录！"})
        return render(request,'query/index.html',{"st":"l"})        

def logout_d(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def mainpage(request):
    #userid = request.user
    #user = userid.first_name
    #print(type(userid),user)
    return render(request,'query/main.html')

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
        users = list(users)
        for i in users:
            u_hos = models.HospitalRecord.objects.get(instituteid=i.hospitalid).institutename
            d_num,a_num = dnum.get(i.patientid),anum.get(i.patientid)
            d_num,a_num = d_num if d_num!=None else 0 ,a_num if a_num!=None else 0
            u_content = [i.id,i.patientname,i.gender,i.age,u_hos,i.checkdate,d_num,a_num,i.checknumber,i.patientid]
            patient_list.append(u_content)

        usernum = len(users)
        print(usernum)#,len(patientids_a),len(patientids_d))
        content = {'patient_id':patient_list ,'patient_num':str(usernum),'obj':obj}
        return render(request,'query/query_patient.html',content) 
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
        patientid = obj.get("patientid")
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
        
        hosid = models.HospitalRecord.objects.filter(institutename=hos)[0].instituteid
        if len(hosid)==0:
                data = {"tip":"医院未涵盖！","class":"danger"}
                return HttpResponse(json.dumps(data))
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
            data = {"tip":f"成功更新患者{name}的信息！","class":"success"}
        
        return HttpResponse(json.dumps(data))

@login_required
def query_detail(request):
    if request.method == 'POST':
        obj = request.POST
        id = obj.get('pid')
        #img_id = request.POST.get('img_id')
        dtype = obj.get('bztype')
        doctor = obj.get('doctor_name')
        datype = obj.get('da_type')

        try:
            daid = models.Diseasedict.objects.get(diseasename=datype).diseaseid
        except:
            daid = '-' if datype.strip() else ''
        areaid = [i.areaid for i in models.DArearoi.objects.filter(diseaseid__contains=daid)]

        pid = list(models.Patientbasicinfos.objects.filter(id=id)) if id.strip() else []
        name = pid[0].patientname if pid!=[] else ''
        pid = pid[0].patientid if pid!=[] else ''
        doctors = models.User.objects.filter(username=doctor)
        doctors = doctors[0].userid if list(doctors)!=[] else ''
    
        images = models.DLabeledimage.objects.filter(patientid__contains=pid,pathtype__contains=dtype,areaid__in=areaid)
        if doctors!='':
            images = images.filter(userid__iexact=doctors)
        image_list = []

        for i in images:
            try:
                patient = models.Patientbasicinfos.objects.get(patientid=i.patientid)
            except:
                return render(request,'query/detail.html',{'title':'病理','error':'数据库错误，我的代码没错'})

            imgpath = models.Imagepath.objects.get(imageid=i.imageid).imgpath
            diseaseids = models.DArearoi.objects.filter(areaid=i.areaid)
            disease = '、'.join([models.Diseasedict.objects.get(diseaseid=i.diseaseid).diseasename for i in diseaseids])
            if datype=='':
                yzx = '请输入疾病类型以检验'
            else:
                yzx = ('一致' if datype in patient.examinationfindings else '不一致') if patient.examinationfindings!= '无' and patient.examinationfindings!='' else '-'
            content=[i.imageid,i.pathtype,models.User.objects.get(userid=i.userid).username,patient.id,patient.patientname,disease,imgpath,yzx] 
            image_list.append(content)

        num = str(len(image_list))
        print(name,num)
        return render(request,'query/detail.html',{'data':image_list,'counter':num,'title':'疾病','obj':obj,'name':name})
    return render(request,'query/detail.html',{'title':'疾病'})

@login_required
def query_adetail(request):
    if request.method == 'POST':
        obj = request.POST
        id = obj.get('pid')
        #img_id = request.POST.get('img_id')
        dtype = obj.get('bztype')
        doctor = obj.get('doctor_name')
        datype = obj.get('da_type')

        try:
            daid = models.Anatomydict.objects.get(anatomyname=datype).anatomyid
        except:
            daid = '-' if datype.strip() else ''
        areaid = [i.areaid for i in models.AArearoi.objects.filter(anatomyid__contains=daid)]

        pid = list(models.Patientbasicinfos.objects.filter(id=id)) if id.strip() else []
        name = pid[0].patientname if pid!=[] else ''
        pid = pid[0].patientid if pid!=[] else ''
        doctors = models.User.objects.filter(username=doctor)
        doctors = doctors[0].userid if list(doctors)!=[] else ''
    
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
            content=[i.imageid,i.pathtype,models.User.objects.get(userid=i.userid).username,patient.id,patient.patientname,disease,imgpath,''] 
            image_list.append(content)

        num = str(len(image_list))
        print(name,num)
        return render(request,'query/detail.html',{'name':name,'data':image_list,'counter':num,'title':'解剖','ati':'a','obj':obj})
    return render(request,'query/detail.html',{'title':'解剖','ati':'a'})
    