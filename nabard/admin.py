from django.contrib import admin


class Admin(admin.ModelAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
