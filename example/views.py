from django.shortcuts import render, redirect
from .forms import RegistrationForm
from supabase import create_client, Client
from decouple import config
from datetime import datetime
from django.http import HttpResponse
import json
from django.contrib.auth.hashers import check_password
import razorpay
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Initialize Supabase client
url = config('SUPABASE_URL')
key = config('SUPABASE_ANON_KEY')
supabase: Client = create_client(url, key)

RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')
RAZORPAY_WEBHOOK_SECRET = config('RAZORPAY_WEBHOOK_SECRET')

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            data = {
                'name': form.cleaned_data['name'],
                'roll_number': form.cleaned_data['roll_number'],
                'dob': form.cleaned_data['dob'].strftime('%Y-%m-%d'),  # Convert date to string
                'mobile_number': form.cleaned_data['mobile_number'],  # New field for mobile number
                'email': form.cleaned_data['email'],  # New field for email address
                'year': form.cleaned_data['year'],
                'semester': form.cleaned_data['semester'],
                'course': form.cleaned_data['course'],
                'reason_to_join': form.cleaned_data['reason_to_join'],
                'expectations': form.cleaned_data['expectations'],
            }
            # Insert data into Supabase
            response = supabase.table('registrations').insert(data).execute()
            registration_id = response.data[0]['id']  # Assuming the response contains the inserted ID

            # Create a Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': 100,  # Amount in paise (100 INR)
                'currency': 'INR',
                'receipt': f'receipt# {registration_id}',
                'notes': {
                    'registration_id': registration_id  # Include registration ID in notes
                }
            })

            # Redirect to the payment page with the order ID and Razorpay key ID
            return render(request, 'payment.html', {
                'razorpay_order_id': razorpay_order['id'],
                'registration_id': registration_id,
                'razorpay_key_id': RAZORPAY_KEY_ID,  # Pass the Razorpay key ID to the template
            })
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')

    # Fetch the user details using payment_id and order_id
    response = supabase.table('registrations').select('*') \
        .eq('payment_id', payment_id).eq('order_id', order_id).execute()

    registration = response.data[0] if response.data else None

    return render(request, 'success.html', {
        'message': 'Payment processed successfully!' if registration else 'No registration details found!',
        'registration': registration
    })

def login_user(request):
    if request.method == 'POST':
        try:
            # Handle JSON or form-encoded data
            if request.content_type == "application/json":
                data = json.loads(request.body)
                username = data.get('username')  # Username still required for authentication
                password = data.get('password')
            else:
                username = request.POST.get('username')
                password = request.POST.get('password')

            # Validate input
            if not username or not password:
                return HttpResponse("Username and password are required", status=400)

            # Authenticate user
            response = supabase.table('users').select('password').eq('username', username).execute()
            if response.data:
                stored_password = response.data[0]['password']

                if check_password(password, stored_password):
                    # Redirect to home page without including the name
                    return redirect('/home/')  # Change this to your desired home page URL

            # If credentials are invalid
            return HttpResponse("Invalid credentials", status=401)

        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    elif request.method == 'GET':
        return render(request, 'login.html')

    return HttpResponse("Method not allowed", status=405)

def home(request):
    # Fetch all registrations from Supabase
    response = supabase.table('registrations').select('*').execute()
    registrations = response.data  # Get the data from the response

    return render(request, 'home.html', {'registrations': registrations})

from django.urls import reverse
from urllib.parse import urlencode

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    registration_id = request.GET.get('registration_id')

    try:
        payment = razorpay_client.payment.fetch(payment_id)
        
        if payment['status'] == 'captured':
            supabase.table('registrations').update({
                'status': 'successful',
                'payment_id': payment_id,
                'order_id': order_id
            }).eq('id', registration_id).execute()
        else:
            supabase.table('registrations').update({
                'status': 'not successful',
                'payment_id': payment_id,
                'order_id': order_id
            }).eq('id', registration_id).execute()

        # Use reverse to get the base URL and urlencode to append query parameters
        base_url = reverse('success')  # Ensure 'success' is the name of your view in urls.py
        query_params = urlencode({'payment_id': payment_id, 'order_id': order_id})
        success_url = f"{base_url}?{query_params}"

        return redirect(success_url)
    except Exception as e:
        return HttpResponse(f"An error occurred while verifying payment: {str(e)}", status=500)
        
@csrf_exempt  # Disable CSRF for this view
def razorpay_webhook(request):
    if request.method == 'POST':
        # Get the webhook secret from your environment variables
        webhook_secret = config('RAZORPAY_WEBHOOK_SECRET')
        payload = request.body
        signature = request.headers.get('X-Razorpay-Signature')

        # Verify the webhook signature
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        # Parse the webhook payload
        event_data = json.loads(payload)

        # Handle different events
        if event_data['event'] == 'payment.captured':
            payment_id = event_data['payload']['payment']['entity']['id']
            registration_id = event_data['payload']['payment']['entity']['notes']['registration_id']

            # Update registration status to successful
            supabase.table('registrations').update({'status': 'successful'}).eq('id', registration_id).execute()

        elif event_data['event'] == 'payment.failed':
            registration_id = event_data['payload']['payment']['entity']['notes']['registration_id']

            # Update registration status to not successful
            supabase.table('registrations').update({'status': 'not successful'}).eq('id', registration_id).execute()

        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def payment_cancelled(request):
    return render(request, 'cancelled.html')