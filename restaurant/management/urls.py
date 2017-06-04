from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_item/$', views.add_item, name='add_item'),
    url(r'^view_item_list/$', views.view_item_list, name='view_item_list'),
    url(r'^view_item/detail/$', views.item_detail, name='item_detail'),
    url(r'^view_item/del/$', views.delItem, name='delItem'),
    url(r'^view_user_list/$', views.view_user_list, name='view_user_list'),
    url(r'^add_order/$', views.add_order, name='add_order'),
    url(r'^view_order_list/$', views.view_order_list, name='view_order_list'),
    url(r'^view_order/detail/$', views.order_detail, name='order_detail'),
    url(r'^add_orderItem/$', views.add_orderItem, name='add_orderItem'),
    url(r'^view_user/del/$', views.delUser, name='delUser'),
    url(r'^view_order/del/$', views.delOrder, name='delOrder'),
    url(r'^view_item/edit/$', views.editItem, name='editItem'),
    url(r'^view_OrderItem/edit/$', views.editOrderItem, name='editOrderItem'),
    url(r'^view_orderItem/del/$', views.delOrderItem, name='delOrderItem'),

]
