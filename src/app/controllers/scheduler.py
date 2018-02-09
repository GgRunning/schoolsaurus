import requests
from app.models import School, SchedulerLog, OtherSchool, SchoolCCA
from app.factory import SchoolFactory
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test


@transaction.atomic
def insert_school_to_db(school):
    """
    This method is a helper method to insert
    school we get from data.gov.sg API to our database
    """
    mapper = {
        '_id': 'api_id',
        'school_name': 'school_name',
        'url_address': 'url_address',
        'address': 'address',
        'postal_code': 'postal_code',
        'telephone_no': 'telephone_no',
        'telephone_no_2': 'telephone_no_2',
        'fax_no': 'fax_no',
        'fax_no_2': 'fax_no_2',
        'email_address': 'email_address',
        'mrt_desc': 'mrt_desc',
        'bus_desc': 'bus_desc',
        'principal_name': 'principal_name',
        'first_vp_name': 'first_vp_name',
        'second_vp_name': 'second_vp_name',
        'third_vp_name': 'third_vp_name',
        'fourth_vp_name': 'fourth_vp_name',
        'fifth_vp_name': 'fifth_vp_name',
        'visionstatement_desc': 'visionstatement_desc',
        'missionstatement_desc': 'missionstatement_desc',
        'philosophy_culture_ethos': 'philosophy_culture_ethos',
        'dgp_code': 'dgp_code',
        'zone_code': 'zone_code',
        'cluster_code': 'cluster_code',
        'type_code': 'type_code',
        'nature_code': 'nature_code',
        'session_code': 'session_code',
        'mainlevel_code': 'mainlevel_code',
        'sap_ind': 'sap_ind',
        'autonomous_ind': 'autonomous_ind',
        'gifted_ind': 'gifted_ind',
        'ip_ind': 'ip_ind',
        'mothertongue1_code': 'mothertongue1_code',
        'mothertongue2_code': 'mothertongue2_code',
        'mothertongue3_code': 'mothertongue3_code',
        'special_sdp_offered': 'special_sdp_offered'
    }
    school_kwargs = dict()
    for key in school:
        if key in mapper:
            school_kwargs[mapper[key]] = school[key]
        else:
            print('Key not found! ', key)
            # TODO: add error here

    # try to find if school already exists
    try:
        # if exists, check whether the data is updated
        # if the data is not updated, update it and create update log
        if school_kwargs['mainlevel_code'] == 'SECONDARY' or school_kwargs['mainlevel_code'] == 'MIXED LEVEL':
            school = School.objects.get(api_id=school_kwargs['api_id'])
        else:
            school = OtherSchool.objects.get(api_id=school_kwargs['api_id'])
        for key in school_kwargs:
            if school_kwargs[key] != getattr(school, key):
                if school.mainlevel_code == 'SECONDARY' or school.mainlevel_code == 'MIXED LEVEL':
                    new_log = SchedulerLog(
                        school=school,
                        field=key,
                        type='U',
                        previous_data=getattr(school, key),
                        new_data=school_kwargs[key]
                    )
                else:
                    new_log = SchedulerLog(
                        other_school=school,
                        field=key,
                        type='U',
                        previous_data=getattr(school, key),
                        new_data=school_kwargs[key]
                    )
                new_log.save()
                setattr(school, key, school_kwargs[key])
        school.save()
    except (School.DoesNotExist, OtherSchool.DoesNotExist):
        # if does not exists, create a new school, and add new entry log
        new_school = SchoolFactory(school_kwargs)
        new_school.save()
        if new_school.mainlevel_code == 'SECONDARY' or new_school.mainlevel_code == 'MIXED LEVEL':
            new_log = SchedulerLog(
                school=new_school,
                type='N'
            )
        else:
            new_log = SchedulerLog(
                other_school=new_school,
                type='N'
            )
        new_log.save()

def insert_cca_to_db(cca):
    """
    This method is a helper method to insert
    cca we get from data.gov.sg API to our database
    """
    mapper = {
        '_id': 'api_id',
        'school_name': 'school_name',
        'school_section': 'school_section',
        'cca_grouping_desc': 'cca_group',
        'cca_generic_name': 'cca_name',
        'cca_customized_name': 'cca_customized_name'
    }
    cca_kwargs = dict()
    for key in cca:
        if key in mapper:
            cca_kwargs[mapper[key]] = cca[key]
        else:
            print('Key not found! ', key)
            # TODO: add error here

    # try to find if school already exists
    try:
        # if exists, check whether the data is updated
        # if the data is not updated, update it and create update log
        if cca_kwargs['school_section'] == 'SECONDARY' or cca_kwargs['school_section'] == 'MIXED LEVEL':
            school = School.objects.get(school_name=cca_kwargs['school_name'])
        else:
            school = OtherSchool.objects.get(school_name=cca_kwargs['school_name'])

        cca = SchoolCCA.objects.get(api_id=cca_kwargs['api_id'])

        for key in cca_kwargs:
            if cca_kwargs[key] != getattr(cca, key):
                if school.mainlevel_code == 'SECONDARY' or school.mainlevel_code == 'MIXED LEVEL':
                    new_log = SchedulerLog(
                        school=school,
                        field=key,
                        type='U',
                        previous_data=getattr(cca, key),
                        new_data=cca_kwargs[key]
                    )
                else:
                    new_log = SchedulerLog(
                        other_school=school,
                        field=key,
                        type='U',
                        previous_data=getattr(cca, key),
                        new_data=cca_kwargs[key]
                    )
                new_log.save()
                setattr(cca, key, cca_kwargs[key])
        cca.save()
    except (SchoolCCA.DoesNotExist):
        # if does not exists, create a new school, and add new entry log
        new_cca= SchoolCCA(**cca_kwargs)
        new_cca.save()
        if cca_kwargs['school_section'] == 'SECONDARY' or cca_kwargs['school_section'] == 'MIXED LEVEL':
            school = School.objects.get(school_name=new_cca.school_name)
            new_log = SchedulerLog(
                    school=school,
                    type='N',
                    new_data = new_cca.cca_name
                )
        else:
            school = OtherSchool.objects.get(school_name=new_cca.school_name)
            new_log = SchedulerLog(
                    other_school=school,
                    type='N',
                    new_data = new_cca.cca_name
                )
        new_log.save()

    except (School.DoesNotExist, OtherSchool.DoesNotExist):
        pass

@user_passes_test(lambda u: u.is_superuser)
def update_school_data(request):
    # loop until records = 0
    BASE_API_URL = 'https://data.gov.sg{}'
    start_url = BASE_API_URL.format('/api/action/datastore_search?resource_id=ede26d32-01af-4228-b1ed-f05c45a1d8ee')
    response = requests.get(start_url)
    while True:
        if response.status_code == 200:
            data = response.json()
            next_url = data['result']['_links']['next']
            schools_list = data['result']['records']
            if len(schools_list) == 0:
                break
            for school in schools_list:
                insert_school_to_db(school)
            response = requests.get(BASE_API_URL.format(next_url))
        else:
            break
    #insert school cca
    start_url = BASE_API_URL.format('/api/action/datastore_search?resource_id=dd7a056a-49fa-4854-bd9a-c4e1a88f1181')
    response = requests.get(start_url)
    while True:
        if response.status_code == 200:
            data = response.json()
            next_url = data['result']['_links']['next']
            cca_list = data['result']['records']
            if len(cca_list) == 0:
                break
            for cca in cca_list:
                insert_cca_to_db(cca)
            response = requests.get(BASE_API_URL.format(next_url))
        else:
            break

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
