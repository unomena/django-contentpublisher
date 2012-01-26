from django.contrib import admin
from contentpublisher.models import ContentUpgrade, ContentM2MUpgrade

admin.site.register(ContentUpgrade)
admin.site.register(ContentM2MUpgrade)
