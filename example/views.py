from django.shortcuts import render, redirect
from .forms import RegistrationForm
from supabase import create_client, Client
from decouple import config
from datetime import datetime
from django.http import HttpResponse
import json
from django.contrib.auth.hashers import check_password

# Initialize Supabase client
url = config('SUPABASE_URL')
key = config('SUPABASE_ANON_KEY')
supabase: Client = create_client(url, key)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            data = {
                'name': form.cleaned_data['name'],
                'roll_number': form.cleaned_data['roll_number'],
                'dob': form.cleaned_data['dob'].strftime('%Y-%m-%d'),  # Convert date to string
                'year': form.cleaned_data['year'],
                'semester': form.cleaned_data['semester'],
                'course': form.cleaned_data['course'],
                'reason_to_join': form.cleaned_data['reason_to_join'],
                'expectations': form.cleaned_data['expectations'],
            }
            # Insert data into Supabase
            supabase.table('registrations').insert(data).execute()
            return redirect('success')  # Redirect to a success page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def success(request):
    return render(request, 'success.html')

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
        return render(request, 'registration/login.html')

    return HttpResponse("Method not allowed", status=405)

def home(request):
    # Fetch all registrations from Supabase
    response = supabase.table('registrations').select('*').execute()
    registrations = response.data  # Get the data from the response

    return render(request, 'home.html', {'registrations': registrations})