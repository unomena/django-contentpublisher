'''
Created on 21 Jun 2011

@author: euan
'''
from django import db
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from contentpublisher.models import ContentUpgrade, ContentM2MUpgrade

#------------------------------------------------------------------------------
def check_sql(sql):
    return not sql.startswith('SELECT') and \
        not sql.startswith('INSERT INTO "django_admin_log"') and \
        not 'contentpublisher_contentupgrade' in sql and \
        not 'contentpublisher_contentm2mupgrade' in sql and \
        not 'SAVEPOINT' in sql
        
#------------------------------------------------------------------------------
def track_object(instance):
    sqls = []
    if settings.CONTENT_STAGING:
        for q in db.connection.queries:
            if check_sql(q['sql']) and q['sql'] not in sqls:
                sqls.append(q['sql'])
                
        db.reset_queries()
        
    if sqls:
        try:
            cu = ContentUpgrade.objects.get(object_content_type=ContentType.objects.get_for_model(instance.__class__),
                                      object_id=instance.id)
            cu.sql = '%s;' % ';\n'.join(sqls)
            cu.must_publish = True
            cu.save()
            
        except ContentUpgrade.DoesNotExist:
            ContentUpgrade.objects.create(object_content_type=ContentType.objects.get_for_model(instance.__class__),
                                          object_id=instance.id, 
                                          sql='%s;' % ';\n'.join(sqls))

#------------------------------------------------------------------------------
def track_saved_object(sender, instance, created, **kwargs):
    """
    Track a saved object
    """
    track_object(instance)

#------------------------------------------------------------------------------
def track_m2m_changed_object(sender, instance, **kwargs):
    """
    Track a saved object
    """
    sqls = []
    if settings.CONTENT_STAGING:
        for q in db.connection.queries:
            if check_sql(q['sql']) and q['sql'] not in sqls:
                sqls.append(q['sql'])
                
        db.reset_queries()
        
    if sqls:
        ContentM2MUpgrade.objects.create(object_content_type=ContentType.objects.get_for_model(instance.__class__),
                                         object_id=instance.id, 
                                         sql='%s;' % ';\n'.join(sqls))

#------------------------------------------------------------------------------
def track_deleted_object(sender, instance, **kwargs):
    """
    Track a deleted object
    """
    track_object(instance)
