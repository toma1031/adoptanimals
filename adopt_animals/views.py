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

# Create your views here.
class IndexView(ListView):
  template_name = "index.html"
  model = Post
  context_object_name = 'post_list'
  paginate_by = 9

# get_queryset関数で検索機能を実装
  def get_queryset(self):
    # 全Postオブジェクトを取得し、object_list変数に代入
      object_list = Post.objects.all()
    # query_category が空っぽ(= html側のvalueがvalue=""の時)にはq_categoryをNoneにするが、html側のvalueに何か入っている時は
    # q_categoryにそれを代入する。以下同様
      q_category = self.request.GET.get('query_category', None)
      q_sex = self.request.GET.get('query_sex', None)
      q_state = self.request.GET.get('query_state', None)
      q_zipcode = self.request.GET.get('query_zipcode', None)

    # もしcategoryになにかある場合（html側のvalueに何か入っている時）、
      if q_category:
        # PostモデルのcategoryフィールドはTagモデルに紐づいており、Tagモデルのcategoryフィールドを取得しobject_list変数に代入
          object_list = object_list.filter(category__category=q_category)
    # もしsexになにかある場合（html側のvalueに何か入っている時）、
      if q_sex:
        # Postモデルのsexフィールドを取得しobject_list変数に代入
          object_list = object_list.filter(sex=q_sex)
    # もしstateになにかある場合（html側のvalueに何か入っている時）、
      if q_state:
        # １番目のuserはUserモデルのuserフィールド、２番目のstateはUserモデルstateフィールド、３番目はUserモデルにはStateモデルがForeginKey紐づいているのでStateモデルのstateフィールドを表す。それを取得しobject_list変数に代入
          object_list = object_list.filter(user__state__state=q_state)
    # もしzipcodeになにかある場合（html側のvalueに何か入っている時）、
      if q_zipcode:
        # １番目のuserはUserモデルのuserフィールド、２番目のzipcodeはUserモデルzipcodeフィールド、３番目はicontainsは入力された文字列。それを取得しobject_list変数に代入
          object_list = object_list.filter(user__zipcode__icontains=q_zipcode)
    # 最後に取得されたオブジェクトのリスト（Post）を返す
      return object_list

# いいね機能の部分
# contextは辞書型のデータ。そしてcontextという変数にデータが入る。
# context = super().get_context_data(**kwargs) は先日もsuper().get() でお話しした通り、親クラスから継承するよという意味になります。
# IndexViewはListViewを継承しているのでpaginatorのデータが格納されています。(IndexViewでpaginate_by使ってますよね)
# さらにはpage_objにはpaginate_byで指定した分だけのPostオブジェクトが格納されています。
# ここまではListViewが勝手に処理をしてくれますが、これ以外にもtemplate側にデータを渡すときにはget_context_dataを使います。
# ここでcontextに入れているのはpaginate_byで指定した分だけのPostオブジェクトが格納されています。
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # post_listへPostオブジェクトを代入
    post_list = Post.objects.all()
    # Liked_listというスタックを用意する
    liked_list = []
    # ユーザーがログインしていなければ、このfor文を回さない
    if self.request.user.is_authenticated:
      for post in post_list:
        # like_setでpostに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている
          # 今回の場合LikeモデルにPostモデルと、Userモデルを外部キーで連携させています。
          # LikeモデルのLikeオブジェクトからPostモデルの情報を引っ張ってくるときを参照といいます(Like.objects.filter(post=Post_object) )
          # が逆にPostモデルもしくはUserモデルからLikeモデルの情報を引っ張ってくるときのことを逆参照といいます。
          # 逆参照の時はオブジェクト.モデル名_set とすることでPostオブジェクトに紐づくLikeオブジェクトを取得することが可能になります。
          liked = post.like_set.filter(user=self.request.user)
          # いいねされていたらliked_list スタックの中にそのいいねされたPostを入れていく
          if liked.exists():
              liked_list.append(post.id)
    # contextのliked_listリストにliked_listを代入
    context['liked_list'] = liked_list
    # contextを返す
    return context

class CreatePostView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = 'adopt_animals/pets/animals_post_form.html'
  success_url = reverse_lazy('adopt_animals:post_done')

# 下記のコードでPost時にユーザーを取得
# 何かformでは入力しないけど保存時に何かデータを突っ込みたいときにはdef form_valid()で入力してあげればOK
  def form_valid(self, form):
      form = form.save(commit=False)
      # フォームを送信するユーザーとログインしているユーザーを紐づけしている
      form.user = self.request.user
      form.save()
      return redirect('adopt_animals:post_done')

# 下記のコードでcategoryの初期値をDog（１）に設定を取得
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
      # post_listへPostオブジェクトを代入
      post_list = Post.objects.all()
      # Liked_listというスタックを用意する
      liked_list = []
      # ユーザーがログインしていなければ、このfor文を回さない
      if self.request.user.is_authenticated:
        for post in post_list:
          # like_setでpostに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている
            # 今回の場合LikeモデルにPostモデルと、Userモデルを外部キーで連携させています。
            # LikeモデルのLikeオブジェクトからPostモデルの情報を引っ張ってくるときを参照といいます(Like.objects.filter(post=Post_object) )
            # が逆にPostモデルもしくはUserモデルからLikeモデルの情報を引っ張ってくるときのことを逆参照といいます。
            # 逆参照の時はオブジェクト.モデル名_set とすることでPostオブジェクトに紐づくLikeオブジェクトを取得することが可能になります。
            liked = post.like_set.filter(user=self.request.user)
            # いいねされていたらliked_list スタックの中にそのいいねされたPostを入れていく
            if liked.exists():
                liked_list.append(post.id)
      # contextのliked_listリストにliked_listを代入
      context['liked_list'] = liked_list
      # contextを返す
      return context

    # メッセージボタンクリックした後にdef post() に飛ぶ
    def post(self, request, **kwargs):
      # filter()で該当Postオブジェクトかつinquiry_user が登録されているMessageRoomオブジェクトがあるのかないのかをチェックする
      message_room = MessageRoom.objects.filter(post_id=self.kwargs['pk'], inquiry_user_id=self.request.user.id)
      # ログインしているユーザーと該当のPostオブジェクトが登録されているMessageRoomオブジェクトを検索
      if message_room:
        # MessageRoomオブジェクトがあれば該当のMessageRoomオブジェクトの/message_room/<int:pk> へ飛ばす
        # この場合はクエリセットで取得されます。（MessageRoom.objects.filterで取得しているため）
        # クエリセットはオブジェクトが1つ以上格納されたリストに近い形ですのでmessage_room[0] で1つ目のオブジェクトが、message_room[1] で2つ目のオブジェクトが取得できます
        return redirect('adopt_animals:message_room', pk=message_room[0].id)

      else:
        # なければ新しくMessageRoomオブジェクトを作成し/message_room/<int:pk> にリダイレクトさせる、
        # こちらはMessageRoomオブジェクトを作成した後に作成したオブジェクトを返します。
        # なのでmessage_room変数に新規のオブジェクトを格納しているということですね。
        # オブジェクトなのでmessage_room.id とすることができます。
        message_room = MessageRoom.objects.create(post_id=self.kwargs['pk'], inquiry_user_id=self.request.user.id)
        return redirect('adopt_animals:message_room', pk=message_room.id)






class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'adopt_animals/pets/post_update_form.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('adopt_animals:post_detail')
    context_object_name = 'post'

    # 引数が必要になる(今回の場合<pk: id)URLにリダイレクトさせる時は別途get_success_urlを継承してあげる必要があります。
    def get_success_url(self):
        return reverse('adopt_animals:post_detail', kwargs={'pk': self.object.id})

    # def get()関数 というのを継承してページにアクセスできるユーザーに制限をかける
    # requestにはurlなどの情報が入っています。
    # アクセス先のurlやメタ情報など様々な情報が含まれています。
    def get(self, request, *args, **kwargs):
      # Postオブジェクトを取得する
      # 該当のPostオブジェクトが存在しない場合HTTPのステータスが404になるのでページが存在しないことになります。
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # 投稿したユーザーとログイン中のユーザーが一致すれば
        if self.request.user == post.user:
          # アクセスさせる
          # super()はUpdateView。
          # 親クラスは継承元のことを言うのでPostUpdateViewのことでは無い。
          # requestにはurlなどの情報が入っている。
          # アクセス先のurlやメタ情報など様々な情報が含まれている。
          # kwargsにはアクセス時に送信されたキーワード引数が含まれる。
          # こちらの解説が詳しいので参考にしてみてください
          # https://teratail.com/questions/299155
            return super().get(request, **kwargs)
        else:
          # それ以外はindexへ
            return redirect('adopt_animals:index')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'adopt_animals/pets/post_delete.html'
    model = Post
    success_url = reverse_lazy('adopt_animals:index')

    # ２、class MyPostListView(LoginRequiredMixin, ListView)　と　class PostDetailView(DetailView)
    # にはdef get_context_dataを記載していませんが、
    # なぜ動くのでしょうか？
    # MyPostListViewとPostDetailViewは両方model = 'Post' としていますね。
    # これはListViewを継承している場合、Post.objects.all() が、DetailViewを継承している場合はPost.objects.get(id=pk) が自動的に実行されるようになっています。
    # get_context_dataでは上記のmodel='Post' 以外で何かtemplate側にデータを持っていきたい場合に使用します。
    # こんかいの場合、liked_listというログイン中のユーザーがいいねしたPostオブジェクトのIDを格納したリストをtemplate側に渡していましたね。


class MyPostListView(LoginRequiredMixin, ListView):
    template_name = 'adopt_animals/pets/my_post_list.html'
    model = Post
    ontext_object_name = 'post_list'
    success_url = reverse_lazy('adopt_animals:index')
    paginate_by = 9

# get_queryset(self) を使用して、ページにアクセスできるユーザーは投稿者のみにする
    def get_queryset(self):
      # Postの中でログインユーザーが投稿したもののみ表示する
        return Post.objects.filter(user_id=self.request.user.id)

    # ２、class MyPostListView(LoginRequiredMixin, ListView)とclass PostDetailView(DetailView)
    # にはdef get_context_dataを記載していませんが、
    # なぜ動くのでしょうか？
    # MyPostListViewとPostDetailViewは両方model = 'Post' としていますね。
    # これはListViewを継承している場合、Post.objects.all() が、DetailViewを継承している場合はPost.objects.get(id=pk) が自動的に実行されるようになっています。
    # get_context_dataでは上記のmodel='Post' 以外で何かtemplate側にデータを持っていきたい場合に使用します。
    # こんかいの場合、liked_listというログイン中のユーザーがいいねしたPostオブジェクトのIDを格納したリストをtemplate側に渡していましたね。

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post_listへPostオブジェクトを代入
        post_list = Post.objects.all()
        # Liked_listというスタックを用意する
        liked_list = []
        # ユーザーがログインしていなければ、このfor文を回さない
        if self.request.user.is_authenticated:
          for post in post_list:
            # like_setでpostに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている
              # 今回の場合LikeモデルにPostモデルと、Userモデルを外部キーで連携させています。
              # LikeモデルのLikeオブジェクトからPostモデルの情報を引っ張ってくるときを参照といいます(Like.objects.filter(post=Post_object) )
              # が逆にPostモデルもしくはUserモデルからLikeモデルの情報を引っ張ってくるときのことを逆参照といいます。
              # 逆参照の時はオブジェクト.モデル名_set とすることでPostオブジェクトに紐づくLikeオブジェクトを取得することが可能になります。
              liked = post.like_set.filter(user=self.request.user)
              # いいねされていたらliked_list スタックの中にそのいいねされたPostを入れていく
              if liked.exists():
                  liked_list.append(post.id)
        # contextのliked_listリストにliked_listを代入
        context['liked_list'] = liked_list
        # contextを返す
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

# get_queryset(self) を使用して、ページにアクセスできるユーザーは投稿者のみにする
    def get_queryset(self):
      # Postの中でログインユーザーがいいねした投稿したもののみ表示する
      # （like__user=self.request.user）の意味は（Likeモデル__Userモデル＝ログインしているユーザー）で
      # ログイン中ユーザーがLikeしているPostオブジェクトを全て取得するという意味になります。
      return Post.objects.filter(like__user=self.request.user)

    # ２、class MyPostListView(LoginRequiredMixin, ListView)　と　class PostDetailView(DetailView)
    # にはdef get_context_dataを記載していませんが、
    # なぜ動くのでしょうか？
    # MyPostListViewとPostDetailViewは両方model = 'Post' としていますね。
    # これはListViewを継承している場合、Post.objects.all() が、DetailViewを継承している場合はPost.objects.get(id=pk) が自動的に実行されるようになっています。
    # get_context_dataでは上記のmodel='Post' 以外で何かtemplate側にデータを持っていきたい場合に使用します。
    # こんかいの場合、liked_listというログイン中のユーザーがいいねしたPostオブジェクトのIDを格納したリストをtemplate側に渡していましたね。

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post_listへPostオブジェクトを代入
        post_list = Post.objects.all()
        # Liked_listというスタックを用意する
        liked_list = []
        # ユーザーがログインしていなければ、このfor文を回さない
        if self.request.user.is_authenticated:
          for post in post_list:
            # like_setでpostに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている
              # 今回の場合LikeモデルにPostモデルと、Userモデルを外部キーで連携させています。
              # LikeモデルのLikeオブジェクトからPostモデルの情報を引っ張ってくるときを参照といいます(Like.objects.filter(post=Post_object) )
              # が逆にPostモデルもしくはUserモデルからLikeモデルの情報を引っ張ってくるときのことを逆参照といいます。
              # 逆参照の時はオブジェクト.モデル名_set とすることでPostオブジェクトに紐づくLikeオブジェクトを取得することが可能になります。
              liked = post.like_set.filter(user=self.request.user)
              # いいねされていたらliked_list スタックの中にそのいいねされたPostを入れていく
              if liked.exists():
                  liked_list.append(post.id)
        # contextのliked_listリストにliked_listを代入
        context['liked_list'] = liked_list
        # contextを返す
        return context


class MessageRoomView(LoginRequiredMixin, DetailView):
  template_name = 'adopt_animals/pets/message_room.html'
  model = MessageRoom
  form_class = MessageForm
  context_object_name = 'message_room'
  success_url = reverse_lazy('adopt_animals:message_room')

# Get関数でメッセージルームにアクセスできるユーザーを制限
  def get(self, request, **kwargs):
    # message_room_obj変数にMessageroomオブジェクトのIDを入れ込む
      message_room_obj = get_object_or_404(MessageRoom, pk=self.kwargs['pk'])
      # 投稿したユーザー(message_room_obj.post.userとログイン中のユーザー(self.request.user)が一致する、もしくは
      # メッセージルームを作ったユーザー（message_room_obj.inquiry_user）とログイン中のユーザー（self.request.user）が一致すれば、メッセージルームへ移動させる
      if message_room_obj.post.user == self.request.user or message_room_obj.inquiry_user == self.request.user:
        # super(). = MessageRoomViewクラスに設定しているListViewのこと
        # **kwargs　＝　ここではその前のコードでmessage_room_obj=get_object_or_404(MessageRoom, pk=self.kwargs['pk'])としているから、message_roomのIDのことをさす。つまりreturn super().get(request, **kwargs)を詳しくいうと
        # ListViewで設定したmessage_roomのIDを探して（GET）、それを返す
          return super().get(request, **kwargs)
      else:
        # メッセージルームのメンバーでない場合はIndexへ飛ばす
          return redirect('/')

  # 送信済みのメッセージを表示するために必要
  def get_context_data(self, **kwargs):
    # contextという変数にDetailView（ここではsuperがDetailViewを表している）のContextデータ（context_object_name = 'message_room'）をGetして辞書型として代入
    # この時点で変数contextにはmessage_roomが辞書型で入っている。
    context = super().get_context_data(**kwargs)
    # CreateViewとUpdateView以外ではtemplate側で{{ form }} が使えないので、HTMLで表示するためForms.pyを使用している場合は下記のように書いてやる必要がある。
    context['form'] = MessageForm
    # message_listをContextとして定義。contextは辞書型のデータなので、データを追加することもできる。例えば、context['message_list'] = 'message_room'とすれば、keyがmessage_list、valueがMessage.objects.all()というデータを追加することができる。
    # つまり、下記のように書くことによりcontextをどういうものにするか定義していることになる
    # Message.objects.filter(message_room_id=self.kwargs['pk'])はMessageモデルのmessage_roomフィールドが今アクセスしてるMessageRoomのidと一致するものだけ持ってくるという意味。self.kwargs[‘pk’]はそのオブジェクトのIDという意味がある
    context['message_list'] = Message.objects.filter(message_room_id=self.kwargs['pk'])
    # 最後にContext（Message.objects.all()）を返す
    return context


# このPost関数はDetailViewであるMessageRoomView（MessageRoomページ）において、投稿機能を持たせるときに必要な関数
  def post(self, request, **kwargs):
    # def post内はself.object使えないので
    # 以下のようにすればうまくいくと思います。
    self.object = self.get_object()
    # form変数にMessageFormを代入（このMessageRoomViewでMessageFormを使うには必須の作業）
    form = MessageForm(request.POST)
    # メッセージを保存するために必要
    if form.is_valid():
      # 仮のオブジェクトを作る(データベースにはまだ保存されない)
      message_obj = form.save(commit=False)
      # ここでmessage_roomに値（Pkやユーザー情報を入れてやる）。message_obj.message_room_id とはMessageオブジェクトに紐づいているMessage_roomのIDという意味
      message_obj.message_room_id = self.kwargs['pk']
      # Messageオブジェクトを作成時にmessage_user（送信者）のIDそのものを設定してやる必要がある。self.request.user.idの意味は「そのユーザーのIDそのもの」 
      message_obj.message_user_id = self.request.user.id
      # オブジェクトを保存する(データベースに保存される)
      message_obj.save()
      # MessageRoomのupdate_timeフィールドを更新する処理を追加
      MessageRoom.objects.filter(pk=self.kwargs['pk']).update(update_time=timezone.now())
      # もしログインしているユーザーがmessage_room.inquiry_user(ペットの投稿者じゃない)だった場合
      if self.request.user ==  self.object.inquiry_user:
        print(self.object.post.user)
        # ペットの投稿者（message_room.post.user）にメールを送る
        # 自分の中ではform.送りたい宛先.email_userで
        # メールが送れるのかなと解釈しておりました。
        # なるほど、この場合は
        # form = form.save(commit=False)
        # こうしているのでRequestPTOオブジェクトを作成しているのでform.chose_supervisor.email.. というのが使えています。
        # 自分の中ではform.送りたい宛先.email_userでメールが送れるのかなと解釈しておりました。
        # この考え方はやめましょう。大事なのはformという変数に何がはいっているのか というところですね。
        # 今回の場合同じformという変数が定義されていても中身は異なります。
        # 何が入っているのか、というのを意識づけてもらえればなと思います。
        # では今回の場合は、同様な処理を行っているのはmessage_obj = form.save(commit=False)ですね。
        self.object.post.user.email_user(
          # 題名
          # 題名に外部情報を読み込む方法は下記を参照。
          # https://qiita.com/nomurasan/items/d68ed63a7dae897eda7c
          'Hi! ' '{0}'.format(self.object.post.user) + '! Recieved message about your Post on Adopt Animals',
          # メッセージの中身
          # メッセージに外部情報を読み込む方法は下記を参照。
          # https://qiita.com/nomurasan/items/d68ed63a7dae897eda7c
          # request.POSTにはHTML側のフォームからPOSTされた内容が保管されている
          'New Message Recieved. The massage is "{0}". Please login to your account and check the Message! \n\n http://127.0.0.1:8000/message_room_list/'.format(request.POST.get('message')))
      # もしログインしているユーザーがmessage_room.post(ペットの投稿者)だった場合
      else:
        print(self.object.inquiry_user)
        # 質問者（message_room.inquiry_user）にメールを送る
        self.object.inquiry_user.email_user(
          # 題名
          'Hi! ' '{0}'.format(self.object.inquiry_user) + '! Recieved message about your Post on Adopt Animals',
          # メッセージの中身
          'New Message Recieved. The massage is "{0}". Please login to your account and check the Message! \n\n http://127.0.0.1:8000/message_room_list/'.format(request.POST.get('message')))
    else:
      # メッセージに何か不備がある場合はエラー表示
      print(form.errors)
    # メッセージを送った後はそのメッセージルームにリダイレクト
    # ただ豆知識でお伝えしておくと以下のように書いておけばmessage_room = MessageRoom.objects.filter(id=self.kwargs['pk'], inquiry_user_id=self.request.user.id) これは不要になります。
    return redirect('adopt_animals:message_room', pk=self.object.id)


class MessageRoomListView(LoginRequiredMixin, ListView):
  template_name = 'adopt_animals/pets/my_messages.html'
  model = MessageRoom
  # HTMLのmessage_room_listを意味している
  context_object_name = 'message_room_list'
  success_url = reverse_lazy('adopt_animals:my_messages')
  paginate_by = 9

  # def get_context_data(self, **kwargs):
  #   # contextという変数にDetailView（ここではsuperがDetailViewを表している）のContextデータ（context_object_name = 'message_room'）をGetして辞書型として代入
  #   # この時点で変数contextにはmessage_roomが辞書型で入っている。
  #   context = super().get_context_data(**kwargs)
  #   # message_room_listをContextとして定義。contextは辞書型のデータなので、データを追加することもできる。例えば、context['message_room_list'] = 'message_room'とすれば、keyがmessage_list、valueがMessage.objects.all()というデータを追加することができる。
  #   # つまり、下記のように書くことによりcontextをどういうものにするか定義していることになる
  #   context['message_room_list'] = MessageRoom.objects.filter(inquiry_user=self.request.user)
  #   # 最後にContext（MessageRoom.objects.all()）を返す
  #   return context

# paginated_by = 8　を使っている時点で、オブジェクトをフィルターをかけてページに表示するには
# get_context_data関数は使えず、get_queryset関数しか使えない

# 検索機能
  def get_queryset(self):
    # ログインしているユーザー(self.request.user)が質問者(inquiry_user)もしくはペット投稿者(post__user)というフィルタリングをかけて、
    # MessageRoomを取得
    # .distinct()は重複取得をふせぐ時に使用するので基本は絶対書くべき。その際はorder_byをつける。そうしないと、レコードに値がバラバラに入っていると正しく重複を削除してくれないので注意。.reverse()は逆にするという意味だが、今回の場合はupdate_timeが最新のものが通常は一番最後に表示されるところを一番最初に持ってきてくれる。
    message_room_list = MessageRoom.objects.filter(Q(inquiry_user=self.request.user) | Q(post__user=self.request.user)).order_by('update_time').reverse().distinct()
    # HTMLのname="message"がViewのdef get_querysetの中の構文、search_text = self.request.GET.get('message')の
    # messageを意味する
    search_text = self.request.GET.get('message')
    if search_text:
  # １番目のmassageはmassageモデル、１番目のmassageモデルのmassageフィールド、3番目はicontainsは入力された文字列。それを取得しobject_list変数に代入。つづけてユーザーネーム（inquiry_user（質問者）とpost__user（投稿者）のユーザーネーム）でも検索できるようにQ(inquiry_user__username__icontains=search_text)| Q(post__user__username__icontains=search_text)を追記
      message_room_list = message_room_list.filter(Q(message__message__icontains=search_text) | Q(inquiry_user__username__icontains=search_text)
      | Q(post__user__username__icontains=search_text))
  # 最後に取得されたオブジェクトのリスト（message_roomのリスト）を返す
      return message_room_list



    # フィールドを繋げて取得する時は、__で繋いでやる。post__user=はPostモデルの先にあるuserというフィールドを条件にかけてほしいという意味。ちなみに下記のコードはログインしているユーザー(self.request.user)が質問者(inquiry_user)もしくはペット投稿者(post__user)に該当するMessageRoomオブジェクトを取得し、リターンするという意味になる
    return MessageRoom.objects.filter(Q(inquiry_user=self.request.user) | Q(post__user=self.request.user)).order_by('update_time').reverse()






# お問い合わせフォーム
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