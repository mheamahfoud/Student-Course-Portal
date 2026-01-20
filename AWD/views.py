from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Offering, Subscription, User
from django.middleware.csrf import get_token
import json

# Endpoint to get all offerings
def api_offerings(request):
    offerings = Offering.objects.all().values('id', 'title', 'description')
    return JsonResponse(list(offerings), safe=False)

# Endpoint to handle subscriptions
def ajax_subscribe(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    # Use session-based auth (the project stores user id in session when logging in)
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User not authenticated. Please log in.'}, status=401)

    try:
        try:
            data = json.loads(request.body.decode('utf-8')) if isinstance(request.body, (bytes,)) else json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        offering_id = data.get('offering_id')
        if not offering_id:
            return JsonResponse({'success': False, 'error': 'Missing offering_id'}, status=400)

        offering = get_object_or_404(Offering, id=offering_id)
        user = get_object_or_404(User, id=user_id)

        # Prevent duplicate subscriptions
        if Subscription.objects.filter(user=user, offering=offering).exists():
            return JsonResponse({'success': False, 'error': 'Already subscribed'}, status=200)

        Subscription.objects.create(user=user, offering=offering)

        return JsonResponse({'success': True, 'message': 'Successfully subscribed'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Home Page
def home(request):
    return render(request, 'home.html')

# Register Page
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Create user
        user = User(name=name, email=email)
        user.set_password(password)
        user.save()
        return redirect('/login/')

    return render(request, 'register.html')

# Login Page
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password_hash):
                request.session['user_id'] = user.id
                return redirect(next_url or '/dashboard')
        except User.DoesNotExist:
            pass

    return render(request, 'login.html', {'next': next_url})

# Dashboard
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')

    user = User.objects.get(id=user_id)
    subscriptions = Subscription.objects.filter(user=user)
    return render(request, 'dashboard.html', {'user': user, 'subscriptions': subscriptions})

# Offerings Page
def offerings(request):
    offerings = Offering.objects.all()

    # Ensure CSRF cookie exists for AJAX requests
    get_token(request)

    user_id = request.session.get('user_id')
    subscribed_ids = []
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            subscribed_ids = list(Subscription.objects.filter(user=user).values_list('offering_id', flat=True))
        except User.DoesNotExist:
            user_id = None

    return render(request, 'offerings.html', {'offerings': offerings, 'subscribed_ids': subscribed_ids, 'user_id': user_id})

# Logout
def logout_view(request):
    logout(request)
    return redirect('/')
