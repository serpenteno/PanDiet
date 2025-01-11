from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def custom_404_view(request, exception):
    return render(request, '404.html', {}, status=404)
