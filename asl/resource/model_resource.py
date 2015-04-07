'''
REST for a DB model.

/articles/

Created on Sep 5, 2013

@author: Peter Morihladko
'''

from sqlalchemy.orm import class_mapper
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

class ResourceQueryContext(object):

    def __init__(self, params, args, data):
        self._params = params
        self._args = args.copy()
        self._args_original = args
        self._data = data

        # Prepare fields and related.
        if 'related' in self._args:
            self._args['related'] = self._args['related'].split(',')

        if 'fields' in self._args:
            self._args['fields'] = self._args['fields'].split(',')
            # we can pass related fields with this, ensure its in 'related' union of two lists
            self._args['related'] = list(set(self._args.get('related', [])) | set(related_from_fields(self._args['fields'])))

    def get_params(self):
        return self._params
    params = property(get_params)

    def get_args(self):
        return self._args
    args = property(get_args)

    def get_data(self):
        return self._data
    data = property(get_data)

    def get_row_id(self):
        return None if len(self.params) == 0 else self.params[0]

    def get_related(self):
        return self._args.get('related', None)

    def get_filter_by(self):
        return self._args.get('filter_by', None)

class ModelResource(SqlSesionMixin):
    '''
    ModelResource works only for tables with a single-column identifier (key).
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

    def _create_context(self, params, args, data):
        return ResourceQueryContext(params, args, data)

    @transactional
    def create(self, params, args, data):
        '''
        POST /resource/model_cls/
        data

        Create new resource
        '''
        ctx = self._create_context(params, args, data)
        model = self._create_one(ctx)
        self._save_one(model, ctx)
        return self._return_saved_one(model, ctx)

    @transactional
    def read(self, params = [], args = {}, data = None):
        '''
        GET /resource/model_cls/[params:id]?[args:{limit,offset,page,per_page,filter_by,order_by,related,fields}]

        Get resource/s
        '''
        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id:
            return self._get_one(row_id, ctx)

        elif 'count' in args:
            return self._get_collection_count(ctx)

        elif 'desc' in args:
            return self._get_collection_desc(ctx)

        else:
            if 'page' in ctx.params:
                page_to_offset(ctx.params)

            return self._get_collection(ctx)

    @transactional
    def update(self, params, args, data):
        '''
        PUT /resource/model_cls/[params:id]
        data

        Update resource/s
        '''
        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id is not None:
            model = self._update_one(ctx)
            return None if model is None else model.get_app_model()
        else:
            return app_models(self._update_collection(ctx))

    @transactional
    def delete(self, params, args, data):
        '''
        DELETE /resource/model_cls/[params]?[args]

        delete resource/s
        '''
        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id is not None:
            return self._delete_one(row_id, ctx)
        else:
            return self._delete_collection(ctx)

    # Create implementation
    def _create_one(self, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        fields = dict_pick(ctx.data, self._model_columns)
        model = self.model_cls(**fields)
        return model

    def _save_one(self, model, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        self._orm.add(model)
        self._orm.flush()

    def _return_saved_one(self, model, ctx):
        return model.get_app_model()

    # Read one implementation.
    def _get_one(self, row_id, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        q = self._orm.query(self.model_cls).filter(self._model_pk == row_id)

        related = ctx.get_related()
        if related is not None:
            q = self.add_related(q, related)
            return nested_model(self._read_one(q, ctx), create_related_tree(related))
        else:
            return self._read_one(q, ctx).get_app_model()

    def _read_one(self, q, ctx):
        return q.one()

    # Read collection implementation.
    def _create_collection_query(self, ctx):
        return self._orm.query(self.model_cls)

    def _get_collection_count(self, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        filter_by = ctx.get_filter_by()

        q = self._create_collection_query(ctx)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        return self._read_collection_count(q, ctx)

    def _read_collection_count(self, q, ctx):
        return q.count()

    def _get_collection(self, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        order_by = ctx.args.get('order_by', None)
        filter_by = ctx.get_filter_by()
        related = ctx.get_related()

        q = self._create_collection_query(ctx)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        if order_by is not None:
            q = self.set_ordering(q, order_by)

        if related is not None:
            q = self.add_related(q, related)
            return nested_models(self._read_collection(q, ctx), create_related_tree(related))
        else:
            return app_models(self._read_collection(q, ctx))

    def _read_collection(self, q, ctx):
        offset = ctx.args.get('offset', 0)
        limit = ctx.args.get('limit', 10)
        if limit is not None and limit != 'unlimited':
            q = q.limit(limit)
        if offset > 0:
            q = q.offset(offset)
        return q.all()

    def _get_collection_desc(self):
        return [column.name for column in class_mapper(self.model_cls).columns]

    # Update
    def _update_one_simple(self, row_id, fields):
        fields = dict_pick(fields, self._model_columns)

        model = self._orm.query(self.model_cls).get(row_id)

        if model is None:
            return None

        for name,value in fields.items():
            setattr(model, name, value)

        return model

    def _update_one(self, ctx):
        '''
        Update row
        '''
        assert isinstance(ctx, ResourceQueryContext)
        fields = ctx.data
        row_id = ctx.get_row_id()
        return self._update_one_simple(row_id, fields)

    def _update_collection(self, ctx):
        '''
        Bulk update
        '''
        assert isinstance(ctx, ResourceQueryContext)
        models = []

        for row in ctx.data:
            models.append(self._update_one_simple(row.pop('id'), row))

        return models

    # Delete methods
    def _delete_one(self, row_id, ctx):
        '''
        Delete row by id
        '''
        assert isinstance(ctx, ResourceQueryContext)

        return self._orm.query(self.model_cls).filter(self._model_pk == row_id).delete()

    def _delete_collection(self, ctx):
        '''
        Delete a collection from DB, optionally filtered by ``filter_by``
        '''
        assert isinstance(ctx, ResourceQueryContext)

        filter_by = ctx.get_filter_by()
        q = self._orm.query(self.model_cls)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        return q.delete()
