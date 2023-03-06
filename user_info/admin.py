from django.contrib import admin
from .models import (KumbioUser, KumbioUserPermission, KumbioUserRole, NotificationsSettings, ToDoList, ToDoListTask)

admin.site.register(KumbioUser)
admin.site.register(KumbioUserPermission)
admin.site.register(KumbioUserRole)
admin.site.register(NotificationsSettings)
admin.site.register(ToDoList)
admin.site.register(ToDoListTask)
