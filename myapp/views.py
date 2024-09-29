from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from .models import User, Talk
from .forms import UserModelForm, UserLoginForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    user_form = UserModelForm()
    return render(request, "myapp/signup.html", {'user_form':user_form})

class UserCreate(CreateView):
    model = User
    form_class = UserModelForm
    template_name = 'myapp/signup.html'
     # 投稿に成功した時のURL
    success_url = reverse_lazy('index')
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)

class UserLogin(LoginView):
    template_name = 'myapp/login.html'
    next_page = '/friends' 
    form_class = UserLoginForm



def friends_next(request):
    talking_user=[]
    newest_log=[]
    not_talking=[]
    for account in User.objects.all():
       if Talk.objects.filter(Q(sender=request.user, recipient=account)|Q(sender=account, recipient=request.user)).exists():
           talking_user.append(account)
           newest = Talk.objects.filter(Q(sender=request.user, recipient=account)|Q(sender=account, recipient=request.user)).order_by('-send_time').first()
           newest_log.append(newest)

       else:
           not_talking.append(account)
           
    context = {'you':request.user,
               'talking_user':talking_user,
               'newest_log':newest_log,
               'not_talking':not_talking}
    return render(request, "myapp/friends.html", context)

def talk_room(request, your_id, the_other_id):
    _sender = request.user
    _recipient = User.objects.get(id=the_other_id)
    #メッセージを送信した時
    if request.method == 'POST':
        _message = request.POST.get("message")
        _send_time = datetime.now()
        talk_log = Talk(sender=_sender, recipient=_recipient, message=_message, send_time=_send_time)
        talk_log.save()

    talk_content = Talk.objects.filter(Q(sender=_sender, recipient=_recipient)|Q(sender=_recipient, recipient=_sender)).order_by('send_time')

    context = {'the_other':User.objects.get(id=the_other_id),
               'you':request.user,
               'talk_content':talk_content}
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

class NameChange(UpdateView):
    model = User
    fields = ["username"]
    template_name = "myapp/name_change.html"
    success_url = reverse_lazy('setting')
    
class EmailChange(UpdateView):
    model = User
    fields = ["email"]
    template_name = "myapp/email_change.html"
    success_url = reverse_lazy('setting')

class IconChange(UpdateView):
    model = User
    fields = ["img"]
    template_name = "myapp/icon_change.html"
    success_url = reverse_lazy('setting')

class PassChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('pass_change_success')
    template_name = 'myapp/pass_change.html'

def pass_change_success(request):
    return render(request, "myapp/pass_change_success.html")

def logout(request):
    return render(request, "myapp/logout.html")

class UserLogout(LogoutView):
    template_name = "myapp/logout2.html"