

class DbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'user':
            return 'user'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'user':
            return 'user'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return self.db_for_read(obj1) == self.db_for_read(obj2)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'user':
            return db == 'user'
        return db == 'default'