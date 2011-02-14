from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.validators import email_re
from django.contrib import messages
from django.template import RequestContext
from django import forms

# user login
def new_session(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(email=username, password=password)
  
  if user is not None:
    if user.is_active:
      login(request, user)
      if request.POST.has_key('remember_me') and request.POST['remember_me'] == '1':
        request.session.set_expiry(60 * 60 * 24 * 31)  # 31 day expiry on the session
      else:
        request.session.set_expiry(0) # session cookie has a session expiry (invalidates on a window close)
    else:
      request.session['error'] = 'Sorry, your account has been disabled'
  else:
    request.session['error'] = 'Sorry, your email or password are incorrect'
  
  path = '/'
  if request.POST.has_key('next') and (len(request.POST['next']) is not 0):
    path = request.POST['next']
  return redirect(path)


# signup form
class SignupForm(forms.Form):
  email = forms.EmailField(max_length=100)
  password = forms.CharField(widget=forms.PasswordInput, max_length=128)
  confirm = forms.CharField(widget=forms.PasswordInput, max_length=128)
  
  def clean_email(self):
    email = self.cleaned_data['email']
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError("A user with that email address already exists.")
  
  def clean_confirm(self):
    password = self.cleaned_data.get('password', '')
    confirm = self.cleaned_data['confirm']
    if password != confirm:
        raise forms.ValidationError("The password confirmation does not match the password.")
    return confirm


# show signup form and create users
def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      # create the user
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = User.objects.create_user(email, email, password)
      
      # because of django stupidity, find the user again (so .backend is set)
      user = authenticate(email=email, password=password)
      login(request, user)
      return redirect('/briefing')
  else:
    form = SignupForm()
  
  return render_to_response('users/signup.html', {
    'title': 'Signup',
    'form': form,
  }, context_instance=RequestContext(request))



# user settings form
class SettingsForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput, max_length=128)
  confirm = forms.CharField(widget=forms.PasswordInput, max_length=128)
  
  def clean_confirm(self):
    password = self.cleaned_data.get('password', '')
    confirm = self.cleaned_data['confirm']
    if len(password) != 0 and len(confirm) != 0 and password != confirm:
        raise forms.ValidationError("The password confirmation does not match the password.")
    return confirm


# user settings page
@login_required
def settings(request):
  message = ''
  if request.method == 'POST':
    form = SettingsForm(request.POST)
    if form.is_valid():
      # update the user
      request.user.set_password(form.cleaned_data['password'])
      request.user.save()
      message = 'Your password has been updated'
  else:
    form = SettingsForm()
  
  return render_to_response('users/settings.html', {
    'title': 'Settings',
    'form': form,
    'message': message
  }, context_instance=RequestContext(request))
