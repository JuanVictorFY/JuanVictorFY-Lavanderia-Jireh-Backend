from django.urls import path
from .views import AnalyticsView, ExcelPedidosView

urlpatterns = [
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("excel/",     ExcelPedidosView.as_view(), name="excel-export"),
]
