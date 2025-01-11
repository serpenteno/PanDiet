from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView


class CustomLoginView(View):
    def get(self, request, *args, **kwargs):
        # Display login page
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        # Check login
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Remember me support
            remember_me = request.POST.get('rememberMe')
            if remember_me:
                request.session.set_expiry(7 * 24 * 60 * 60)  # 7 days remember
            else:
                # Expiration after browser close
                request.session.set_expiry(0)

            # Login user
            login(request, user)
            messages.success(request, 'Welcome to PanDiet!')
            return redirect('/')  # Redirect to index
        else:
            messages.error(request, 'Invalid login or password!')

        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # Logout user
        logout(request)
        return redirect('/login')


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')

    def get_template_names(self):
        user_role = self.request.user.role
        if user_role in ['admin', 'dietitian']:
            return ['index.html']
        elif user_role == 'client':
            return ['index-client.html']
        else:
            return
