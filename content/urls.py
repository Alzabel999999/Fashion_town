from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views, viewsets
from .viewsets import GlobalSearch


router = DefaultRouter()

router.register(r'news', viewsets.NewsViewSet)
router.register(r'menu_item', viewsets.MenuItemViewSet)
router.register(r'banner', viewsets.BannerViewSet)
router.register(r'review', viewsets.ReviewViewSet)
router.register(r'likes', viewsets.LikesViewSet)
router.register(r'faq', viewsets.FAQViewSet)
router.register(r'question_category', viewsets.QuestionCategoryViewSet)
router.register(r'faq_user_question', viewsets.FAQUserQuestionViewSet)
router.register(r'problem_area', viewsets.ProblemAreaViewSet)
router.register(r'common_feedback', viewsets.CommonFeedbackViewSet)

urlpatterns = router.urls

urlpatterns += [
    re_path(r'page/(?P<slugs>.*)$', views.PageView.as_view()),
    path("search/", GlobalSearch.as_view(), name="global_search"),
]
