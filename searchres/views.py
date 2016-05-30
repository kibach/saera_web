from django.shortcuts import render
from langdetect import detect
import snowballstemmer


LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'fr': 'French',
    'ru': 'Russian',
    'es': 'Spanish',
    'pt': 'Portuguese',
    'it': 'Italian',
    'hr': 'Croatian',
    'mk': 'Macedonian',
    'ar': 'Arabic',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'tr': 'Turkish',
    'pl': 'Polish',
    'sv': 'Swedish',
    'uk': 'Ukrainian',
    'ja': 'Japanese',
    'cs': 'Czech',
    'zh': 'Chinese',
    'kr': 'Korean',
}


def search_result(request):
    query = request.POST.get('query')
    q_words = query.split()
    stemmed_words = []
    for word in q_words:
        lng = detect(word)
        if lng in LANGUAGES:
            lng = LANGUAGES[lng]
            stemmed_words.append(snowballstemmer.stemmer(lng).stemWord(word))
        else:
            stemmed_words.append(word)

    return render(request, 'searchres/search_result.html', {})


def home_page(request):
    return render(request, 'searchres/home_page.html', {})


def indexing_url(request):
    return render(request, 'searchres/indexing_url.html', {})


def editing_url(request):
    return render(request, 'searchres/editing_url.html', {})


def status(request):
    return render(request, 'searchres/status.html', {})


def about(request):
    return render(request, 'searchres/about.html', {})
