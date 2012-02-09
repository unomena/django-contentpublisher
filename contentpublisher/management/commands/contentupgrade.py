'''
Created on 04 Apr 2011

@author: euan
'''
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.sites.models import Site

from contentpublisher.models import ContentUpgrade

#==============================================================================
class Command(BaseCommand):
    """
    Upgrades Content
    """
    
    help = 'Upgrades flagged content.'

    option_list = BaseCommand.option_list + (
        make_option('-x', '--execute', action='store_true', help='Upgrades the content to default or specified database'),

        make_option('-d', '--database', action='store', dest='database',
            default=settings.DEFAULT_CONTENT_PUBLISH_DATABASE, 
            help='Nominates a specific database to publish content to. Defaults to "production".'),
    )
    
    #--------------------------------------------------------------------------
    def handle(self, *args, **options):
        
        using = options.get('database', settings.DEFAULT_CONTENT_PUBLISH_DATABASE)
        execute = options.get('execute')
        can_upgrade = False
        content = ContentUpgrade.objects.filter(must_publish=True).order_by('date_time')
        
        if content:
            if settings.DATABASES.has_key(using):
                print 'Will upgrade %d records to database %s' % (content.count(), using)
                can_upgrade = True
            else:
                print 'Need to upgrade %d, but database %s does not exist' % (content.count(), using)
        else:
            print 'No content to upgrade.'
        
        for content_item in content:
            if can_upgrade and execute:
                
                print 'Upgrading: %s' % str(content_item.object)
                
                content_item.object.save(using=using)
                
                if hasattr(content_item.object, 'sites'):
                    for site in content_item.object.sites.all():
                        type(content_item.object).objects.using(using).get(pk=content_item.object.id).sites.add(Site.objects.using(using).get(name=site.name))
                        
                try:
                    content_item.object.content_publish_extra(using)
                except:
                    pass
                
                content_item.delete()
                
                