from django.contrib import admin

from users.models import User, Event, SubTitle, Lead, Trial


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'member_id', 'email', 'apk', 'age', 'phone')

    def email(self, obj):
        return obj.user.email

    def phone(self, obj):
        return obj.phone_number


admin.site.register(User, UserAdmin)
admin.site.register(Event)
admin.site.register(SubTitle)
admin.site.register(Lead)
admin.site.register(Trial)
