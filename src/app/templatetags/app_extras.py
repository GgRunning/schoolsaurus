from django import template
from app.models import ReportComment

register = template.Library()


@register.filter(name='is_bookmarked')
def is_bookmarked(school, user):
    return school.bookmark_set.filter(user=user).exists()


@register.filter(name='is_compared')
def is_compared(school, request):
    compare_school_id_list = request.session.get('compare_school_id_list', [])
    return str(school.id) in compare_school_id_list


@register.filter(name='is_not_reported_by')
def is_not_reported_by(comment, user):
    return not ReportComment.objects.filter(comment=comment, reported_by=user).exists()
