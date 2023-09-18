from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import WordForm, GrammarForm
from .models import Word, Grammar
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
import unicodedata
from unicodedata import normalize
from django.db.models import F
from .models import Word, WordFTS
from django.db import connection
import arabic_reshaper
from bidi.algorithm import get_display


@login_required
def add_word(request):
    if request.method == 'POST':
        word_form = WordForm(request.POST)
        grammar_form = GrammarForm(request.POST)
        if word_form.is_valid() and grammar_form.is_valid():
            word = word_form.save(commit=False)
            word.user = request.user
            word.save()
            word_form.save_m2m()  # This is necessary for saving many-to-many fields

            # Add the following two lines to create a WordFTS instance:
            # Remember to replace "text" with the actual attribute of your Word model that represents the word text
            content = normalize('NFD', word.text).encode(
                'ascii', 'ignore').decode("utf-8")
            WordFTS.objects.create(word=word, content=content)

            grammar = grammar_form.save(commit=False)
            grammar.word = word
            grammar.user = request.user
            grammar.save()
            return redirect('word_list')
    else:
        word_form = WordForm()
        grammar_form = GrammarForm()
    return render(request, 'dictionary/add_word.html', {'word_form': word_form, 'grammar_form': grammar_form})


  

def home(request):
    return render(request, 'dictionary/home.html')


def word_detail(request, pk):
    word = get_object_or_404(Word, pk=pk)
    return render(request, 'dictionary/word_detail.html', {'word': word})


@login_required
def word_list(request):
    words = Word.objects.filter(user=request.user)
    return render(request, 'dictionary/word_list.html', {'words': words})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('word_list')
    else:
        form = UserCreationForm()
    return render(request, 'dictionary/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('word_list')
    else:
        form = AuthenticationForm()
    return render(request, 'dictionary/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('word_list')


def edit_word(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    grammar = get_object_or_404(Grammar, word=word)
    if request.method == 'POST':
        word_form = WordForm(request.POST, instance=word)
        grammar_form = GrammarForm(request.POST, instance=grammar)
        if word_form.is_valid() and grammar_form.is_valid():
            word_form.save()
            grammar_form.save()
            return redirect('word_list')
    else:
        word_form = WordForm(instance=word)
        grammar_form = GrammarForm(instance=grammar)
    return render(request, 'dictionary/edit_word.html', {'word_form': word_form, 'grammar_form': grammar_form})



def delete_word(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    if request.method == 'POST':
        word.delete()
        return redirect('word_list')
    return render(request, 'dictionary/confirm_delete.html', {'word': word})


def strip_accents(text):
    normalized_text = unicodedata.normalize('NFD', text)
    stripped_text = ''.join(c for c in normalized_text if not unicodedata.combining(
        c) or unicodedata.category(c) != 'Mn')
    return stripped_text


def search_results(request):
    query = request.GET.get('q')

    # Normalize the query
    normalized_query = strip_accents(query.lower())

    # Use WordFTS table to perform the search
    words_fts = WordFTS.objects.filter(content__icontains=normalized_query)

    # Get the Word objects for the results
    words = Word.objects.filter(Q(text__icontains=normalized_query) | Q(
        translation__icontains=normalized_query) | Q(id__in=words_fts.values('word_id')))

    # Create a set to store the unique results
    results = set()

    # Add the matching words and their related words to the result set
    for word in words:
        results.add(word)
        results.update(word.related_words.all())

    return render(request, 'dictionary/search_results.html', {'words': results})
