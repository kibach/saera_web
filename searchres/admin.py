from django.contrib import admin
from searchres.models import *

admin.site.register(Document)
admin.site.register(DocumentStemMap)
admin.site.register(DocumentMap)
admin.site.register(Stem)
admin.site.register(Setting)
admin.site.register(Queue)
admin.site.register(IndexerTask)

# Register your models here.
