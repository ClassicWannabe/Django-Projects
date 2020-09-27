from django.shortcuts import render,redirect
from .models import Post, Image
from .forms import PostForm,PostImageForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model
from braces.views import SelectRelatedMixin
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
User = get_user_model()

class PostList(SelectRelatedMixin,LoginRequiredMixin,generic.ListView):
    model = Post
    template_name = 'post/post_list.html'
    select_related = ('user','group')


class PostDetail(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'post/post_detail.html'

# class PostCreate(LoginRequiredMixin,generic.CreateView):
#     model = Post
#     fields = ['name','text','group']
#     template_name = 'post/post_create.html'
#
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['picture'] = PostImageForm()
#         return context
#
#     def form_valid(self,form):
#         files = self.request.FILES.getlist('images')
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#
#         self.object.save()
#         for file in files:
#             self.object.image_set.picture = Image.objects.create(post=self.object,picture=file)
#         return super().form_valid(form)

@login_required
def post_create(request):
    ImageFormSet = modelformset_factory(Image,form=PostImageForm,extra=3)

    if request.method == 'POST':
        postform = PostForm(request.POST)
        formset = ImageFormSet(request.POST,request.FILES,queryset=Image.objects.none())

        if postform.is_valid() and formset.is_valid():
            new_post = postform.save(commit=False)
            new_post.user = request.user
            new_post.save()

            for form in formset.cleaned_data:
                if form:
                    picture = form['picture']
                    photo = Image(post=new_post,picture=picture)
                    photo.save()
            messages.success(request,"Success with images")
            return redirect('groups:group_detail_url',slug=new_post.group.slug,pk=new_post.group.pk)
        else:
            print(postform.errors,formset.errors)
    else:
        postform = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request,'post/post_create.html',{'postform':postform,'formset':formset})


class UserPosts(SelectRelatedMixin,LoginRequiredMixin,generic.ListView):
    model = Post
    template_name = 'post/user_post_list.html'
    context_object_name = 'posts'
    select_related = ('user','group')

    def get_queryset(self,*args,**kwargs):
        self.queryset = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        return self.queryset.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = self.queryset
        return context

class PostDelete(LoginRequiredMixin,generic.DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('groups:group_list_url')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


# class PostUpdate(LoginRequiredMixin,generic.UpdateView):
#     model = Post
#     template_name = 'post/post_create.html'
#     fields = ('name','text')
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(user_id=self.request.user.id)

@login_required
def post_update(request,pk):
    ImageFormSet = modelformset_factory(Image,form=PostImageForm,extra=3)
    obj = Post.objects.get(pk=pk,user_id=request.user.id)
    if request.method == 'POST':
        postform = PostForm(request.POST,instance=obj)
        formset = ImageFormSet(request.POST,request.FILES,queryset=Image.objects.none())

        if postform.is_valid() and formset.is_valid():
            new_post = postform.save(commit=False)
            new_post.user = request.user
            new_post.save()
            for form in formset.cleaned_data:
                if form:
                    new_post.image.all().delete()
                    picture = form['picture']
                    photo = Image(post=new_post,picture=picture)
                    photo.save()
            messages.success(request,"Success with images")
            return redirect('groups:group_detail_url',slug=new_post.group.slug,pk=new_post.group.pk)
        else:
            print(postform.errors,formset.errors)
    else:
        postform = PostForm(instance=obj)
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request,'post/post_create.html',{'postform':postform,'formset':formset})
