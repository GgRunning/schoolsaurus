from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.dispatch import receiver
from django.conf import settings
from sso.utils import send_email


class BaseSchool(models.Model):
    api_id = models.IntegerField(unique=True, blank=True, null=True, default=None)
    school_name = models.CharField(max_length=200)
    url_address = models.TextField()
    address = models.TextField()
    postal_code = models.TextField()
    telephone_no = models.TextField()
    telephone_no_2 = models.TextField()
    fax_no = models.TextField()
    fax_no_2 = models.TextField()
    email_address = models.TextField()
    mrt_desc = models.TextField()
    bus_desc = models.TextField()
    principal_name = models.TextField()
    first_vp_name = models.TextField()
    second_vp_name = models.TextField()
    third_vp_name = models.TextField()
    fourth_vp_name = models.TextField()
    fifth_vp_name = models.TextField()
    visionstatement_desc = models.TextField()
    missionstatement_desc = models.TextField()
    philosophy_culture_ethos = models.TextField()
    dgp_code = models.TextField()
    zone_code = models.TextField()
    cluster_code = models.TextField()
    type_code = models.TextField()
    nature_code = models.TextField()
    session_code = models.TextField()
    sap_ind = models.TextField()
    autonomous_ind = models.TextField()
    gifted_ind = models.TextField()
    ip_ind = models.TextField()
    mainlevel_code = models.TextField()
    mothertongue1_code = models.TextField()
    mothertongue2_code = models.TextField()
    mothertongue3_code = models.TextField()
    special_sdp_offered = models.TextField()
    lat = models.FloatField(default=None, null=True, blank=True)
    lng = models.FloatField(default=None, null=True, blank=True)
    logo_name = models.CharField(max_length=300, default='no-img.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def get_overall_rating(self):
        return self.schoolcomment_set.all().aggregate(Avg('rating'))['rating__avg']


class OtherSchool(BaseSchool):
    pass


class School(BaseSchool):
    express_nonaff_lower = models.IntegerField(default=None, null=True, blank=True)
    express_nonaff_upper = models.IntegerField(default=None, null=True, blank=True)
    normal_technical_nonaff_upper = models.IntegerField(default=None, null=True, blank=True)
    normal_technical_nonaff_lower = models.IntegerField(default=None, null=True, blank=True)
    normal_academic_nonaff_upper = models.IntegerField(default=None, null=True, blank=True)
    normal_academic_nonaff_lower = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        ordering = ['school_name']


class SchedulerLog(models.Model):
    type = models.CharField(
        max_length=2,
        choices=(
            ('N', 'New Entry'),
            ('U', 'Updated Entry')
        )
    )
    school = models.ForeignKey('app.School', blank=True, null=True, default=None)
    other_school = models.ForeignKey('app.OtherSchool', blank=True, null=True, default=None)
    field = models.CharField(max_length=30)
    previous_data = models.TextField()
    new_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class SchoolCCA(models.Model):
    api_id = models.IntegerField(unique=True, blank=True, null=True, default=None)
    school_name = models.CharField(max_length=200)
    school_section = models.TextField()
    cca_group = models.TextField()
    cca_name = models.TextField()
    cca_customized_name = models.TextField(null=True)

    class Meta:
        ordering = ['school_name']

class SchoolComment(models.Model):
    school = models.ForeignKey('app.School')
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    message = models.TextField()
    created_by = models.ForeignKey('sso.User')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=(
            ('P', 'Pending'),
            ('A', 'Answered')
        ),
        default='P'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class EnquiryAnswer(models.Model):
    enquiry = models.ForeignKey('app.Enquiry')
    answer = models.TextField()
    answered_by = models.ForeignKey('sso.User')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Bookmark(models.Model):
    user = models.ForeignKey('sso.User')
    school = models.ForeignKey('app.School')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ReportComment(models.Model):
    comment = models.ForeignKey('app.SchoolComment')
    reported_by = models.ForeignKey('sso.User')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


@receiver(models.signals.post_save, sender=ReportComment)
def execute_after_save(sender, instance, created, raw, *args, **kwargs):
    if created and not raw:
        # when there is a new report
        for name, email in settings.ADMINS:
            content = 'Hi, {} <br><br> There is a new report submitted. <br><br>' \
                        'Details: <br>' \
                        '{}: {} <br>'
            send_email(
                email,
                'New Report',
                content.format(name, instance.reported_by.get_full_name(), instance.comment.message))
