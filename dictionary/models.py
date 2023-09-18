from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Word(models.Model):
    text = models.CharField(max_length=100)  # The original word
    translation = models.CharField(
        max_length=100, null=True, blank=True)  # The Arabic translation
    language = models.CharField(max_length=10, choices=[
                                ('AR', 'Arabic'), ('BS', 'Bosnian')])
    # Related words in the same language
    related_words = models.ManyToManyField(
        "self", blank=True, symmetrical=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text


class Grammar(models.Model):
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name='grammar_rules')
    content = RichTextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Grammar rule for {self.word.text}" 


class WordFTS(models.Model):
    word = models.OneToOneField(
        Word, on_delete=models.CASCADE, primary_key=True)
    content = models.TextField()
