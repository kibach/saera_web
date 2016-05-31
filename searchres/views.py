from django.shortcuts import render, redirect
from langdetect import detect, detect_langs
from searchres.models import *
from django.db.models import *
from django.db.models.functions import Length
from django.http import HttpResponse
from django.core.validators import URLValidator
import snowballstemmer
import datetime


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
    filters = []
    for word in q_words:
        if word.startswith('domain:'):
            filters.append(('domain', word.replace('domain:', '').lower()))
        elif word.startswith('lang:'):
            filters.append(('lang', word.replace('lang:', '').lower()))
        elif word.startswith('encoding:'):
            filters.append(('encoding', word.replace('encoding:', '').lower()))
        else:
            try:
                lngs = detect_langs(word)
                correct_lng = 'english'
                for lng in lngs:
                    if lng in LANGUAGES and LANGUAGES[lng].lower() in snowballstemmer.algorithms():
                        correct_lng = LANGUAGES[lng].lower()
                stemmed_words.append(snowballstemmer.stemmer(correct_lng).stemWord(word))
            except:
                stemmed_words.append(word)

    doc_ratings = {}

    for word in stemmed_words:
        try:
            stem = Stem.objects.get(stem=word)
        except:
            continue

        term_ratings = {}
        for relation in DocumentStemMap.objects.filter(stem=stem):
            for fil in filters:
                if fil[0] == 'domain':
                    if not fil[1] in relation.doc.domain:
                        continue
                elif fil[0] == 'lang':
                    if not fil[1] == relation.doc.language:
                        continue
                elif fil[0] == 'encoding':
                    if not fil[1] == relation.doc.encoding:
                        continue

            rc = relation.rank_component
            if rc < 0:
                rc = 0
            if relation.doc_id in term_ratings:
                term_ratings[relation.doc_id] += rc
            else:
                term_ratings[relation.doc_id] = rc

        for doc_id in term_ratings:
            term_ratings[doc_id] = term_ratings[doc_id] / (2 + term_ratings[doc_id]) * stem.idf
            if doc_id in doc_ratings:
                doc_ratings[doc_id] += term_ratings[doc_id]
            else:
                doc_ratings[doc_id] = term_ratings[doc_id]

        del term_ratings

    rated_docs = doc_ratings.items()

    rated_docs.sort(key=lambda x: x[1])
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
                try:
                    uv(url)
                except:
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
                try:
                    uv(url)
                except:
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
    ind_size = Document.objects.aggregate(isize=Sum(Length('contents')))['isize']
    return render(request, 'searchres/status.html', {
        'doc_cnt': doc_cnt,
        'ind_size': ind_size,
        'documents': Document.objects.all().order_by('id'),
    })


def about(request):
    return render(request, 'searchres/about.html', {})


def url_delete(request, urlid):
    if not request.user.is_authenticated():
        return redirect('/admin/')

    del_ur = Document.objects.get(pk=urlid)
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