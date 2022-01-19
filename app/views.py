from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.http.response import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def registerPage(request):
    form = CreateUserForm()
    if request.method== "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)
            return redirect("login")
    context = {"form": form}
    return render(request, "register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method== "POST":
            username =request.POST.get("username")
            password =request.POST.get("password")
            user =authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'User OR password is incorrect')
                return render(request, "login.html")
    context = {}
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('login')


class TaskList(ListView,LoginRequiredMixin):
    model=Task
    context_object_name = 'tasks'

    def get_context_data(self):
        context = super().get_context_data()
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
class TaskDetail(DetailView):
    model= Task
    context_object_name = 'task'

class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('home')

class DeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('home')

class AdminView(UserPassesTestMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self):
        context = super().get_context_data()
        context['count'] = context['tasks'].filter(complete = False).count()
        return context

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self) -> HttpResponseRedirect:
        raise Http404

    
    