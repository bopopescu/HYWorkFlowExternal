from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class IndexView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    redirect_field_name = '/'
    template_name="home.html"