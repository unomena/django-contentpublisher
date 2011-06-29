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
        make_option('--sql-only', action='store_false', default='False', help='Prints the sql out to upgrade the content'),
                    
        make_option('--database', action='store', dest='database',
            default=settings.DEFAULT_CONTENT_PUBLISH_DATABASE, 
            help='Nominates a specific database to publish content to. Defaults to "production".'),
    )
    
    #--------------------------------------------------------------------------
    def handle(self, *args, **options):
        
        using = options.get('database', settings.DEFAULT_CONTENT_PUBLISH_DATABASE)
        sql_only = not options.get('sql-only')
        
        if not sql_only:
            cursor = connections[using].cursor()
        
        for content_upgrade in ContentUpgrade.objects.filter(must_publish=True).order_by('date_time'):
            print content_upgrade.sql
            if not sql_only:
                cursor.execute(content_upgrade.sql)
                transaction.commit_unless_managed(using=using)
                content_upgrade.delete()
                print 'content upgraded'