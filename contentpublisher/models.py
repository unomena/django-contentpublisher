from django.db import models

#==============================================================================
class ContentUpgrade(models.Model):
    """
    Stores sql to upgrade objects on another system.
    """
    object_content_type = models.ForeignKey(ContentType,  related_name='object_set')
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey(ct_field='object_content_type', fk_field='object_id')
    sql = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    must_publish = models.BooleanField(default=True)
    
    #==========================================================================
    class Meta:
        ordering = ('-date_time',)
        unique_together = (('object_content_type','object_id'),)
    
    #--------------------------------------------------------------------------
    def __unicode__(self):
        return self.object

#==============================================================================    
class ContentUpgradeMixin(models.Model):    
    
    #==========================================================================
    class Meta:
        abstract = True
    
    #--------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        
        super(ContentUpgradeMixin, self).save(*args, **kwargs)
        
        if settings.CONTENT_STAGING:
            sqls = []
            for q in db.connection.queries:
                sql = q["sql"]
                if sql not in sqls and not sql.startswith('SELECT') and not sql.startswith('INSERT INTO "django_admin_log"'):
                    sqls.append(sql)
                    
            all_sql = '%s;' % ';\n'.join(sqls)
            cu, created = ContentUpgrade.objects.get_or_create(object_content_type=self.content_type,
                                                               object_id=self.as_leaf_class().id, 
                                                               defaults={'sql' : all_sql})
            if not created:
                cu.sql = all_sql
                cu.save()
    
            #db.reset_queries()
        
