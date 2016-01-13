import abc

class Entity:
    __metaclass__ = abc.ABCMeta

    primary_key = ''
    foreign_references = []
    order_clause = 'id'

    def __init__(self):
        self.duplicates = []
        self.duplicate_root = None
        self.merge_statements = []

    @classmethod
    def split_column_name(self, col_name):
        """a.b.c  -->  a.b, c"""
        return tuple(col_name.rsplit('.', 1))

    @classmethod
    def get_all(self, cursor):
        table_name, attribute = self.split_column_name(self.primary_key)
        cursor.execute('SELECT * FROM %s ORDER BY %s' % (table_name, self.order_clause))
        output = []
        for row in cursor.fetchall():
            output.append(self(*row))
        return output

    def stop_iteration(self, other_entity):
        return False

    def is_duplicate(self):
        return self.duplicate_root is not None

    def append_merge_statements(self, old_id):
        for reference in self.foreign_references:
            table_name, attribute = self.split_column_name(reference)
            self.merge_statements.append('UPDATE %s SET %s = %i WHERE %s = %i' % (table_name, attribute, self.id, attribute, old_id))
        table_name, attribute = self.split_column_name(self.primary_key)
        self.merge_statements.append('DELETE FROM %s WHERE %s = %i' % (table_name, attribute, old_id))

    def get_class_statements(self):
        return []

    @abc.abstractmethod
    def equal(self, other_entity):
        return

    @abc.abstractmethod
    def merge(self, other_entity):
        return

    @abc.abstractmethod
    def get_update_statements(self):
        return
