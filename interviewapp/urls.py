from . import views
from django.urls import path
from.views import homepage
from.views import regspage
from.views import register1
from.views import login2
#from.views import homepage1

urlpatterns = [
   
    path('',views.homepage,name='homepage'),
    path('regspage',views.regspage,name='regspage'),
    path('register1',views.register1,name='register1'),
    path('instruction',views.instruction,name='instruction'),
    path('testresult',views.testresult,name='testresult'),
    path('finalresult',views.finalresult,name='finalresult'),
    path('adminlv',views.adminlv,name='adminlv'),
    path('login2',views.login2,name='login2'),
    #path('loginpage',views.loginpage,name='loginpage'),
    path('homepage1',views.homepage1,name='homepage1'),
    path('userview',views.userview,name='userview'),
    path('finalresult',views.finalresult,name='finalresult'),
    path('index',views.index,name='index'),
    path('add',views.add,name='add'),
    path('addrecord/',views.addrecord,name='addrecord'),
    path('delete/<int:fld_slno>',views.delete,name='delete'),
    path('update/<int:fld_slno>',views.update,name='update'),
    path('update/updaterecord/<int:fld_slno>',views.updaterecord,name='updaterecord'),
    path('logout',views.logout,name='logout'),
    path('stored_proc',views.stored_proc,name='stored_proc'),
    path('userpage',views.userpage,name='userpage'),
    path('show_registeruser', views.show_registeruser, name='show_registeruser'),
    path('user_result',views.user_result,name='user_result'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('retun_page',views.retun_page,name='retun_page'),
    # path('serve-file/', views.serve_file, name='serve_file'),
    path('downloadfile/<int:user_id>/', views.downloadfile, name='downloadfile'),
    path('total_test', views.total_test, name='total_test'),
    path('today_test', views.today_test, name='today_test')

    ]