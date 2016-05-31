from django.shortcuts import render, redirect
from langdetect import detect, detect_langs
from searchres.models import *
from django.db.models import *
from django.db.models.functions import Length
from django.http import HttpResponse
from django.core.validators import URLValidator
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
    if not request.method == "POST":
        return redirect('/')

    query = request.POST.get('query')
    q_words = query.split()
    stemmed_words = []
    for word in q_words:
        lngs = detect_langs(word)
        correct_lng = 'english'
        for lng in lngs:
            if lng in LANGUAGES and LANGUAGES[lng].lower() in snowballstemmer.algorithms():
                correct_lng = LANGUAGES[lng].lower()
        stemmed_words.append(snowballstemmer.stemmer(correct_lng).stemWord(word))

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
    if request.method == "POST":
        uv = URLValidator(schemes=['http', 'https'])
        form = request.POST.get('urls')
        was_added = False
        if form:
            for url in form.split('\n'):
                url = url.strip()
                if not uv(url):
                    continue
                qi = Queue()
                qi.url = url
                qi.parent = 0
                qi.depth = 0
                qi.save()
                was_added = True

        urlfile = request.FILES.get('urlfile')
        if urlfile:
            for url in urlfile:
                url = url.strip()
                if not uv(url):
                    continue
                qi = Queue()
                qi.url = url
                qi.parent = 0
                qi.depth = 0
                qi.save()
                was_added = True

        if was_added:
            task = IndexerTask()
            task.type = 'reload_queue'
            task.parameters = ''
            task.completed = False
            task.created_at = datetime.datetime.now()
            task.save()
            msg = 'OK'
        else:
            msg = 'No valid URLs found'

    else:
        msg = None
    return render(request, 'searchres/indexing_url.html', {
        'msg': msg
    })


def editing_url(request):
    return render(request, 'searchres/editing_url.html', {})


def status(request):
    if not request.user.is_authenticated():
        return redirect('/admin/')

    doc_cnt = Document.objects.count()
    ind_size = Document.objects.aggregate(Sum(Length('contents')))
    return render(request, 'searchres/status.html', {
        'doc_cnt': doc_cnt,
        'ind_size': ind_size,
        'documents': Document.objects.all().order_by(Document.pk),
    })


def about(request):
    return render(request, 'searchres/about.html', {})


def url_delete(request, urlid):
    if not request.user.is_authenticated():
        return redirect('/admin/')

    del_ur = Document.url.get(pk=urlid)
    DocumentMap.objects.filter(A=del_ur).delete()
    DocumentMap.objects.filter(B=del_ur).delete()
    DocumentStemMap.objects.filter(doc=del_ur).delete()
    del_ur.delete()
    return redirect('/status/')


def url_html(request, urlid):
    doc = Document.objects.get(pk=urlid)
    resp = HttpResponse(content_type='text/html')
    resp.write(doc.contents)
    return resp


def url_plain(request, urlid):
    doc = Document.objects.get(pk=urlid)
    resp = HttpResponse(content_type='text/plain')
    resp.write(doc.plaintext)
    return resp