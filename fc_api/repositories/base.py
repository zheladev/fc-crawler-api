from datetime import datetime
from typing import Union
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.sql.expression import desc, asc


class BaseRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def create(self, flush=True, **kwargs):
        """
        Creates a new instance of this object in the database
        :param flush: Flush directly or not
        :param kwargs: Object attributes and values
        :return: Newly created object
        """
        object_ = self.model(**kwargs)

        self.session.add(object_)
        if flush:
            self.session.flush()
        return object_

    def update(self, object_, **data):
        """
        Update object and return it
        :param object_: Object to be updated
        :param data: Model attributes and their values dictionary
        :return: Updated object
        """
        for attribute, value in data.items():
            if hasattr(object_, attribute):
                setattr(object_, attribute, value)
        self.session.add(object_)
        return object_

    def list(self, offset=0, limit=25, **criteria):
        """
        Get a list of all items of this model that are not deleted
        :param offset: rows to skip
        :param limit: results limit
        :param criteria: filter parameters
        :return: List of objects
        """
        query = self._find(**criteria)
        return query.limit(limit).offset(offset).all()

    def get(self, id_):
        """
        Fetch object form database based on its primary ID
        :param id_: Primary ID
        :return: Object or None
        """
        return self._query().filter(self.model.fc_id == id_).one_or_none()

    def find(self, **criteria):
        """
        Get a an item with criteria filtered
        :param criteria: Filter attributes
        :return: an object or None
        """
        query = self._find(**criteria)
        return query.one_or_none()

    def find_one(self, **criteria):
        """
        Get one item with the criteris filtered.

        :param criteria: Filter attributes
        :return: At most one object
        :raises MultipleResultsFound: if multiple results were found
        """
        return self._find(**criteria).one()

    def hard_delete(self, id_):
        """
        Permanently deletes from database
        :param id_:
        :return: None
        """
        # query here instead of private function as we want soft deleted
        # records to be deleted
        to_delete = self.session.query(self.model).get(id_)
        if to_delete:
            self.session.delete(to_delete)
            self.session.flush()

    def delete(self, id_):
        """
        Performs a soft delete on an object in the database by ID
        :param id_: Id of model object to be deleted
        :return: None
        """
        to_delete = self.get(id_)
        if to_delete:
            self.update(to_delete, deleted=datetime.now())

    def _find(self, order=None, **criteria):
        """
        Prepare a query with filter criteria
        :param offset: Int of items to skip
        :param limit: Int of items to return
        :param order: Order by attribute
        :param criteria: Filter attributes
        :return: Query
        """
        query = self._query()
        query = self._apply_filtering(query, **criteria)
        return self._order(query, order)

    def _apply_filtering(self, query, **criteria):
        """
        apply filter criteria
        :param criteria:
        :return:
        """
        for _filter, value in criteria.items():
            column = getattr(self.model, _filter, None)
            if column:
                if type(value) == list:
                    query = query.filter(or_(column == v for v in value))
                else:
                    query = query.filter(column == value)
        return query

    def _order(self, query, order):
        """
        Order query results
        :param order: string of order attributes separated by comma
        :return: ordered query string
        """
        if order:
            columns_to_order = self._apply_ordering(order.split(','))
            query = query.order_by(*columns_to_order)
        return query

    def _apply_ordering(self, ordering):
        """
        Logical ordering based on passed parameters
        :param ordering: List of strings to order by
        :return: Query ordering
        """
        order_list = []
        for order_value in ordering:
            column = order_value.replace('-', '')
            if not hasattr(self.model, column):
                continue
            column = getattr(self.model, column)
            if order_value.startswith('-'):
                order_list.append(desc(column))
            else:
                order_list.append(asc(column))
        return order_list

    def _query(self):
        """
        Basic function that prepares a query to exclude deleted objects
        :return: Query
        """
        query = self.session.query(self.model)
        if hasattr(self.model, 'deleted'):
            query = query.filter(self.model.deleted.is_(None))
        if hasattr(self.model, 'active'):
            query = query.filter(self.model.active.is_(True))

        return query
