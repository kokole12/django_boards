from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board,User, Topic, Post
from django.http import Http404
from .forms import NewTopicForm
# Create your views here.

def home(request):
    boards = Board.objects.all()
    
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    """board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})
    """
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user  = User.objects.first()
    if request.method == 'POST':
        """subject = request.POST['subject']
        message =  request.POST['message']

        user =  User.objects.first()

        topic = Topic.objects.create(
            subject = subject,
            board = board,
            starter = user
        )"""
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

        return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
