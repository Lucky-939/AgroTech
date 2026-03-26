from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import json

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        # Traditional login fallback
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        # User model requires username, we'll map phone to username
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Invalid credentials')
            
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if User.objects.filter(username=phone).exists():
            messages.error(request, 'Account already exists. Please login.')
        else:
            user = User.objects.create_user(username=phone, password=password, first_name=name)
            login(request, user)
            return redirect('/dashboard/')
            
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def biometric_auth(request):
    """
    Simulated Bio-metric authentication endpoint.
    In a real world app, this would use WebAuthn library for Python 
    to verify the FIDO2/WebAuthn payload from the frontend.
    For this demo, we accept a successful frontend signal, 
    and login a demo user automatically.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get('status') == 'success':
                # For demo purposes, we log in or create a "Farmer Bio" user
                user, created = User.objects.get_or_create(username='farmer_bio')
                if created:
                    user.set_password('bio1234')
                    user.first_name = 'Farmer (Biometric ID)'
                    user.save()
                    
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})
