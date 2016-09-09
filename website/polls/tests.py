import datetime
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """ Was published recently should return False if future date. """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ Was published recently should return False if old date. """

        time = timezone.now() - datetime.timedelta(days=30)
        question = Question(pub_date=time)
        self.assertIs(question.was_published_recently(), False)
        
    def test_was_published_recently_with_current_question(self):
        """ Was published recently should return True if current date. """

        time = timezone.now() - datetime.timedelta(hours=1)
        question = Question(pub_date=time)
        self.assertIs(question.was_published_recently(), True)

class QuestionListViewTests(TestCase):
    """Test the question view"""
    def setUp(self):
        setup_test_environment() 

    def test_only_recent_questions_shown(self):
        client = Client()
        for i in range(-1,2):
            q = Question(pub_date=timezone.now()+datetime.timedelta(days=i))
            q.save()
        response = client.get(reverse('polls:index'))
        self.assertIs(len(response.context['latest_question_list']), 2)

