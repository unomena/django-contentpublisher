'''
Created on 04 Apr 2011

@author: euan
'''
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections, transaction

from contentpublisher.models import ContentUpgrade

#==============================================================================
class Command(BaseCommand):
    """
    Upgrades Content
    """
    
    help = 'Upgrades flagged content.'

    option_list = BaseCommand.option_list + (
        make_option('-s', '--sql', action='store_true', help='Prints the sql out to upgrade the content'),

        make_option('-x', '--execute', action='store_true', help='Upgrades the content to default or specified database'),

        make_option('-d', '--database', action='store', dest='database',
            default=settings.DEFAULT_CONTENT_PUBLISH_DATABASE, 
            help='Nominates a specific database to publish content to. Defaults to "production".'),
    )
    
    #--------------------------------------------------------------------------
    def handle(self, *args, **options):
        
        using = options.get('database', settings.DEFAULT_CONTENT_PUBLISH_DATABASE)
        print_sql = options.get('sql')
        execute = options.get('execute')
        can_upgrade = False
        content = ContentUpgrade.objects.filter(must_publish=True).order_by('date_time')
        m2m_content = ContentM2MUpgrade.objects.filter(must_publish=True).order_by('date_time')
        
        if content or m2m:
            if settings.DATABASES.has_key(using):
                print 'Will upgrade %d records to database %s' % (content.count() + m2m_content.count(), using)
                can_upgrade = True
            else:
                print 'Need to upgrade %d, but database %s does not exist' % (content.count() + m2m_content.count(), using)
        else:
            print 'No content to upgrade.'
         
        if can_upgrade and execute:
            cursor = connections[using].cursor()
            print 'Preparing to upgrade...'
        
        for content_item in content:
            if print_sql:
                print content_item.sql
                
            if can_upgrade and execute:
                try:
                    cursor.execute(content_item.sql)
                    transaction.commit_unless_managed(using=using)
                    content_item.delete()
                    print 'content upgraded'
                except:
                    print 'content upgrade failed'
                    content_item.must_publish=False
                    content_item.save()
        
        for content_item in m2m_content:
            if print_sql:
                print content_item.sql
                
            if can_upgrade and execute:
                try:
                    cursor.execute(content_item.sql)
                    transaction.commit_unless_managed(using=using)
                    content_item.delete()
                    print 'content upgraded'
                except:
                    print 'content upgrade failed'
                    content_item.must_publish=False
                    content_item.save()
                
                