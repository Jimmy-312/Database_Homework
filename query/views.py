from django.shortcuts import render,redirect
from . import models
from django.http import HttpResponse,JsonResponse
import pymysql
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,'query/index.html')

def query_patient(request):
    if request.method=='POST':
        pid = request.POST.get("patientid")
        datefrom = request.POST.get("datefrom")
        dateto = request.POST.get("dateto")
        bz_type = request.POST.get("ill_bztype")
        jp_type = request.POST.get("jp_type")
        ill_type = request.POST.get("ill_type")
        aill_type = request.POST.get("aill_type")
        ddoctor = request.POST.get("doctor_name")
        adoctor = request.POST.get("doctor_a")
        pages = request.POST.get("ages")
        pagee = request.POST.get("agee")
        psex = request.POST.get("sex")
        hospital = request.POST.get("hospital")

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
            ill = ''
        area_d = [i.areaid for i in models.DArearoi.objects.filter(diseaseid__contains=ill)]

        try:
            aill = models.Anatomydict.objects.get(anatomyname=aill_type).anatomyid
        except:
            aill = ''
        area_a = [i.areaid for i in models.AArearoi.objects.filter(anatomyid__contains=aill)]
        #print(ill)
        try:
            hos = models.HospitalRecord.objects.get(institutename=hospital).instituteid
        except:
            hos = '' 

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
        
        users = users if pid == '' else users.filter(id=pid)    
        users = list(users)
        for i in users:
            u_hos = models.HospitalRecord.objects.get(instituteid=i.hospitalid).institutename
            d_num,a_num = dnum.get(i.patientid),anum.get(i.patientid)
            d_num,a_num = d_num if d_num!=None else 0 ,a_num if a_num!=None else 0
            u_content = [i.id,i.patientname,i.gender,i.age,u_hos,i.checkdate,d_num,a_num]
            patient_list.append(u_content)

        usernum = len(users)
        print(usernum)#,len(patientids_a),len(patientids_d))
        content = {'patient_id':patient_list ,'patient_num':str(usernum),'pid':pid,'date_from':datefrom,'date_to':dateto,'bz_type':bz_type,'jp_type':\
            jp_type,'ill_type':ill_type,'ddoctor':ddoctor,'pages':pages,'pagee':pagee,'psex':psex,'hospital':hospital,'adoctor':adoctor,'aill_type':aill_type}
        return render(request,'query/query_patient.html',content) 
    else:
        return render(request,'query/query_patient.html')


def query_detail(request):
    if request.method == 'POST':
        id = request.POST.get('pid')
        #img_id = request.POST.get('img_id')
        dtype = request.POST.get('bztype')
        doctor = request.POST.get('doctor_name')
        datype = request.POST.get('da_type')

        try:
            daid = models.Diseasedict.objects.get(diseasename=datype).diseaseid
        except:
            daid = ''
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
        return render(request,'query/detail.html',{'id':id,'name':name,'doctor':doctor,'bz_type':dtype,'data':image_list,'counter':num,'title':'疾病','da_type':datype})
    return render(request,'query/detail.html',{'title':'疾病'})

def query_adetail(request):
    if request.method == 'POST':
        id = request.POST.get('pid')
        #img_id = request.POST.get('img_id')
        dtype = request.POST.get('bztype')
        doctor = request.POST.get('doctor_name')
        datype = request.POST.get('da_type')

        try:
            daid = models.Anatomydict.objects.get(anatomyname=datype).anatomyid
        except:
            daid = ''
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
        return render(request,'query/detail.html',{'id':id,'name':name,'doctor':doctor,'bz_type':dtype,'data':image_list,'counter':num,'title':'解剖','ati':'a','da_type':datype})
    return render(request,'query/detail.html',{'title':'解剖','ati':'a'})
    