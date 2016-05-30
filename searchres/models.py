from django.db import models


class Document(models.Model):
    url = models.CharField(max_length=2000, db_index=True)
    domain = models.CharField(max_length=500, db_index=True)
    title = models.CharField(max_length=1000)
    language = models.CharField(max_length=20)
    encoding = models.CharField(max_length=20)
    contents = models.TextField()
    plaintext = models.TextField()
    indexed_at = models.DateTimeField()


class Stem(models.Model):
    stem = models.CharField(max_length=500, unique=True)


class DocumentMap(models.Model):
    A = models.IntegerField(db_index=True)
    B = models.IntegerField(db_index=True)


class DocumentStemMap(models.Model):
    doc = models.ForeignKey(Document, db_index=True)
    stem = models.ForeignKey(Stem, db_index=True)
    count = models.IntegerField()
    type = models.IntegerField()


class Setting(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)


class Queue(models.Model):
    url = models.CharField(max_length=2000)
    depth = models.IntegerField()
    parent = models.IntegerField()


class IndexerTask(models.Model):
    created_at = models.DateTimeField()
    type = models.CharField(max_length=100)
    parameters = models.TextField()
    completed = models.BooleanField()
