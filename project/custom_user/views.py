from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
import google.generativeai as genai
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_user.models import Question
from custom_user.models import  History
import re
from django.shortcuts import render
from collections import Counter
from .forms import CreateUserForm
from django.views.decorators.http import require_POST
import google.generativeai as genai
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from custom_user.Ai.predicition import predict_responses  # Import the predict_responses function
os.environ['YOUR_GEMINI_API_KEY'] = 'AIzaSyB6ML2FxTfLOJqs9oB_FmMCYxmQP9IchiU'
genai.configure(api_key=os.environ['YOUR_GEMINI_API_KEY'])
from custom_user.models import User

@login_required(login_url='login')
def ViewSessions(request):
    previous_sessions = History.objects.filter(user=request.user).order_by('-date')

    return render(request, 'custom_user/ViewSessions.html', {'previous_sessions': previous_sessions})


@login_required(login_url='login')
def model(request):
    chatbot_model = request.session.get('chatbot_model', 'Default Model')
    return render(request, 'custom_user/model.html', {'chatbot_model': chatbot_model, 'is_result_visabel': False , 'is_msg':False})

@login_required(login_url='login')
def dashboard(request):
    if request.method == 'POST':
        chatbot_model = request.POST.get('chatbot')
        request.session['chatbot_model'] = chatbot_model
        return redirect('model')
    return render(request, 'custom_user/main-page.html')

def ClickEvaluate(request):
    if request.method == 'POST':
        selected_rights = request.POST.getlist('rights', [])
        selected_right_numbers = [re.findall(r'\d+', right)[0] for right in selected_rights if re.findall(r'\d+', right)]
        request.session['selected_rights'] = selected_right_numbers

        if not selected_rights:
            msg="Please select at least one right."
            return render(request, 'custom_user/model.html',{'msg' : msg, 'is_result_visabel': False,  'is_msg':True})

        questions = Question.objects.filter(right__in=selected_rights)[:1]
        print("The Selected Rights:", selected_rights)
        chatbot_model = request.session.get('chatbot_model', 'Default Model')
        responses = []

        if chatbot_model == 'Gemini':
            print('chat model:', chatbot_model)
            model = genai.GenerativeModel('gemini-pro')
            for question in questions:
                question_parts = question.question.split('/')
                for part in question_parts:
                    part = part.strip()
                    if part:
                        try:
                            response = model.generate_content(part)
                            response_text = response.text
                            # print("Question Part:", part)
                            # print("Response:", response_text)
                            responses.append(response_text)
                        except (AttributeError, ValueError) as e:
                            responses.append("Error: Response might be blocked or empty.")
                        except Exception as e:
                            responses.append("Error: Failed to generate response")
            serialized_responses = json.dumps(responses, cls=DjangoJSONEncoder)
            request.session['responses'] = serialized_responses
            return redirect('display_predictions')
        else:
            return render(request, 'custom_user/model.html', {'is_result_visabel': False  , 'is_msg':False})

def display_predictions(request):
    serialized_responses = request.session.get('responses', '[]')
    responses = json.loads(serialized_responses)

    predictions = predict_responses(responses)

    prediction_counts = Counter(predictions)

    most_common_prediction = prediction_counts.most_common(1)
    if most_common_prediction:
        most_common_prediction = most_common_prediction[0][0]
    else:
        most_common_prediction = None

    chatbot_model = request.session.get('chatbot_model', 'Default Model')
    selected_rights = request.session.get('selected_rights')

    history=History(user=request.user , summary=most_common_prediction , model_name=chatbot_model ,right_selected=selected_rights)
    history.save()

    return render(request, 'custom_user/model.html', {
        'most_common_prediction': most_common_prediction,
        'is_result_visabel': True,
         'is_msg':False
    })


def logout(request):
    auth_logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('main-page')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, 'please go to you email to email}')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('main-page')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = CreateUserForm()

    return render(
        request=request,
        template_name="custom_user/register.html",
        context={"form": form}
        )

def login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('main-page')
            else:
                context['password_error'] = True
                messages.error(request, 'Invalid password.')
        except User.DoesNotExist:
            context['email_error'] = True
            messages.error(request, 'Invalid email.')
    
    return render(request, 'custom_user/login.html', context)
