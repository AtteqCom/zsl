'''
REST for a DB model.

/articles/

Created on Sep 5, 2013

@author: Peter Morihladko
'''

from sqlalchemy.orm import class_mapper
from asl.application.initializers.database_initializer import SessionHolder
from asl.resource.resource_helper import filter_from_url_arg, apply_related, create_related_tree,\
    related_from_fields, order_from_url_arg
from functools import partial
from asl.db.helpers import app_models
from asl.db.helpers.nested import nested_models, nested_model
from asl.service.service import transactional, SqlSesionMixin

def dict_pick(dictionary, allowed_keys):
    '''
    Return a dictionary only with keys found in ``allowed_keys``
    '''
    return dict((key, value) for (key,value) in dictionary.items() if key in allowed_keys)

def page_to_offset(params):
    '''
    Transform 'page'/'per_page' to 'limit'/'offset'
    '''
    
    if 'page' not in params:
        return
    
    page = params['page']
    del params['page']

    # 'per_page' je len alias za 'limit'
    if 'per_page' in params:
        per_page = params.get('per_page')
        del params['per_page']
    else:
        per_page = params.get('limit', 10)
    
    params['offset'] = int(per_page) * (int(page) - 1)
    params['limit'] = per_page
    
class ModelResource(SqlSesionMixin):
    '''
    TODO: zatial to funguje iba na tabulky s 1 primary key
    '''

    def __init__(self, model_cls):
        """
        Create Model CRUD resource for ``model_cls``
        """
        
        self.init_sql_session()
        
        self.model_cls = model_cls

        mapper = class_mapper(model_cls)
        self._model_pk = mapper.primary_key[0]
        self._model_columns = [column.key for column in mapper.column_attrs]

        self.to_filter = partial(filter_from_url_arg, model_cls)
        self.add_related = partial(apply_related, model_cls)
        self.set_ordering = partial(order_from_url_arg, model_cls)

    @transactional
    def create(self, params, args, data):
        '''
        POST /resource/model_cls/
        data

        Create new resource
        '''
        fields = dict_pick(data, self._model_columns)

        model = self.model_cls(**fields)
        self._orm.add(model)
        self._orm.flush()

        return model.get_app_model()

    
    @transactional
    def read(self, params = [], args = {}, data = None):
        '''
        GET /resource/model_cls/[params:id]?[args:{limit,offset,page,per_page,filter_by,order_by,related,fields}]

        Get resource/s
        '''
        row_id = params[0] if len(params) > 0 else None

        args = args.copy()

        if 'related' in args:
            args['related'] = args['related'].split(',')

        if 'fields' in args:
            args['fields'] = args['fields'].split(',')

            # we can pass related fields with this, ensure its in 'related'
            # union of two lists
            args['related'] = list(set(args.get('related', [])) | set(related_from_fields(args['fields'])))

        if row_id:
            return self.get_one(row_id, args.get('related'))

        elif 'count' in args:
            return self.get_collection_count(args.get('filter_by'))

        elif 'desc' in args:
            return self.get_collection_desc()

        else:
            kwargs = dict_pick(args, ['limit', 'offset', 'filter_by', 'order_by', 'related', 'page', 'per_page'])
            
            if 'page' in kwargs:
                page_to_offset(kwargs)
            
            return self.get_collection(**kwargs)

    @transactional
    def update(self, params, args, data):
        '''
        PUT /resource/model_cls/[params:id]
        data

        Update resource/s
        '''
        row_id = params[0] if len(params) > 0 else None

        if row_id is not None:
            return self.update_one(row_id, data)
        else:
            return self.update_collection(data)

    @transactional
    def delete(self, params, args, data):
        '''
        DELETE /resource/model_cls/[params]?[args]

        delete resource/s
        '''
        row_id = params[0] if len(params) > 0 else None

        if row_id is not None:
            return self.delete_one(row_id)
        else:
            return self.delete_collection(args.get('filter_by', None))

    def get_one(self, row_id, related=None):
        q = self._orm.query(self.model_cls).filter(self._model_pk == row_id)

        if related is not None:
            q = self.add_related(q, related)

            return nested_model(q.one(), create_related_tree(related))
        else:
            return q.one().get_app_model()


    def get_collection_count(self, filter_by=None):
        q = self._orm.query(self.model_cls)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        return q.count()

    def get_collection(self, limit=10, offset=0, filter_by=None, order_by=None, related=None):
        q = self._orm.query(self.model_cls)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        if order_by is not None:
            q = self.set_ordering(q, order_by)

        if limit is not None and limit != 'unlimited':
            q = q.limit(limit)

        if offset > 0:
            q = q.offset(offset)

        if related is not None:
            q = self.add_related(q, related)

            return nested_models(q.all(), create_related_tree(related))
        else:
            return app_models(q.all())

    def get_collection_desc(self):
        return [column.name for column in class_mapper(self.model_cls).columns]

    def _update_one_simple(self, row_id, fields):
        fields = dict_pick(fields, self._model_columns)

        model = self._orm.query(self.model_cls).get(row_id)

        if model is None:
            return None

        for name,value in fields.items():
            setattr(model, name, value)

        return model

    def update_one(self, row_id, fields={}):
        '''
        Update row
        '''

        model = self._update_one_simple(row_id, fields)

        return None if model is None else model.get_app_model()

    def update_collection(self, rows=[]):
        '''
        Bulk update
        '''
        models = []

        for row in rows:
            models.append(self.update_one(row.pop('id'), row))

        return models

    def delete_one(self, row_id):
        '''
        Delete row by id
        '''
        return self._orm.query(self.model_cls).filter(self._model_pk == row_id).delete()

    def delete_collection(self, filter_by=None):
        '''
        Delete a collection from DB, optionally filtered by ``filter_by``
        '''
        q = self._orm.query(self.model_cls)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        return q.delete()
