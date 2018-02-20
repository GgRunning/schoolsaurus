from django.http import HttpResponseRedirect
from django.shortcuts import (
    get_object_or_404,
    render
)
from django.urls import reverse
from app.models import (
    Bookmark, SchoolComment, ReportComment
)
from app.proxy import SecondarySchoolProxy
from sso.models import User
from app.forms import ProfileForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from app import utils
from django.contrib.auth.decorators import login_required


class UserView():
    @login_required
    def bookmark(request, school_id):
        latitude, longitude, has_coordinate = utils.get_coordinate_from_request(request)
        user = request.user
        school = get_object_or_404(SecondarySchoolProxy, id=school_id)
        new_bookmark = Bookmark(
            user=user,
            school=school
        )
        new_bookmark.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @login_required
    def unbookmark(request, school_id):
        latitude, longitude, has_coordinate = utils.get_coordinate_from_request(request)
        user = request.user
        school = get_object_or_404(SecondarySchoolProxy, id=school_id)
        try:
            bookmark = Bookmark.objects.get(user=user, school=school)
            bookmark.delete()
        except Bookmark.DoesNotExist:
            pass
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @login_required
    def bookmark_list(request):
        user = request.user
        bookmark_list = Bookmark.objects.filter(user=user)
        return render(request, 'app/bookmark/indexNew.html', {'bookmark_list': bookmark_list})

    @login_required
    def report_comment(request, comment_id):
        comment = get_object_or_404(SchoolComment, id=comment_id)
        try:
            new_report = ReportComment.objects.get(reported_by=request.user, comment=comment)
        except ReportComment.DoesNotExist:
            messages.success(request, 'This comment is successfully reported. Thank you for informing us!')
            new_report = ReportComment(
                reported_by=request.user,
                comment=comment
            )
            new_report.save()
        return HttpResponseRedirect(reverse('app:school_detail', kwargs={'school_id': comment.school.id}))

    @login_required
    def profile(request):
        password_form = PasswordChangeForm(request.user)
        profile_form = ProfileForm(initial={'email': request.user.email})
        return render(request, 'app/profile/index.html', {'password_form': password_form, 'profile_form': profile_form})

    @login_required
    def change_profile(request):
        user = request.user
        password_form = PasswordChangeForm(request.user)
        profile_form = ProfileForm(request.POST)
        if request.method == 'POST':
            if profile_form.is_valid():
                user.email = request.POST['email']
                user.save()
                messages.success(request, 'Your profile was successfully updated!')
                return HttpResponseRedirect(reverse('app:profile'))
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'app/profile/index.html', {'user': user, 'password_form': password_form, 'profile_form': profile_form})

    @login_required
    def change_password(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(
                    reverse(
                        'app:profile',
                    ),
                )
            else:
                messages.error(request, 'Please correct the error below.')
        return HttpResponseRedirect(reverse('app:profile'))

    @login_required
    def deactivate_account(request):
        user = request.user
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('app:home'))
