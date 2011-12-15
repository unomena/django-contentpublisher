'''
Created on 15 Dec 2011

@author: euan
'''
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from contentpublisher import models

def toggle_item(request, item_id):
    """
    Toggle the item.
    """
    item =  get_object_or_404(models.ContentUpgrade, id=item_id)
    if item.must_publish:
        item.must_publish = False
    else:
        item.must_publish = True
    
    item.save()
    
    return HttpResponse(item.must_publish)