from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login/')
def dashboard(request):
    """
    Dashboard view that shows Mandi market dashboard and simulated offline sync.
    """
    return render(request, 'market/dashboard.html')
