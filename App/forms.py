from django import forms
from . import models
from django.core.exceptions import ValidationError


SCHOOL = [
    ("Sammopur","Sammopur"),
    ("NA","Other"),
]

def getID():
    d = f"STXS{models.IdMonitor.objects.all()[0].current}"
    return d

class RegisterForm(forms.Form):

    a = [("NA","Select"), *((act.id, act.name) for act in models.Activities.objects.all())]
    t = [("NA","Select"), *((time.id, time) for time in models.TimeSlots.objects.all())]


    student_id = forms.CharField(label="Student id",initial=getID, disabled=True,widget=forms.TextInput(attrs={'class':'input input-bordered'}))
    school_name = forms.CharField(label="School name",widget=forms.Select(attrs={'class':'input input-bordered'}, choices=SCHOOL))
    
    other_school_name = forms.CharField(label="Other School name",widget=forms.TextInput(attrs={'class':'input input-bordered'}), required=False)
    image = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'input input-bordered hidden'} ))
    
    name = forms.CharField(label="Name",widget=forms.TextInput(attrs={'class':'input input-bordered'}))
    gender = forms.CharField(label="Gender",widget=forms.Select( choices=models.GENDER,attrs={'class':'input input-bordered'}))
    Class = forms.CharField(label="Class",widget=forms.Select( choices=models.Klass,attrs={'class':'input input-bordered'}))
    
    contact_number  = forms.CharField(label="Contact",widget=forms.TextInput(attrs={'class':'input input-bordered'}))
    guradian_name  = forms.CharField(label="Guardian Name",widget=forms.TextInput(attrs={'class':'input input-bordered'}))

    activity1 = forms.CharField(label="Activity 1", widget=forms.Select(choices=a,attrs={'class':'input input-bordered'}))
    time1 = forms.CharField(label="Time", widget=forms.Select(choices= t,attrs={'class':'input input-bordered'}))

    activity2 = forms.CharField(label="Activity 2", widget=forms.Select(choices=a,attrs={'class':'input input-bordered'}))
    time2 = forms.CharField(label="Time", widget=forms.Select(choices= t,attrs={'class':'input input-bordered'}))

    activity3 = forms.CharField(label="Activity 3", widget=forms.Select(choices=a,attrs={'class':'input input-bordered'}))
    time3 = forms.CharField(label="Time", widget=forms.Select(choices= t,attrs={'class':'input input-bordered'}))


    def clean_contact_number(self):
        data = str(self.cleaned_data["contact_number"])

        if len(data) != 10:
            raise ValidationError("Invalid contact number")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        act1 = cleaned_data["activity1"]
        act2 = cleaned_data["activity2"]
        act3 = cleaned_data["activity3"]
    
        time1 = cleaned_data["time1"]
        time2 = cleaned_data["time2"]
        time3 = cleaned_data["time3"]

        for act,time in zip((act1,act2,act3), (time1,time2,time3)):
            self.verify_activity(act,time)

    def verify_activity(self, act, time):
        act = models.Activities.objects.get( id=act)   
        time = models.TimeSlots.objects.get(id=time)
        obj = models.Participations.objects.filter(activity=act, time= time)
        if len(obj) >= 30:
            
            raise ValidationError({"time3":"%s not available for time slot %s" %(act,time)})
        return act
    

class UpdateForm(RegisterForm):
    student_id = forms.CharField(label="Student id",widget=forms.TextInput(attrs={'class':'input input-bordered','readonly':True},))
    # image = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'input input-bordered hidden'} ))

class PrintForm(RegisterForm):
    other_school_name = ""
    school_name = forms.CharField(label="School name",widget=forms.TextInput(attrs={'class':'input input-bordered'}))
