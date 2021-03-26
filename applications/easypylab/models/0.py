from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'EasyPyLab'
settings.subtitle = 'Una sencilla aplicacion para el manejo de laboratorios clinicos'
settings.author = 'Wuelfhis Asuaje'
settings.author_email = 'wasuaje@hotmail.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Balanced'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '11de6e28-94cb-482a-9613-6685e69620a6'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = ['attachments', 'datatable', 'dropdown', 'mmodal', 'jqgrid', 'multiselect', 'sortable']
