# """applet URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
# from graphene_django.views import GraphQLView
# from graphql_jwt.decorators import jwt_cookie
#
# from applet.schema import schema
#
# # csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))# this is old auth replaced with graphql_jwt
# urlpatterns = [
#
#     path("graphql", jwt_cookie(GraphQLView.as_view(graphiql=True, schema=schema)))
# ]
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(jwt_cookie(GraphQLView.as_view(
        graphiql=False)))),
    path("graphql2", csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True)))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

