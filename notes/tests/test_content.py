from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заметка автора',
            text='Текст',
            slug='author-slug',
            author=cls.author
        )

        cls.other_note = Note.objects.create(
            title='Чужая заметка',
            text='Текст',
            slug='reader-slug',
            author=cls.reader
        )
    def test_note_in_object_list(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_other_user_note_not_in_list(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        object_list = response.context['object_list']
        self.assertNotIn(self.other_note, object_list)

    def test_create_page_contains_form(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:add'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_page_contains_form(self):
        self.client.force_login(self.author)
        response = self.client.get(
            reverse('notes:edit', args=(self.note.slug,))
        )
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
