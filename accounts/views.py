from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .form import LoginForm, RegisterForm, ResetPasswordForm

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = ''

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  # ✅ تسجيل الدخول
            return redirect('AdminDashboard:admin_dashboard')  # أو أي صفحة تانية بعد الدخول
        else:
            msg = 'Invalid email or password.'

    return render(request, 'accounts/login.html', {'form': form, 'msg': msg})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            # إنشاء المستخدم
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name
            )

            # حفظ رقم الهاتف (ممكن نضيفه لاحقًا في نموذج مخصص)
            # أو نستخدم user.profile.phone = phone

            auth_login(request, user)
            return redirect('accounts:login')  # بعد التسجيل الناجح

    return render(request, 'accounts/register.html', {'form': form})

def reset_password_view(request):
    form = ResetPasswordForm(request.POST or None)
    msg = ''

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                msg = 'Password has been reset successfully.'
                return redirect('accounts:login')  # أو أي صفحة تسجيل دخول
            except User.DoesNotExist:
                msg = 'No user found with this email address.'

    return render(request, 'accounts/reset_password.html', {'form': form, 'msg': msg})
