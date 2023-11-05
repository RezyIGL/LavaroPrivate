
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

from .models import MyUser, UserProfile, Vacancy, Response, Chat, Message


# Create your views here.
def home(request):
    template_name = "LavaroWeb/home.html"

    return render(request, template_name)


def vacancy_list(request):
    template_name = "LavaroWeb/vacancy/list.html"
    vacancy_list = Vacancy.objects.all()
    paginator = Paginator(vacancy_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        plenty_vacancy = paginator.page(page_number)
    except PageNotAnInteger:
        plenty_vacancy = paginator.page(1)
    except EmptyPage:
        plenty_vacancy = paginator.page(paginator.num_pages)

    return render(request, template_name, {'plenty_vacancy': plenty_vacancy})


def profile_detail(request, user_id):
    template_name = "LavaroWeb/profile/detail.html"
    try:
        profile = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        raise Http404("No Profile found.")

    return render(request, template_name, {'profile': profile})


def chat(request):
    template_name = "LavaroWeb/chat/detail.html"
    return HttpResponse(request, template_name)


def vacancy_detail(request, vacancy_id):
    template_name = "LavaroWeb/vacancy/detail.html"
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        raise Http404("No Vacancy found.")
    
    return render(request, template_name, {'vacancy': vacancy})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
    def post (self, request):
        super(CreateView, self).post(request)
        
        username = request.POST['username']
        user_id = MyUser.objects.get(username=username)
        profile = UserProfile.objects.create(user=user_id)
        profile.save()


        return redirect('LavaroWeb:home')
    
#block Chats and Message
@login_required
def chats_list(request):
    template_name = "LavaroWeb/chats_list.html"
    chats = request.user.chats.order_by("-last_modified")
    return render(request, template_name, {"chats": chats})


@login_required
def chat_detail(request, chat_id):
    template_name = "LavaroWeb/chat_detail.html"
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.message.all().order_by("timestamp")
    if request.method == "POST":
        text = request.POST.get("text")
        message = Message.objects.create(sender=request.user, chat=chat, text=text)
        return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", args=[chat_id]))
    return render(request, template_name, {"chat": chat, "messages": messages})


@login_required
def add_participant(request, chat_id):
    chat = get_object_or_404(Chat, chat_id)
    template_name = "LavaroWeb/add_participant.html"
    if request.method == "POST":
        username = request.POST.get("username")
        user = MyUser.objects.filter(username=username).first()
        if user:
            chat.participants.add(user)
            return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", arg=[chat.id]))
        return render(request, template_name, {"chat": chat})
