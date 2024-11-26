from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Artwork)
admin.site.register(Transaction)
admin.site.register(Exhibition)
admin.site.register(Notification)


from django.contrib import admin
from .models import Exhibition, Notification, User

admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'artwork']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Send notifications to Artists and Customers
        users = User.objects.filter(role__in=['Artist', 'Customer'])
        for user in users:
            Notification.objects.create(
                recipient=user,
                message=f"New Exhibition '{obj.title}' has been created! "
                        f"Check out the artwork: {obj.artwork.title}"
            )
