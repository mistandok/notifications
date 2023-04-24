from django.contrib import admin

from notify.models import Notify, NotifyType, Mailing, Template


# Register your models here.
@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "status", "created_at")
    list_filter = ("status", "created_at")


@admin.register(NotifyType)
class NotifyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Template)
class TemplateTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "period", "next_send")
    list_filter = ("period",)
