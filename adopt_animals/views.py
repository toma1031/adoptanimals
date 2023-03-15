from django.db.models.query_utils import InvalidQuery
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MessageRoom, Post, Tag, Like, Message, MessageRoom
from .forms import PostForm, MessageForm, ContactForm
from accounts.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.views.generic.edit import FormView

class IndexView(ListView):
  template_name = "index.html"
  model = Post
  context_object_name = 'post_list'
  paginate_by = 9

  def get_queryset(self):
      object_list = Post.objects.all()
      q_category = self.request.GET.get('query_category', None)
      q_sex = self.request.GET.get('query_sex', None)
      q_state = self.request.GET.get('query_state', None)
      q_zipcode = self.request.GET.get('query_zipcode', None)

      if q_category:
          object_list = object_list.filter(category__category=q_category)
      if q_sex:
          object_list = object_list.filter(sex=q_sex)
      if q_state:
          object_list = object_list.filter(user__state__state=q_state)
      if q_zipcode:
          object_list = object_list.filter(user__zipcode__icontains=q_zipcode)
      return object_list

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    post_list = Post.objects.all()
    liked_list = []
    if self.request.user.is_authenticated:
      for post in post_list:
          liked = post.like_set.filter(user=self.request.user)
          if liked.exists():
              liked_list.append(post.id)
    context['liked_list'] = liked_list
    return context

class CreatePostView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = 'adopt_animals/pets/animals_post_form.html'
  success_url = reverse_lazy('adopt_animals:post_done')

  def form_valid(self, form):
      form = form.save(commit=False)
      form.user = self.request.user
      form.save()
      return redirect('adopt_animals:post_done')

  def get_form_kwargs(self, *args, **kwargs):
    form_kwargs = super().get_form_kwargs(*args, **kwargs)
    form_kwargs['initial'] = {'category': 1 }
    return form_kwargs

class PostDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'adopt_animals/pets/post_done.html'

class PostDetailView(DetailView):
    template_name = "adopt_animals/pets/post_detail.html"
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      post_list = Post.objects.all()
      liked_list = []

      if self.request.user.is_authenticated:
        for post in post_list:
            liked = post.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(post.id)
      context['liked_list'] = liked_list
      return context

    def post(self, request, **kwargs):
      message_room = MessageRoom.objects.filter(post_id=self.kwargs['pk'], inquiry_user_id=self.request.user.id)
      if message_room:
        return redirect('adopt_animals:message_room', pk=message_room[0].id)
      else:
        message_room = MessageRoom.objects.create(post_id=self.kwargs['pk'], inquiry_user_id=self.request.user.id)
        return redirect('adopt_animals:message_room', pk=message_room.id)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'adopt_animals/pets/post_update_form.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('adopt_animals:post_detail')
    context_object_name = 'post'


    def get_success_url(self):
        return reverse('adopt_animals:post_detail', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user == post.user:
            return super().get(request, **kwargs)
        else:
            return redirect('adopt_animals:index')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'adopt_animals/pets/post_delete.html'
    model = Post
    success_url = reverse_lazy('adopt_animals:index')

class MyPostListView(LoginRequiredMixin, ListView):
    template_name = 'adopt_animals/pets/my_post_list.html'
    model = Post
    ontext_object_name = 'post_list'
    success_url = reverse_lazy('adopt_animals:index')
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all()
        liked_list = []
        if self.request.user.is_authenticated:
          for post in post_list:
              liked = post.like_set.filter(user=self.request.user)
              if liked.exists():
                  liked_list.append(post.id)
        context['liked_list'] = liked_list
        return context

def LikeView(request):
  if request.method =="POST":
      post = get_object_or_404(Post, pk=request.POST.get('post_id'))
      user = request.user
      liked = False
      like = Like.objects.filter(post=post, user=user)
      if like.exists():
          like.delete()
      else:
          like.create(post=post, user=user)
          liked = True
  
      context={
          'post_id': post.id,
          'liked': liked,
          'count': post.like_set.count(),
      }

  if request.is_ajax():
      return JsonResponse(context)


class MyFavoritePostListView(LoginRequiredMixin, ListView):
    template_name = 'adopt_animals/pets/my_fav_post_list.html'
    model = Post
    ontext_object_name = 'post_list'
    success_url = reverse_lazy('adopt_animals:index')
    paginate_by = 9

    def get_queryset(self):
      return Post.objects.filter(like__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all()
        liked_list = []

        if self.request.user.is_authenticated:
          for post in post_list:
              liked = post.like_set.filter(user=self.request.user)
              if liked.exists():
                  liked_list.append(post.id)
        context['liked_list'] = liked_list
        return context


class MessageRoomView(LoginRequiredMixin, DetailView):
  template_name = 'adopt_animals/pets/message_room.html'
  model = MessageRoom
  form_class = MessageForm
  context_object_name = 'message_room'
  success_url = reverse_lazy('adopt_animals:message_room')

  def get(self, request, **kwargs):
      message_room_obj = get_object_or_404(MessageRoom, pk=self.kwargs['pk'])
      if message_room_obj.post.user == self.request.user or message_room_obj.inquiry_user == self.request.user:
          return super().get(request, **kwargs)
      else:
          return redirect('/')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = MessageForm
    context['message_list'] = Message.objects.filter(message_room_id=self.kwargs['pk'])
    return context

  def post(self, request, **kwargs):
    self.object = self.get_object()
    form = MessageForm(request.POST)
    if form.is_valid():
      message_obj = form.save(commit=False)
      message_obj.message_room_id = self.kwargs['pk']
      message_obj.message_user_id = self.request.user.id
      message_obj.save()
      MessageRoom.objects.filter(pk=self.kwargs['pk']).update(update_time=timezone.now())
      if self.request.user ==  self.object.inquiry_user:
        self.object.post.user.email_user(
          'Hi! ' '{0}'.format(self.object.post.user) + '! Recieved message about your Post on Adopt Animals',
          'New Message Recieved. The massage is "{0}". Please login to your account and check the Message! \n\n https://adoptanimalsusa.herokuapp.com/'.format(request.POST.get('message')))
      else:
        print(self.object.inquiry_user)
        self.object.inquiry_user.email_user(
          'Hi! ' '{0}'.format(self.object.inquiry_user) + '! Recieved message about your Post on Adopt Animals',
          'New Message Recieved. The massage is "{0}". Please login to your account and check the Message! \n\n https://adoptanimalsusa.herokuapp.com/'.format(request.POST.get('message')))
    else:
      print(form.errors)
    return redirect('adopt_animals:message_room', pk=self.object.id)


class MessageRoomListView(LoginRequiredMixin, ListView):
  template_name = 'adopt_animals/pets/my_messages.html'
  model = MessageRoom
  context_object_name = 'message_room_list'
  success_url = reverse_lazy('adopt_animals:my_messages')
  paginate_by = 9

  def get_queryset(self):
    message_room_list = MessageRoom.objects.filter(Q(inquiry_user=self.request.user) | Q(post__user=self.request.user)).order_by('update_time').reverse().distinct()
    search_text = self.request.GET.get('message')
    if search_text:
      message_room_list = message_room_list.filter(Q(message__message__icontains=search_text) | Q(inquiry_user__username__icontains=search_text)
      | Q(post__user__username__icontains=search_text))
      return message_room_list

    return MessageRoom.objects.filter(Q(inquiry_user=self.request.user) | Q(post__user=self.request.user)).order_by('update_time').reverse()


class ContactFormView(FormView):
    template_name = 'adopt_animals/contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('adopt_animals:contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactResultView(TemplateView):
    template_name = 'adopt_animals/contact/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "The form was sent successfully."
        return context


class AboutView(TemplateView):
  template_name = 'adopt_animals/pets/about.html'