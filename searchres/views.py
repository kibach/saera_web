from django.shortcuts import render
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

    doc_cnt = Document.objects.count()

    avg_fl = {'1': 0, '2': 0}
    for doc in Document.objects.all():
        for field_id in ['1', '2']:
            for entry in DocumentStemMap.objects.filter(doc=doc, type=field_id):
                avg_fl[field_id] += entry.count * len(entry.stem.stem)

    for field_id in ['1', '2']:
        avg_fl[field_id] = avg_fl[field_id] / doc_cnt

    rated_docs = []

    for doc in Document.objects.all():
        doc_fl = {'1': 0, '2': 0}
        w = 0

        for field_id in ['1', '2']:
            for entry in DocumentStemMap.objects.filter(doc=doc, type=field_id):
                doc_fl[field_id] += entry.count * len(entry.stem.stem)

        for word in stemmed_words:
            try:
                stem_obj = Stem.objects.get(stem=word)
            except models.ObjectDoesNotExist:
                continue

            cw = 0
            for field_id in ['1', '2']:
                occurs = DocumentStemMap.objects.filter(doc=doc, stem=stem_obj, type=field_id)
                if occurs.exists():
                    occurs_word = occurs.first()
                    occurs_count = occurs_word.count
                else:
                    occurs_count = 0

                comp = occurs_count * (3 - int(field_id)) / (0.25 + 0.75 * (doc_fl[field_id] / avg_fl[field_id]))
                if comp < 0:
                    comp = 0

                cw += comp

            df = DocumentStemMap.objects.filter(stem=stem_obj).values('doc_id').annotate(tmp=models.Count('type')).count()
            w += cw / (0.5 + cw) * math.log((doc_cnt - df + 0.5) / (df + 0.5))

        rated_docs.append((doc.id, w))

    rated_docs.sort(key=lambda x: x[1])
    results = []
    for doc_id in rated_docs[:10]:
        results.append(Document.objects.get(id=doc_id[0]))

    return render(request, 'searchres/search_result.html', {'documents': results})


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
