# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
############# datos para openshift ###########
#  Root User: adminYbTrJ2d
#   Root Password: d6JeR2X9_Jsu
#   Database Name: web2py
# Connection URL: mysql://$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
#    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
	db = DAL('mysql://root:www4214@localhost/dbpylab')
#	db = DAL('mysql://adminYbTrJ2d:d6JeR2X9_Jsu@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')    
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login


db.define_table('cf_empresa',
    Field('id','integer'),
    Field('nombre','string', label=T('Nombre')),
    Field('razon_social','string', label=T('Razon Social')),
    Field('direccion','text', label=T('Direccion')),
    Field('rif','string', label=T('Rif')),
    Field('nit','string', label=T('Nit')),
    Field('email','string', label=T('Email')),
    Field('tlf','string', label=T('Tlf')),
    Field('fax','string', label=T('Fax')),
    Field('master','boolean', label=T('Empresa Maestra'), default='0'),
    Field('ruta_foto','upload',autodelete=True, label=T('Imagen'))
    )

#----------------------------------------------------
db.define_table('cf_parametro',
    Field('id','integer'),
    Field('parametro','string', label=T('Parametro')),
    Field('valor','string', label=T('Valor'))
    )

#----------------------------------------------------

db.define_table('cf_proveedor',
    Field('id','integer'),
    Field('nombre','string', label=T('Nombre')),
    Field('razon_social','string', label=T('Razon Social')),
    Field('direccion','text', label=T('Direccion')),
    Field('rif','string', label=T('R.I.F')),
    Field('nit','string', label=T('N.I.T')),
    Field('email','string', label=T('E-Mail')),
    Field('tlf','string', label=T('Tlf.')),
    Field('fax','string', label=T('Fax.')),
    Field('ruta_foto','upload',autodelete=True, label=T('Imagen')),format='%(razon_social)s'
	)

db.define_table('cf_cliente',
    Field('id','integer'),
    Field('nombre','string', label=T('Nombre')),
    Field('razon_social','string', label=T('Razon Social')),
    Field('direccion','text', label=T('Direccion')),
    Field('rif','string', label=T('R.I.F')),
    Field('nit','string', label=T('N.I.T')),
    Field('email','string', label=T('E-Mail')),
    Field('tlf','string', label=T('Tlf.')),
    Field('fax','string', label=T('Fax.')),
	Field('juridico','boolean', label=T('Es Juridico')),
	Field('empresa_id','integer', label=T('Empresa'), requires=IS_IN_DB(db, db.cf_empresa, '%(razon_social)s' )),
	Field('ruta_foto','upload',autodelete=True, label=T('Imagen')),format='%(razon_social)s'
	)
#aqui podemos guardas los examenes genereales y los perfiles
#examen_id es recursicvo sobre esta misma tabla para configurar perfiles que contienen
#o bien examenes (con sus determinaciones) o determinacione por separado
db.define_table('cf_examen',
	Field('id','integer'),
	Field('codigo','string', label=T('Codigo')),
    Field('nombre','string', label=T('Nombre')),
    Field('precio_fin','float',  label=T('Precio Final'), default=0),  
	Field('precio_emp','float',  label=T('Precio Empr.'), default=0),  
	Field('precio_seg','float',  label=T('Precio Seguro'), default=0),  
	Field('precio_esp1','float',  label=T('Precio Espec1'), default=0),  
	Field('precio_esp2','float',  label=T('Precio Espec2'), default=0),
	Field('examen_id','integer', label=T('Examen')), #campo recursivo para crear perfiles
	Field('es_perfil','boolean', label=T('Examen'),default='0'),
	Field('ruta_foto','upload',autodelete=True, label=T('Imagen')),format='%(nombre)s'
	)

#
db.define_table('cf_examen_det',
	Field('id','integer'),
	Field('codigo','string', label=T('Codigo')),
    Field('nombre','string', label=T('Nombre')),
	Field('examen_id','integer', label=T('Examen')),		
	Field('examen_tip_id','integer', label=T('Grupo')),		
	Field('ruta_foto','upload',autodelete=True, label=T('Imagen')),format='%(nombre)s'
	)

# TIpo de determinaciones, para subagrupar determinaciones Quimica Sanguinea, Hematologia, Serologia, Microbiolgia,e tc.
db.define_table('cf_examen_tip',
	Field('id','integer'),
	Field('codigo','string', label=T('Codigo')),
    Field('nombre','string', label=T('Nombre')),format='%(codigo)s - %(nombre)s'
)

#Valores normales, seguns rangos de edad y sexo
db.define_table('cf_examen_val',
	Field('id','integer'),
	Field('examen_det_id','integer'),
	Field('einferior','string', label=T('Edad piso')),
    Field('esuperior','string', label=T('Edad tope')),
    Field('linferior','string', label=T('Limite Inferior')),
    Field('lsuperior','string', label=T('Limite Superior')),
    Field('sexo','string', label=T('Sexo')),    
	Field('unidad','string', label=T('Unidad')),
)

db.define_table('fc_orden',
	Field('id','integer'),
	Field('numero','string', label=T('Numero')),
	Field('fecha','date', label=T('Fecha'), default=request.now.date()),	
	Field('cliente_id','integer', label=T('Cliente'),requires=IS_IN_DB(db, db.cf_cliente, '%(codigo)s - %(nombre)s')),  	
	Field('procesada','boolean', label=T('Esta procesada'), default='0'),
	Field('facturada','boolean', label=T('Facturada'), default='0'),
	Field('entregada','boolean', label=T('Ha sido entregada'), default='0'),
	Field('pagada','boolean', label=T('Pagada'), default='0'),	
	Field('fecha_pag','date', label=T('Fecha Pago')),	
	Field('num_fact','string', label=T('Numero Factura')),
	Field('fecha_fac','date', label=T('Fecha Factura')),	
	format='%(numero)s'
	)

db.fc_orden.numero.requires=IS_NOT_IN_DB(db, db.fc_orden.numero)
db.fc_orden.num_fact.requires=IS_NOT_IN_DB(db, db.fc_orden.num_fact)

db.define_table('fc_orden_det',
	Field('id','integer'),
	Field('orden_id','integer', label=T('Nro Orden')),	
	Field('examen_id','integer', label=T('Examen'), requires=IS_IN_DB(db, db.cf_examen, '%(codigo)s - %(nombre)s')),
	Field('cantidad','integer', label=T('Cantidad')),	
	Field('importe','float',  label=T('Importe')),  
	Field('iva','float',  label=T('I.V.A'), default=0),  
	Field('imp1','float',  label=T('Impuesto 1'), default=0),  
	Field('imp2','float',  label=T('Impuesto 2'), default=0),  
	Field('descuento','float', label=T('Descuento'), default=0),
	Field('total','float', label=T('Total')),	
	)

db.fc_orden_det.orden_id.requires=IS_IN_DB(db, db.fc_orden.id)


db.define_table('op_result',
	Field('id','integer'),
	Field('orden_id','integer', label=T('IdOrden') , requires=IS_IN_DB(db, db.fc_orden, '%(numero)s')),	
	Field('fecha_res','date', label=T('Fecha Resultado')),	
	Field('observaciones','string', label=T('Observaciones'))
	)


db.define_table('op_result_det',
	Field('id','integer'),
	Field('result_id','integer', label=T('IdResultado')),	
	Field('examen_det_id','integer', label=T('Examen'), requires=IS_IN_DB(db, db.cf_examen_det, '%(codigo)s - %(nombre)s')),
	Field('resultado','string', label=T('Resultado')),
	Field('observaciones','string', label=T('Observaciones'))
	)

db.op_result_det.result_id.requires=IS_IN_DB(db, db.op_result.id)

