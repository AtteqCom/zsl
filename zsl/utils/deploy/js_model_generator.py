'''
:mod:`asl.utils.deploy.js_model_generator`

.. moduleauthor:: Peter Morihladko
'''

import json
import importlib
from zsl.utils.string_helper import camelcase_to_underscore, underscore_to_camelcase
from sqlalchemy.orm import class_mapper
import sqlalchemy.exc

model_tpl = """    {model_prefix}{model_name} = {model_fn}.extend({{
        urlRoot: App.service_url + 'resource/{resource_name}',
        schema: {schema}
    }});

    {collection_prefix}{model_name} = {collection_fn}.extend({{
        model: {model_prefix}{model_name},
        url: {model_prefix}{model_name}.prototype.urlRoot
    }});
"""


list_opts_tpl = """function(callback, field) {{
                    field.setOptions(new {collection_prefix}{model_name}([],{{limit: 'unlimited'}}));
                }}"""

class ModelGenerator(object):
    def __init__(self, module, model_prefix="", collection_prefix="", model_fn="Atteq.bb.Model", collection_fn="Atteq.bb.Collection"):
        self.model_prefix = model_prefix
        self.collection_prefix = collection_prefix
        self.model_fn = model_fn
        self.collection_fn = collection_fn
        self.table_to_class = {}

        self.models = importlib.import_module(module)

    def _get_list_options(self, column):
        fk = list(column.foreign_keys)[0]
        
        table_name = underscore_to_camelcase(fk.column.table.name)
        
        return list_opts_tpl.format(collection_prefix=self.collection_prefix, model_name=table_name)
    
    def _map_table_name(self, model_names):
        """
        Pre foregin_keys potrbejeme pre z nazvu tabulky zistit class,
        tak si to namapujme
        """
        
        for model in model_names:
            if isinstance(model, tuple):
                model = model[0]

            try:
                model_cls = getattr(self.models, model)
                self.table_to_class[class_mapper(model_cls).tables[0].name] = model
            except AttributeError:
                pass

    def generate_model(self, model_name, model_plural=None):
        if model_name not in dir(self.models):
            raise ImportError("Model [{name}] couldn't be found in {module}\n".format(name=model_name, module=self.models.__name__))
        
        if model_plural is None:
            model_plural = model_name + 's'
        
        model = getattr(self.models, model_name)
        
        schema = {}
        mapper = class_mapper(model)
        callbacks = []
    
        for column in mapper.columns:
            col_type = column.type.__class__.__name__
            attrs = {}
            
            if column.primary_key:
                continue
            
            if column.foreign_keys:
                try:
                    attrs['type'] = 'AtteqSelect'
                    attrs['options'] = '__CALLBACK__%d' % len(callbacks)
                    callbacks.append(self._get_list_options(column))
                    
                    # TODO uf uf uuuuf
                    fk_table = list(column.foreign_keys)[0].target_fullname.split('.')[0]
                    
                    if fk_table in self.table_to_class:
                        attrs['foreign_model'] = '%s%s' % (self.model_prefix, self.table_to_class[fk_table])
                    
                except sqlalchemy.exc.NoReferencedTableError:
                    attrs['type'] = 'Text'
                
            elif col_type == 'TEXT':
                attrs['type'] = "TextArea"
                
            elif col_type == 'Enum':
                attrs['type'] = 'AtteqSelect' if column.nullable else 'Select'
                attrs['options'] = column.type.enums
            
            elif col_type == 'INTEGER':
                attrs['type'] = 'Number'
                    
            else:
                attrs['type'] = "Text"

            if column.nullable:
                attrs['nullable'] = True
            
            schema[column.name] = attrs
        
        schema = "\n        ".join(json.dumps(schema, indent=4).split("\n"))
        
        for i in xrange(len(callbacks)):
            schema = schema.replace('"__CALLBACK__%d"' % i, callbacks[i])
        
        return model_tpl.format(
            model_name = model_name,
            model_prefix = self.model_prefix,
            collection_prefix = self.collection_prefix,
            resource_name = camelcase_to_underscore(model_plural), 
            model_fn = self.model_fn,
            collection_fn = self.collection_fn,
            schema = schema
        )
    
    def generate_models(self, models):
        js_models = []
        
        self._map_table_name(models)
        
        for model in models:
            if isinstance(model, tuple):
                model_name = model[0]
                model_plural = model[1]
            else:
                model_name = model
                model_plural = None
                
            js_model = self.generate_model(model_name, model_plural)
            js_models.append(js_model)
            
        return js_models
