from django.conf.urls import url,include
from django.contrib import admin
from msg_app.views import Home,Log_out,Login,Register,Msg
urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin', admin.site.urls),
    url(r'^register', Register.as_view()),
    url(r'^logout', Log_out.as_view()),
    url(r'^send_msg', Msg.as_view()),
    url(r'^get_msgs/(?P<friend>.*)$', Msg.as_view()),
    url(r'^login', Login.as_view()),
    url(r'^', Home.as_view()),

]