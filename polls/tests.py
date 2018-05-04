# -*- coding:utf-8 -*-\
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    """Question tests"""

    def test_was_published_recently_with_future_question(self):
        """
        pub_date 가 미래값이라면 was_published_recently() 는 False 를
        반환해야 합니다
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        pub_date 가 1일 이상 과거이면 was_published_recently() 는 False 를
        반환해야 합니다
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_qeustion(self):
        """
        pub_date 가 지난 1일 이내일 경우 was_published_recently() 는 True 를
        반환해야 합니다
        """
        time = timezone.now() -\
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    `question_text` 를 받아서 `Question`을 생성합니다. 오늘로부터 `days` 만큼 이동한 날짜로
    게시일이 주어집니다
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        `Question`이 없으면 안내 메시지 출력 
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        과거 `Question`을 넣으면 출력된다
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        미래의 `Question`은 출력되지 않는다
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_future_question_and_past_question(self):
        """
        만약 미래와 과거 `Question`이 모두 있으면 과거만 출력된다
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        하나 이상의 `Question` 들을 출력할 수 있다 
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        상세보기에서 미래 게시물인 경우 404 를 리턴한다
        """
        future_question = create_question(
            question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        상세보기에서 과거 게시물인 경우 텍스트를 출력한다
        """
        past_question = create_question(
            question_text="Future question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
