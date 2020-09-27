from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView,DeleteView,UpdateView,DetailView,ListView,View,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from .models import *
from braces.views import SelectRelatedMixin
from django.utils.text import slugify
# Create your views here.

class GroupList(ListView):
    model = Group
    template_name = 'group/group_list.html'
    context_object_name = 'groups'

class GroupCreate(LoginRequiredMixin,CreateView):
    model = Group
    fields = ('name','description')
    template_name = 'group/group_create.html'
    success_url = reverse_lazy('groups:group_list_url')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user.username
        self.object.save()
        return super().form_valid(form)

class GroupDetail(LoginRequiredMixin,DetailView):
    model = Group
    template_name = 'group/group_detail.html'



class GroupUpdate(LoginRequiredMixin,UpdateView):
    model = Group
    fields = ('name','description')
    template_name = 'group/group_create.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model.objects.get(slug=self.kwargs.get('slug'),pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author__exact=self.request.user.username)

class GroupDelete(LoginRequiredMixin,DeleteView):
    model = Group
    template_name = 'group/group_delete.html'
    success_url = reverse_lazy('groups:group_list_url')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author__exact=self.request.user.username)

class GroupEnter(LoginRequiredMixin,RedirectView,View):
    def get_redirect_url(self,**kwargs):
        return reverse('groups:group_detail_url',kwargs={'slug':self.kwargs.get('slug'),'pk':self.kwargs.get('pk')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'),pk=self.kwargs.get('pk'))
        user = self.request.user

        try:
            new_member = GroupMember.objects.create(user=request.user,group=group)
        except:
            print('Click slower')
        return super().get(request,*args,**kwargs)

class GroupLeave(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:group_detail_url',kwargs={'slug':self.kwargs.get('slug'),'pk':self.kwargs.get('pk')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'),pk=self.kwargs.get('pk'))
        try:
            member = GroupMember.objects.get(user=request.user,group=group)
            member.delete()
        except:
            print('click slower')
        return super().get(request,*args,**kwargs)
