from core.models import User, Category
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'khang'
        self.password = '123456'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_page_exists(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('index'))  # Chuyển hướng sau khi đăng nhập thành công

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'username': 'invalid_username', 'password': 'invalid_password'})
        self.assertEqual(response.status_code, 200)  # Trang đăng nhập không chuyển hướng khi đăng nhập không thành công

    def test_logged_in_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session['_auth_user_id'])  # Kiểm tra nếu người dùng đang đăng nhập

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))  # Chuyển hướng sau khi đăng xuất thành công
        self.assertFalse(self.client.session.get('_auth_user_id'))  # Kiểm tra nếu người dùng không còn đăng nhập


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

    def test_get_categories_list(self):
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Giả sử có 2 thể loại ở setUp

    def test_create_category(self):
        url = reverse('categories-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_update_category(self):
        url = reverse('categories-list') + str(self.category1.id) + '/'
        data = {'name': 'Updated Category 1'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Updated Category 1')

    def test_delete_category(self):
        url = reverse('categories-list') + str(self.category1.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
