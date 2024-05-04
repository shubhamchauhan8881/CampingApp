from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from . import forms
from . import models
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def Home(request):
    # event_list = models.Activities.objects.all()
    # time_slots = models.TimeSlots.objects.all()

    # res = []

    # for a in event_list:
    #     temp = []
    #     for t in time_slots:
    #         o = 30 - models.Participations.objects.filter(activity=a, time=t).count()
            
    #         if o <= 0:
    #             temp.append((t, "No available"))
    #         else:
    #             temp.append((t,o))
    #     res.append([a,temp])
    
    # print(res)    

    recents = models.Student.objects.all()[:10]
    form = forms.RegisterForm()
    return render(request, 'index.html', {'form': form, 'recents': recents})


 


@csrf_exempt
def SendStData(request, Id):
    data = models.Student.objects.filter(student_id=Id)
    
    response = {'status': 'success'}
    if not data:
        response['status']:'failed'
    else: 
        data = data[0]
        a = ', '.join([f"{x.activity.name} ({x.time})" for x in models.Participations.objects.filter(student=data) ])

        response['data'] = {
            "id": data.student_id,
            'name':data.student_name,
            'gender':data.student_gender,
            'class':data.Class,
            'guardian':data.guradian_name,
            'phone':data.contact_number,
            'activities':a,
            'image':data.image.url if data.image else "",

        }
    return JsonResponse(response)


def Delete(request, Id):
    st = models.Student.objects.filter(student_id=Id)
    messages.success(request,f"{st[0].student_name} was deleted successfully!.")
    st.delete()
    return redirect('index')


def ListAll(request):
    records = []
    st = models.Student.objects.all()
    for s in st:
        p = models.Participations.objects.filter(student = s)
        records.append( (s, p) )

    return render(request, 'all.html', {"records": records})

def render_to_pdf(context_dict={}):
    template = get_template("reciept.html")
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{context_dict["st"].student_name}.pdf"'
    return response


def Print(request, Id):
    student = models.Student.objects.get(student_id=Id, )
    act = models.Participations.objects.filter(student=student)
    form = forms.RegisterForm(data = 
    {
        "name":student.student_name,
        "school_name":student.school_name,
        "gender":student.student_gender,
        "Class":student.Class,
        "contact_number":student.contact_number,
        "guradian_name":student.guradian_name,
        "activity1":act[0].activity.id,
        "activity2":act[1].activity.id,
        "activity3":act[2].activity.id,

        "time1":act[0].time.id,
        "time2":act[1].time.id,
        "time3":act[2].time.id,
        
    })
    # actt = models.Participations.objects.filter(student=student)
    # pdf = render_to_pdf({'st':student, 'act':actt})
    # return pdf

    return render(request, 'reciept.html', {'form': form,  "image":student.image.url,})

def generateStudentId():
    while True:
        res = models.IdMonitor.objects.all()[0]
        d = f"STXS{res.current}"
        res.current += 1
        # # check if taken
        # if models.Student.objects.filter(student_id=d).exists():
        #     d = f"STXS{res.current}"
        
        res.save()
        return d

def Enroll(request):
    if request.method == 'POST':
        form = forms.RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            st = models.Student.objects.create(
                student_id = generateStudentId(),
                school_name = form.cleaned_data['school_name'] if form.cleaned_data['school_name'] != "NA" else form.cleaned_data['other_school_name'],
                image = form.cleaned_data['image'],
                student_name =form.cleaned_data['name'],
                student_gender = form.cleaned_data['gender'],
                Class =form.cleaned_data['Class'],
                guradian_name = form.cleaned_data['guradian_name'],
                contact_number = form.cleaned_data['contact_number'],

            )

            act1 = form.cleaned_data["activity1"]
            act2 = form.cleaned_data["activity2"]
            act3 = form.cleaned_data["activity3"]
        
            time1 = form.cleaned_data["time1"]
            time2 = form.cleaned_data["time2"]
            time3 = form.cleaned_data["time3"]

            
            for act,time in zip((act1,act2,act3), (time1,time2,time3)):
                act = models.Activities.objects.get( id=act)
                time = models.TimeSlots.objects.get(id=time)
                pt = models.Participations.objects.create(
                    student=st,
                    activity=act,
                    time = time
                )
            
            messages.success(request, f"{st.student_name} was added successfully!")
            return redirect("index")
        else:
            print("error", form.errors)
            return render(request, 'index.html', {'form': form}) 
  