'''
Created on 21 Jun 2011

@author: euan
'''
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

#==============================================================================
class ContentUpgrade(models.Model):
    """
    Stores sql to upgrade objects on another system.
    """
    object_content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    object = generic.GenericForeignKey(ct_field='object_content_type', fk_field='object_id')
    sql = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    must_publish = models.BooleanField(default=True)
    
    #==========================================================================
    class Meta:
        ordering = ('-date_time',)
#        unique_together = (('object_content_type','object_id'),)
    
    #--------------------------------------------------------------------------
    def __unicode__(self):
        return str(self.object)