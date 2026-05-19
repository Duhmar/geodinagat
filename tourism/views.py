from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# Import the community engagement models from your accounts app
from accounts.models import Report, Comment
from .models import TouristSpot

@login_required
def analytics_dashboard(request):
    # Aggregating user comments and engagement as per your proposal
    total_reports = Report.objects.count()
    total_comments = Comment.objects.count()
    total_spots = TouristSpot.objects.count()
    
    # Find the most engaged multimedia reports based on likes
    popular_reports = Report.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]

    context = {
        'total_reports': total_reports,
        'total_comments': total_comments,
        'total_spots': total_spots,
        'popular_reports': popular_reports,
    }
    return render(request, 'tourism/analytics.html', context)