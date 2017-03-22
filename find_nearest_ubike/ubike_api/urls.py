from django.conf.urls import url
from .views import server_response


urlpatterns = [
    # ex: /v1/ubike-station/taipei?lat=25.034153&lng=121.568509
    url(r'^$', server_response, name='ubike-api' )
]