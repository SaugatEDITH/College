from django.urls import path
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Make sure this is named 'home'
    path('about', views.about, name='about'),
    path('blogs', views.BlogListView.as_view(), name='blogs'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='Blog_Depth'),
    path('notice', views.NoticeListView.as_view(), name='notice'),
    # path('faqs', views.FAQView.as_view(), name='faq'),
    path('faqs', views.faq, name='faq'),
    # programs starts
    path('bcaProgram/', views.ProgramView.as_view(template_name='collegeapp/bcaProgram.html'), name='bca_program'),
    path('bscCsitProgram/', views.ProgramView.as_view(template_name='collegeapp/bscCsitProgram.html'), name='bsc_csit_program'),
    path('plus2Program/', views.ProgramView.as_view(template_name='collegeapp/plus2Program.html'), name='plus2_program'),
    path('bbsProgram/', views.ProgramView.as_view(template_name='collegeapp/bbsProgram.html'), name='bbs_program'),
    path('admission-procedure/', views.ProgramView.as_view(template_name='collegeapp/admission-procedure.html'), name='admission_procedure'),
    # programs ends    
    path('notice/<slug:slug>/', views.NoticeDetailView.as_view(), name='noticedetail'),
    path('contact', views.contact, name='contact'),
    path('gallary', views.gallery, name='gallary'),
    path('about/leadership', views.AboutLeadershipView.as_view(), name='leadership'),
    path('our-team', views.OurTeamListView.as_view(),name = 'ourteam'),
    path('apply-online', views.applyonline, name='applyonline'),
    path('hello-world', views.helloworld, name='helloworld'),
    path('Downloads', views.Downloads, name='downloads'),
    path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacypolicy'),
    path('teacher-login',views.LoginTeacherView.as_view(),name='teacher-login'),
    path('teacher-logout', views.teacher_logout, name='teacher-logout'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher-dashboard')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)