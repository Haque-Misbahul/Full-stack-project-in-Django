from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SearchForm 
# Create your views here.


def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html', {'tweets': tweets})


@login_required
def tweet_create(request):
    if request.method == "POST":
       form = TweetForm(request.POST, request.FILES)
       if form.is_valid():
          tweet =  form.save(commit=False)
          tweet.user = request.user
          tweet.save()
          return redirect('tweet_list')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id,user =request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance =  tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
       
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confrim_delete.html', {'tweet': tweet})
    

def register(request):
    if request.method == 'POST':
       form =  UserRegistrationForm(request.POST)
       if form.is_valid():
           user = form.save(commit=False)
           user.set_password(form.cleaned_data['password1'])
           user.save()
           login(request, user)
           return redirect('tweet_list')
    else:
        form = UserRegistrationForm()


    return render(request, 'registration/register.html', {'form': form})



def search(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query', '')

    # Perform the search only if there is a query
    if query:
        results = Tweet.objects.filter(text__icontains=query)  # Case-insensitive search for the text
    else:
        results = Tweet.objects.none()  # Return an empty queryset if no query is provided

    # Pass query to the template so it can be displayed in the search bar after submitting
    return render(request, 'search_results.html', {'form': form, 'results': results, 'query': query})