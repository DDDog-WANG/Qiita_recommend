# class DBRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'default':
#             return 'default'
#         if model._meta.app_label == 'mysql':
#             return 'mysql'
#         return None

#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'sqlite_app':
#             return 'default'
#         if model._meta.app_label == 'mysql_app':
#             raise Exception('mysql_db is not writable!')  # 書き込み禁止
#         return None

#     def allow_relation(self, obj1, obj2, **hints):
#         return True

#     def allow_migrate(self, db, app_label, model=None, **hints):
#         if app_label == 'auth' or app_label == 'contenttypes' or app_label == 'sessions' or app_label == 'admin':
#             return db == 'default'
#         if app_label == 'sqlite_app':
#             return db == 'default'
#         if app_label == 'mysql_app':
#             return db == 'mysql_db'
#         return None