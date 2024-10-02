from django.urls import reverse
from django.utils import timezone
from .models import News, Comment

# Тесты для модели News
class NewsModelTest(TestCase):

    def test_has_comments_true(self):
        """Проверка, что has_comments возвращает True, если есть комментарии"""
        news = News.objects.create(title="Test News", content="Test Content", created_at=timezone.now())
        Comment.objects.create(news=news, content="Test Comment", created_at=timezone.now())
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        """Проверка, что has_comments возвращает False, если комментариев нет"""
        news = News.objects.create(title="Test News", content="Test Content", created_at=timezone.now())
        self.assertFalse(news.has_comments())

# Тесты для представлений
class NewsViewsTest(TestCase):

    def test_news_list_sorted(self):
        """Проверка, что новости выводятся в отсортированном порядке по убыванию"""
        news1 = News.objects.create(title="Old News", content="Content 1", created_at=timezone.now() - timezone.timedelta(days=1))
        news2 = News.objects.create(title="New News", content="Content 2", created_at=timezone.now())
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['news'],
            [news2, news1],
            transform=lambda x: x
        )

    def test_news_detail(self):
        """Проверка, что детальная информация о новости выводится корректно"""
        news = News.objects.create(title="Test News", content="Test Content", created_at=timezone.now())
        url = reverse('news_detail', args=[news.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, news.title)
        self.assertContains(response, news.content)

    def test_news_comments_sorted(self):
        """Проверка, что комментарии выводятся и отсортированы по убыванию"""
        news = News.objects.create(title="Test News", content="Test Content", created_at=timezone.now())
        comment1 = Comment.objects.create(news=news, content="Old Comment", created_at=timezone.now() - timezone.timedelta(days=1))
        comment2 = Comment.objects.create(news=news, content="New Comment", created_at=timezone.now())
        url = reverse('news_detail', args=[news.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['comments'],
            [comment2, comment1],
            transform=lambda x: x
        )