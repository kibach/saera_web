from django.db import models


class Document(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    domain = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=20)
    encoding = models.CharField(max_length=20)
    contents = models.TextField()
    plaintext = models.TextField()
    indexed_at = models.DateTimeField()

    def __str__(self):
        return self.title + ' (' + self.url + ')'


class Stem(models.Model):
    stem = models.CharField(max_length=255, unique=True)
    idf = models.FloatField()

    def __str__(self):
        return self.stem + ' / ' + str(self.idf)


class DocumentMap(models.Model):
    A = models.IntegerField(db_index=True)
    B = models.IntegerField(db_index=True)

    def __str__(self):
        return str(self.A) + ' -> ' + str(self.B)


class DocumentStemMap(models.Model):
    doc = models.ForeignKey(Document, db_index=True)
    stem = models.ForeignKey(Stem, db_index=True)
    count = models.IntegerField()
    type = models.IntegerField()
    rank_component = models.FloatField()

    def __str__(self):
        return self.doc.title + ' -> ' + self.stem.stem


class Setting(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' = ' + self.value


class Queue(models.Model):
    url = models.CharField(max_length=255)
    depth = models.IntegerField()
    parent = models.IntegerField()

    def __str__(self):
        return self.url + ' / ' + str(self.depth)


class IndexerTask(models.Model):
    created_at = models.DateTimeField()
    type = models.CharField(max_length=100)
    parameters = models.TextField()
    completed = models.BooleanField()

    def __str__(self):
        return self.type + ' / Completed: ' + str(self.completed)
