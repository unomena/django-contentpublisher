Django-Contentpublisher
=======================

Keeps track of content changes.

Add 'contentpublisher' to 'INSTALLED_APPS' in settings.

Import standard setting into your project settings:

if 'contentpublisher' in INSTALLED_APPS:
    from contentpublisher.settings import *

Add models to be tracked with signals:

models.signals.post_save.connect(track_saved_object, sender=Store)
models.signals.post_save.connect(track_saved_object, sender=ImageOverride)
models.signals.post_delete.connect(track_deleted_object, sender=ImageOverride)
models.signals.m2m_changed.connect(track_m2m_changed_object, sender=ModelBase.sites.through)

Upgrade some content.

Run management command: 'upgradecontent --sql-only' to check what's going to happen.
Run management command: 'upgradecontent' to upgrade to database 'production'
