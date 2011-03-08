from django.contrib import admin
from test_app.models import TestModel

class TestModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ("First", {
            "classes": ("first", ),
            "fields": ("title", "slug", )
        }),
        ("Second", {
            "classes": ("second", ),
            "fields": ("content", "meta_info", )
        }),
    ]

admin.site.register(TestModel, TestModelAdmin)
