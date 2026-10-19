from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileUpdateForm
from applications.models import Application

@login_required
def user_profile(request):
    user = request.user
    applications = Application.objects.filter(user=user).select_related('course').order_by('-created_at')

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect('user_profile')
    else:
        form = UserProfileUpdateForm(instance=user)

    context = {
        'form': form,
        'applications': applications,
    }
    return render(request, 'accounts/profile.html', context)
