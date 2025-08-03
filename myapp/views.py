from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import User
from .forms import RegisterForm, LoginForm

from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # don’t save yet
            user.password = make_password(form.cleaned_data['password'])  # hash it
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    return redirect('posts')
                else:
                    form.add_error(None, 'Incorrect password')
            except User.DoesNotExist:
                form.add_error(None, 'User not found')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


            
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate




#----------------#
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key="")
import random

def generate_ai_post():
        ai_user = User.objects.get(email="ai@posthub.com")
        prompt=ChatPromptTemplate.from_template("Write a short social media post about tech, nature or motivation. choose one topic any and write post direct no fluff explantion or anything")
        chain=prompt|llm;
        result=chain.invoke({})
        title = random.choice(["Thought of the Day", "AI Drop", "Tech Flash", "AutoPost"])
        Post.objects.create(user=ai_user,content=result.content,title=title)
        print("AI post added successfully.")
           
def run_ai_post(request):
    generate_ai_post()
    return redirect('posts')
#-----------------

from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post, User

def post_page(request):
    posts = Post.objects.all().order_by('-created_at')  # newest first

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # get user from session
            user_id = request.session.get('user_id')
            if user_id:
                post.user = User.objects.get(id=user_id)
                post.save()
                return redirect('posts')  # reload the page
    else:
        form = PostForm()

    return render(request, 'post_page.html', {'form': form, 'posts': posts})

from django.shortcuts import get_object_or_404

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user.id != request.session.get('user_id'):
        return HttpResponse("Unauthorized", status=401)

    post.delete()
    return redirect('posts')

def edit_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    
    if post.user.id!=request.session.get('user_id'):
        return HttpResponse("OOPS bumer");
    
    if request.method=='POST':
        form=PostForm(request.POST,instance=post)
        if form.is_valid:
            form.save()
            return redirect('posts')
    else:
        form=PostForm(instance=post)
        
    return render(request, 'edit_post.html', {'form': form})

        
    