from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            # Opcional: login automático após cadastro:
            # login(request, user)
            # return redirect('accounts:dashboard')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Verifique os dados informados.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = 'accounts:login'  # opcional se já configurado em settings

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})
