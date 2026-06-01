from django.test import TestCase, RequestFactory
from rest_framework.request import Request
from core.pagination import StandardPagination, SmallPagination, LargePagination


class PaginationConfigTest(TestCase):
    def test_standard_page_size(self):
        self.assertEqual(StandardPagination.page_size, 20)
        self.assertEqual(StandardPagination.max_page_size, 100)

    def test_small_page_size(self):
        self.assertEqual(SmallPagination.page_size, 10)
        self.assertEqual(SmallPagination.max_page_size, 50)

    def test_large_page_size(self):
        self.assertEqual(LargePagination.page_size, 50)
        self.assertEqual(LargePagination.max_page_size, 200)

    def test_page_size_query_param_configurado(self):
        for cls in [StandardPagination, SmallPagination, LargePagination]:
            self.assertEqual(cls.page_size_query_param, "page_size")
