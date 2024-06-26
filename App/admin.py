from django.contrib import admin
from . import models
from django.conf import settings
import csv
from django.http import HttpResponse
# Register your models here.

# @admin.action(export, description="Export")
# def export():
#     pass
@admin.action(description="Export")
def export(modeladmin, request, queryset):
    headers = ["Id", "Student Name", "Gender","Class", "Guardian", "Contact","School Name","Activity 1","Time 1", "Activity 2","Time 2", "Activity 3","Time 3"]
    with open(f"{settings.BASE_DIR}/static/temp.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, )
        writer.writerow(headers)
        for st in queryset:
            a = models.Participations.objects.filter(student=st)
            temp = [
                st.student_id,
                st.student_name, 
                st.student_gender,
                st.Class,
                st.guradian_name,
                st.contact_number,
                st.school_name if st.school_name else st.other_school_name,
                a[0].activity.name,
                a[0].time,

                a[1].activity.name,
                a[1].time,

                a[2].activity.name,
                a[2].time,
                   
            ]
            writer.writerow(temp)
    response = HttpResponse(open(f"{settings.BASE_DIR}/static/temp.csv", "r",).read(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="student.csv"'
    return response


@admin.action(description="Export")
def exportp(modeladmin, request, queryset):
    headers = ["Student Name", "Gender","Class", "Guardian", "Contact", "Activity "]
    with open(f"{settings.BASE_DIR}/static/temp.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for part in queryset:
            temp = [
                part.student.student_name, 
                part.student.student_gender,
                part.student.Class,
                part.student.guradian_name,
                part.student.contact_number,
                f"{part.activity} ({part.time})"
            ]
            writer.writerow(temp)

    response = HttpResponse(open(f"{settings.BASE_DIR}/static/temp.csv", "r",).read(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="participations.csv"'
    return response


class StudentAdmin(admin.ModelAdmin):
    list_display = ["student_name","student_gender","Class","contact_number","Participation"]
    search_fields = ["student_name"]
    list_filter = ["Class"]
    actions = (export, )
    def Participation(self, query):
        n = ""
        participations = models.Participations.objects.filter(student=query)
        for p in participations: 
            # print(p.activity.name,str(p.time))
            n += p.activity.name +", \n"
        return n


class ParticipationAdmin(admin.ModelAdmin):
    list_filter = ["activity"]
    actions = (exportp, )

admin.site.register(models.Activities)
admin.site.register(models.Branch)
admin.site.register(models.IdMonitor)
admin.site.register(models.TimeSlots)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Participations,ParticipationAdmin)