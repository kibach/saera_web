from django.shortcuts import render, redirect
from langdetect import detect
from searchres.models import *
import snowballstemmer
import math


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
    if not request.method == "POST":
        return redirect('/')

    query = request.POST.get('query')
    q_words = query.split()
    stemmed_words = []
    for word in q_words:
        lng = detect(word)
        if lng in LANGUAGES:
            lng = LANGUAGES[lng].lower()
            stemmed_words.append(snowballstemmer.stemmer(lng).stemWord(word))
        else:
            stemmed_words.append(word)

    doc_ratings = {}

    for word in stemmed_words:
        try:
            stem = Stem.objects.get(stem=word)
        except:
            continue

        term_ratings = {}
        for relation in DocumentStemMap.objects.filter(stem=stem):
            if relation.doc_id in term_ratings:
                term_ratings[relation.doc_id] += relation.rank_component
            else:
                term_ratings[relation.doc_id] = relation.rank_component

        for doc_id in term_ratings:
            term_ratings[doc_id] = term_ratings[doc_id] / (2 + term_ratings[doc_id]) * stem.idf
            if doc_id in doc_ratings:
                doc_ratings[doc_id] += term_ratings[doc_id]
            else:
                doc_ratings[doc_id] = term_ratings[doc_id]

        del term_ratings

    rated_docs = doc_ratings.items()

    rated_docs.sort(key=lambda x: x[1], reverse=True)
    results = []
    for doc_id in rated_docs[:10]:
        results.append(Document.objects.get(id=doc_id[0]))

    return render(request, 'searchres/search_result.html', {
        'documents': results,
        'query': query,
    })


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
