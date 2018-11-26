from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView

from users.forms import UserSignUpForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login

from users.models import User, SubTitle, Lead, Trial
from users.utils import read_from_csv, read_leads_from_csv, read_trials_from_csv


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    return render(request, 'index.html', {})


@login_required(login_url='/login/')
def home(request):
    users = User.objects.all()
    search = request.GET.get('search')
    if search:
        users = users.filter(sub__title=search)
    return render(request, 'home.html', {'users': users, 'subs': SubTitle.objects.all(), 'leads': Lead.objects.all(),
                                         'trials': Trial.objects.all(), 'search': search})


class SignUpView(FormView):
    form_class = UserSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('index')
    extra_context = {'tab': 'signup'}

    def form_valid(self, form):
        new_user = form.save()
        login(self.request, new_user)
        return super(SignUpView, self).form_valid(form)


class FileUploadView(TemplateView):
    template_name = "file_upload.html"

    def post(self, request, **kwargs):
        if request.POST and request.FILES:
            csvfile = request.FILES['csv_file']
            leads_csvfile = request.FILES['leads_csv_file']
            trial_csvfile = request.FILES['trial_csvfile']
            read_from_csv(csvfile.read())
            read_leads_from_csv(leads_csvfile.read())
            read_trials_from_csv(trial_csvfile.read())
            # return redirect(reverse("dashboard:get_user_profile", args=[self.get_selected_org().id]))
        return render(request, self.template_name, {})
