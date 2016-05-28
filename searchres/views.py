from django.shortcuts import render


def search_result(request):
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
