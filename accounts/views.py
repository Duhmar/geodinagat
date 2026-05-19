from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Report, Profile, ReportMedia, Comment
from .forms import ReportForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
import json

# 1. Home Page
def home(request):
    reports = Report.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    
    if query:
        reports = reports.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    return render(request, 'home.html', {'reports': reports})

# 2. Profile Page
@login_required
def profile_view(request):
    user_reports = Report.objects.filter(author=request.user)
    
    total_uploads = user_reports.count()
    total_likes = sum(report.likes.count() for report in user_reports)
    
    context = {
        'total_uploads': total_uploads,
        'total_likes': total_likes,
    }
    return render(request, 'accounts/profile.html', context)

# 3. Signup Logic
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('report_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# 4. Activity Logs (List)
@login_required
def report_list(request):
    reports = Report.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})

# 5. Create New Entry
@login_required
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        files = request.FILES.getlist('extra_media')
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            
            for f in files:
                is_vid = f.name.lower().endswith(('.mp4', '.mov', '.avi'))
                ReportMedia.objects.create(report=report, file=f, is_video=is_vid)
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'reports/report_form.html', {'form': form, 'title': 'New Activity'})

# 6. Update Entry
@login_required
def report_update(request, pk):
    report = get_object_or_404(Report, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        files = request.FILES.getlist('extra_media')
        if form.is_valid():
            form.save()
            
            for f in files:
                is_vid = f.name.lower().endswith(('.mp4', '.mov', '.avi'))
                ReportMedia.objects.create(report=report, file=f, is_video=is_vid)
            
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'reports/report_form.html', {'form': form, 'title': 'Edit Activity'})

# 7. Delete Entry
@login_required
def report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk, author=request.user)
    if request.method == 'POST':
        report.delete()
        return redirect('report_list')
    return render(request, 'reports/report_confirm_delete.html', {'report': report})

# 8. Edit Profile (Fixed with Profile Picture support)
@login_required
def edit_profile(request):
    Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form, 
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)

# 9. Change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

# 10. Admin Delete Override
@staff_member_required
def admin_delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    messages.success(request, "Post removed by Admin.")
    return redirect('home')

# 11. Toggle Like on Report
@login_required
def toggle_like(request, pk):
    if request.method == "POST":
        report = get_object_or_404(Report, pk=pk)
        
        if request.user in report.likes.all():
            report.likes.remove(request.user)
            liked = False
        else:
            report.likes.add(request.user)
            liked = True
            
        return JsonResponse({'liked': liked, 'count': report.likes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 12. Add Comment
@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        report = get_object_or_404(Report, pk=pk)
        
        comment = Comment.objects.create(
            report=report,
            author=request.user,
            text=data.get('text')
        )
        
        return JsonResponse({
            'status': 'success',
            'comment_id': comment.id,
            'author': comment.author.username,
            'text': comment.text,
            'date': comment.created_at.strftime("%b %d")
        })
    return JsonResponse({'status': 'error'}, status=400)

# 13. Delete Comment
@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        report_id = comment.report.id
        
        if request.user == comment.author or request.user.is_staff:
            comment.delete()
            remaining_count = Comment.objects.filter(report_id=report_id).count()
            return JsonResponse({'status': 'success', 'count': remaining_count})
            
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    return JsonResponse({'status': 'error'}, status=400)