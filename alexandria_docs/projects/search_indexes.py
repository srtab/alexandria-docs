# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import logging

from haystack import indexes

from search.extractors import HtmlExtractor
from projects.models import Project, ImportedFile


logger = logging.getLogger('alexandria.search')


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    """Index main project info"""
    text = indexes.CharField(
        document=True, use_template=True,
        template_name="projects/search/project.txt")
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    absolute_url = indexes.CharField()

    def get_model(self):
        return Project

    def prepare_absolute_url(self, obj):
        return obj.get_absolute_url()


class ImportedFileIndex(indexes.SearchIndex, indexes.Indexable):
    """Index imported files"""
    text = indexes.CharField(
        document=True, template_name="projects/search/imported_file.txt")
    title = indexes.CharField()
    body = indexes.CharField()
    absolute_url = indexes.CharField()

    def get_model(self):
        return ImportedFile

    def prepare_absolute_url(self, obj):
        return obj.get_absolute_url()

    def prepare(self, obj):
        """Open the expected .html file and extract body and title to index"""
        data = super(ImportedFileIndex, self).prepare(obj)
        html = self.get_file_content(obj)
        extractor = HtmlExtractor(html)
        # inject the object to the template with the rich content extracted
        context = {
            'object': obj,
            'title': extractor.title,
            'body': extractor.content
        }
        data['title'] = context['title']
        data['body'] = context['body']
        data['text'] = self.fields['text'].prepare_template(context)
        logger.info('Search Index: indexing file project=%s path=%s',
                    obj.project_id, obj.path)
        return data

    def get_file_content(self, obj):
        try:
            with codecs.open(obj.path, encoding='utf-8', mode='rb') as f:
                return f.read()
        except IOError as e:
            logger.error(
                'Search Index: Unable to index file project=%s path=%s',
                obj.project_id, obj.path, exc_info=e)
        return None
