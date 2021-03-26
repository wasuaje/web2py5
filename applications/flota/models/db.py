# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('google:datastore')              # connect to Google BigTable
                                              # optional DAL('gae://namespace')
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    #db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
    db = DAL('mysql://root:www4214@localhost/dbflota')
    #legacy_db = DAL('mysql://root:www4214@localhost/dbflota')
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Mail, Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key()) 
crud, service, plugins = Crud(db), Service(), PluginManager()

auth.settings.create_user_groups = False
auth.settings.registration_requires_approval = True
auth.settings.table_user_name = 'authuser'
auth.settings.table_group_name = 'authgroup'
auth.settings.table_membership_name = 'authmembership'
auth.settings.table_permission_name = 'authpermission'
auth.settings.table_event_name = 'authevent'
auth.settings.table_cas_name = 'authcas'

#print db._lastsql


from gluon.contrib.pyfpdf import FPDF, HTMLMixin

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled = \
#    ['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = auth        # =auth to enforce authorization on crud

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

## configure email
mail=auth.settings.mailer
#mail.settings.server = 'logging' or 'smtp.gmail.com:587'
#mail.settings.sender = 'wasuaje@gmail.com'
#mail.settings.login = 'wasuaje@gmail.com:www4214'

mail.settings.server = 'localhost:25'
mail.settings.sender = 'wasuaje@gmail.com'
mail.settings.tls = False
mail.settings.login = None

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

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

#mail.settings.server = settings.email_server
#mail.settings.sender = settings.email_sender
#mail.settings.login = settings.email_login	


## create all tables needed by auth if not custom tables

########################################
#incluye el webgrid para usarlo globalmente
webgrid = local_import('webgrid')

	
response.files.append(URL(r=request,c='static/jquery-autocomplete',f='jquery.autocomplete.js'))
response.files.append(URL(r=request,c='static/jquery-autocomplete',f='jquery.autocomplete.css'))

#campo
#id_field
#show_fields

def au__tocomplete_widget(f,id_field,show_fields):
    import uuid
    d_id = "autocomplete-" + str(uuid.uuid4())[:8]
    wrapper = DIV(_id=d_id)
    inp = SQLFORM.widgets.string.widget(f,None)
    print f,type(f)
    print inp
    rows = f._db(f._table['id']>0).select(f._table.ALL,distinct=True)
    print rows	
    itms = [str(t[f.name]) for t in rows]
    scr = SCRIPT('var data= "%s".split("|");jQuery("#%s input").autocomplete(data);' % \
                 ("|".join(itms),d_id))
    print scr
    wrapper.append(inp)
    wrapper.append(scr)
    print dir(wrapper)
    print wrapper
    return wrapper


def attrs(**kwds):
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f
    return decorate

@attrs(id_field="db.mt_persona.id",show_fields="cedula,nombres")
def autocomplete_widget(f,v):
    import uuid
    print "asdasdasd"
    d_id = "autocomplete-" + str(uuid.uuid4())[:8]
    wrapper = DIV(_id=d_id)
    inp = SQLFORM.widgets.string.widget(f,v)
    rows = f._db(f._table['id']>0).select(f,distinct=True)
    itms = [str(t[f.name]) for t in rows]
    scr = SCRIPT('var data= "%s".split("|");jQuery("#%s input").autocomplete(data);' % ("|".join(itms),d_id))
    wrapper.append(inp)
    wrapper.append(scr)
    print f,type(f)
    print inp
    print rows	
    print scr
    print type(wrapper)
    print wrapper
#    print id_field,show_fields
    return wrapper

class CascadingSelect(object):
	def __init__(self, *tables):
		self.tables = tables 
		self.prompt = lambda table:str(table)   
	def widget(self,f,v):
		import uuid
		next = 0		
		uid = str(uuid.uuid4())[:8]
		d_id = "cascade-" + uid
		wrapper = TABLE(_id=d_id)
		parent = None; parent_format = None; 
		fn =  '' 
		vr = 'var dd%s = [];var oi%s = [];\n' % (uid,uid)
		prompt = [self.prompt(table) for table in self.tables]
		vr += 'var pr%s = ["' % uid + '","'.join([str(p) for p in prompt]) + '"];\n' 
		f_inp = SQLFORM.widgets.string.widget(f,v)
		f_id = f_inp['_id']
		f_inp['_type'] = "hidden"
		for tc, table in enumerate(self.tables):             						
			db = table._db   
			format = table._format           			
			options = db(table['id']>0).select()					
			id = str(table) + '_' + format[2:-2]             						
			#print db["mt_ciudad"]._tablename
			#if "mt_ciudad" in db[table]._tablename :
			#	print "pasa", table.mt_estado_id
			#print type(parent), type(parent_format)
#  		for opt in options:
#				#print format % opt,  opt.id
#				print opt.keys()
#				if parent:
#					parent=opt[str(parent)]
#					print 'parent', parent
#				else:
#					parent=0
#					print 'parent',parent
				
				#registro=db.mv_entrevista(request.args(0))		
				#para mantener entre pantallas la pregunta activa	
				#session.id_preg=registro['id']
			# la tabla menos especifica para obtener id
			if next>0:
				idfield=self.tables[int(next)-1]._tablename+"_id"
				#print idfield
			opts = [OPTION(format % opt,_value=opt.id, _parent=opt[idfield] if parent else '0')  for opt in options]		
			opts.insert(0, OPTION(prompt[tc],_value=0))			
			inp = SELECT(opts , _id=id,_name=id, _disabled="disabled" if parent else None)			
			wrapper.append(TR(inp))
			next = str(tc + 1)
			vr += 'var p%s = jQuery("#%s #%s"); dd%s.push(p%s);\n' % (tc,d_id,id,uid,tc)            
			vr += 'var i%s = jQuery("option",p%s).clone(); oi%s.push(i%s);\n' % (tc,tc,uid,tc)
			fn_in = 'for (i=%s;i<%s;i+=1){dd%s[i].find("option").remove();'\
					'dd%s[i].append(\'<option value="0">\' + pr%s[i] + \'</option>\');'\
					'dd%s[i].attr("disabled","disabled");}\n' % \
							(next,len(self.tables),uid,uid,uid,uid)
			fn_in +='oi%s[%s].each(function(i){'\
					'if (jQuery(this).attr("parent") == dd%s[%s].val()){'\
					'dd%s[%s].append(this);}});' % (uid,next,uid,tc,uid,next)            
			fn_in += 'dd%s[%s].removeAttr("disabled");\n' % (uid,next)
			fn_in += 'jQuery("#%s").val("");' % f_id
			if (tc < len(self.tables)-1):
				fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in) 
			else:
				fn_in = 'jQuery("#%s").val(jQuery(this).val());' % f_id
				fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in)
				if v:
					fn += 'dd%s[%s].val(%s);' % (uid,tc,v)                       
			parent = table
			parent_format = format[2:-2]					
		wrapper.append(f_inp)
		wrapper.append(SCRIPT(vr,fn))
		return wrapper


db.define_table('authuser',
    Field('email', type='string',
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('username', type='string',
          label=T('Username')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    format='%(username)s',
    migrate=False)

#--------

db.authuser.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.authuser.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.authuser.password.requires = CRYPT(key=auth.settings.hmac_key)
db.authuser.username.requires = IS_NOT_IN_DB(db, db.authuser.username)
db.authuser.registration_id.requires = IS_NOT_IN_DB(db, db.authuser.registration_id)
db.authuser.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.authuser.email))

auth.define_tables(migrate = False) 


db.define_table('cf_asignacion_tipo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('cf_cargo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)
#--------
db.define_table('cf_viaje_tipo',
	Field('id','integer'),
	Field('nombre','string'),
	Field('solo_ida','integer', requires=IS_IN_SET([0, 1,])),
	migrate=False)
#--------
db.define_table('cf_empresa',
    Field('id','integer'),
    Field('nombre','string'),
    Field('razon_social','string'),
    Field('direccion','string'),
    Field('rif','string'),
    Field('nit','string'),
    Field('email','string'),
    Field('tlf','string'),
    Field('fax','string'),
    Field('ruta_foto','upload',autodelete=True),
    migrate=False)

#--------
db.define_table('cf_proveedor',
    Field('id','integer'),
    Field('nombre','string'),
    Field('razon_social','string'),
    Field('direccion','string'),
    Field('rif','string'),
    Field('nit','string'),
    Field('email','string'),
    Field('tlf','string'),
    Field('fax','string'),
    Field('ruta_foto','upload',autodelete=True),format='%(nombre)s', 
    migrate=False)

#--------
db.define_table('cf_item_grupo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('cf_item',
    Field('id','integer'),
    Field('nombre','string'),
    Field('cf_item_grupo_id',db.cf_item_grupo),
    migrate=False)
db.cf_item.cf_item_grupo_id.requires = IS_IN_DB(db,db.cf_item_grupo.id,'%(nombre)s')    

#--------
db.define_table('cf_aviso',
    Field('id','integer'),
    Field('mensaje','string'),
    Field('kilometraje','integer'),
    Field('dias','integer'),
    Field('cf_item_id','integer'),
    migrate=False)
db.cf_aviso.cf_item_id.requires = IS_IN_DB(db,db.cf_item.id,'%(nombre)s')    


#--------
db.define_table('cf_localidad',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('cf_solicitud_tipo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('cf_tipo_combustible',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('cf_tipo_doc',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('cf_vehiculo_marca',
    Field('id','integer'),
    Field('nombre','string'),format='%(nombre)s',
    migrate=False)

#--------
db.define_table('cf_vehiculo_modelo',
	Field('id','integer'),    
	Field('cf_vehiculo_marca_id',db.cf_vehiculo_marca),
	Field('nombre','string'),format='%(nombre)s', 
	migrate=False)

db.cf_vehiculo_modelo.cf_vehiculo_marca_id.requires = IS_IN_DB(db,db.cf_vehiculo_marca.id,'%(nombre)s')
db.cf_vehiculo_modelo.cf_vehiculo_marca_id.represent=lambda val: db.cf_vehiculo_marca[val].nombre
#--------
db.define_table('cf_vehiculo_tipo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
db.define_table('mt_persona',
	Field('id','integer'),
	Field('cedula','string',unique=True),
	Field('nombres','string'),
	Field('apellidos','string'),
	Field('ruta_foto','upload',autodelete=True),
	Field('sexo','string',requires=IS_IN_SET(['M', 'F', 'O'])),
	Field('user','string'),
	Field('password','password'),
	Field('cf_cargo_id','integer'),
	Field('tlf_hab','string'),
	Field('tlf_cel','string'),
	Field('direccion','string'),
	Field('email','string'),	
	migrate=False)
db.mt_persona.cf_cargo_id.requires = IS_IN_DB(db,db.cf_cargo.id,'%(nombre)s')
db.mt_persona.cedula.requires = IS_NOT_IN_DB(db,db.mt_persona.cedula)
db.mt_persona.cf_cargo_id.represent=lambda val: db.cf_cargo[val].nombre

#--------
   
##falta tabla veh_fotos muchos a muchos

#--------
db.define_table('mt_doc_persona',
    Field('id','integer'),
    Field('fecha_emision','date'),
    Field('fecha_vencimiento','date'),
    Field('numero','string'),
    Field('cf_tipo_doc_id','integer'),
    Field('mt_persona_id','integer'),
    migrate=False)
db.mt_doc_persona.mt_persona_id.requires = IS_IN_DB(db,db.mt_persona.id,'%(cedula)s  | %(nombres)s %(apellidos)s ')
db.mt_doc_persona.cf_tipo_doc_id.requires = IS_IN_DB(db,db.cf_tipo_doc.id,'%(nombre)s')    

#--------
db.define_table('mt_estado',
    Field('id','integer'),
    Field('codigo','string'),
    Field('nombre','string'), format='%(nombre)s', 
    migrate=False)

#--------
db.define_table('mt_ciudad',
    Field('id','integer'),
    Field('codigo','string'),
    Field('nombre','string'),
    Field('mt_estado_id','integer'), format='%(nombre)s', 
    migrate=False)
db.mt_ciudad.mt_estado_id.requires = IS_IN_DB(db,db.mt_estado.id,'%(nombre)s')
db.mt_ciudad.mt_estado_id.represent=lambda val: db.mt_estado[val].nombre


#--------
db.define_table('mt_vehiculo',
    Field('id','integer'),
    Field('placa','string'),
    Field('color','string'),
    Field('serial_motor','string'),
    Field('serial_caja','string'),
    Field('serial_carroceria','string'),
    Field('nro_ejes','integer'),
    Field('nro_ruedas','integer'),
    Field('kilometraje','integer'),
    Field('ruta_foto','upload',autodelete=True),
    Field('cf_vehiculo_tipo_id','integer'),
    Field('cf_tipo_combustible_id','integer'),
	Field('cf_vehiculo_modelo_id',db.cf_vehiculo_modelo),
    migrate=False)

db.mt_vehiculo.cf_vehiculo_tipo_id.requires = IS_IN_DB(db,db.cf_vehiculo_tipo.id,'%(nombre)s')
db.mt_vehiculo.cf_tipo_combustible_id.requires = IS_IN_DB(db,db.cf_tipo_combustible.id,'%(nombre)s')
db.mt_vehiculo.placa.requires = IS_NOT_IN_DB(db,db.mt_vehiculo.placa)
db.mt_vehiculo.serial_motor.requires = IS_NOT_IN_DB(db,db.mt_vehiculo.serial_motor)
db.mt_vehiculo.serial_caja.requires = IS_NOT_IN_DB(db,db.mt_vehiculo.serial_caja)
db.mt_vehiculo.serial_carroceria.requires = IS_NOT_IN_DB(db,db.mt_vehiculo.serial_carroceria)
db.mt_vehiculo.cf_vehiculo_modelo_id.requires = IS_IN_DB(db,db.cf_vehiculo_modelo.id,'%(nombre)s')
db.mt_vehiculo.cf_vehiculo_modelo_id.represent=lambda val: db.cf_vehiculo_modelo[val].nombre
cascade = CascadingSelect(db.cf_vehiculo_marca, db.cf_vehiculo_modelo)
cascade.prompt = lambda table: "-- Seleccione --"  
#+ ("un " if str(table)[3] in 'aeiou' else "una ") + str(table)
db.mt_vehiculo.cf_vehiculo_modelo_id.widget = cascade.widget

#--------
db.define_table('mt_doc_vehiculo',
    Field('id','integer'),
    Field('fecha_emision','date'),
    Field('fecha_vencimiento','date'),
    Field('numero','string'),
    Field('cf_tipo_doc_id','integer'),
    Field('mt_vehiculo_id','integer'),
    migrate=False)
db.mt_doc_vehiculo.mt_vehiculo_id.requires = IS_IN_DB(db,db.mt_vehiculo.id,'%(placa)s')
db.mt_doc_vehiculo.cf_tipo_doc_id.requires = IS_IN_DB(db,db.cf_tipo_doc.id,'%(nombre)s')    


#--------
db.define_table('mt_kilometraje',
    Field('id','integer'),
    Field('fecha','date'),
    Field('kilometraje','integer'),
    Field('mt_vehiculo_id','integer'),
    migrate=False)	
db.mt_kilometraje.mt_vehiculo_id.represent=lambda val: db.mt_vehiculo[val].placa
db.mt_kilometraje.mt_vehiculo_id.widget = SQLFORM.widgets.autocomplete(request, db.mt_vehiculo.placa,  min_length=3,  id_field=db.mt_vehiculo.id) 

#--------
db.define_table('mv_viaje',
	Field('id','integer'),
	Field('descripcion','string'),
	Field('fecha_solicitud','date'),
	Field('fecha_inicio','date'),
	Field('fecha_fin','date'),
	Field('nro_pasajeros','integer'),
	Field('horas_espera','integer'),
	Field('status','integer'),
	Field('mt_ciudad_desde','integer'),
	Field('mt_ciudad_hasta','integer'),
	Field('cf_proveedor_id','integer'),
	Field('cf_vehiculo_tipo_id','integer'),
	Field('cf_viaje_tipo_id','integer'),
	migrate=False)

db.mv_viaje.cf_proveedor_id.requires = IS_IN_DB(db,db.cf_proveedor.id,'%(razon_social)s')
db.mv_viaje.cf_vehiculo_tipo_id.requires = IS_IN_DB(db,db.cf_vehiculo_tipo.id,'%(nombre)s')
db.mv_viaje.cf_viaje_tipo_id.requires = IS_IN_DB(db,db.cf_viaje_tipo.id,'%(nombre)s')
db.mv_viaje.mt_ciudad_desde.represent=lambda val: db.mt_ciudad[val].nombre
db.mv_viaje.mt_ciudad_hasta.represent=lambda val: db.mt_ciudad[val].nombre
db.mv_viaje.cf_proveedor_id.represent=lambda val: db.cf_proveedor[val].razon_social
db.mv_viaje.cf_vehiculo_tipo_id.represent=lambda val: db.cf_vehiculo_tipo[val].nombre
db.mv_viaje.cf_viaje_tipo_id.represent=lambda val: db.cf_viaje_tipo[val].nombre

cascade = CascadingSelect(db.mt_estado, db.mt_ciudad)
cascade.prompt = lambda table: "-- Seleccione --"  
#+ ("un " if str(table)[3] in 'aeiou' else "una ") + str(table)
db.mv_viaje.mt_ciudad_desde.widget = cascade.widget

cascade2 = CascadingSelect(db.mt_estado, db.mt_ciudad)
cascade2.prompt = lambda table: "-- Seleccione --"  
#+ ("un " if str(table)[3] in 'aeiou' else "una ") + str(table)
db.mv_viaje.mt_ciudad_hasta.widget = cascade2.widget


#--------
db.define_table('mv_solicitud',
    Field('id','integer'),
    Field('descripcion','string'),
    Field('fecha_solicitud','date'),
    Field('fecha_inicio','date'),
    Field('fecha_fin','date'),
    Field('status','integer'),
    Field('cf_solicitud_tipo_id','integer'),
    Field('mt_persona_id','integer'),
    migrate=False)
db.mv_solicitud.cf_solicitud_tipo_id.requires = IS_IN_DB(db,db.cf_solicitud_tipo.id,'%(nombre)s')
#db.mv_solicitud.mt_persona_id.widget = SQLFORM.widgets.autocomplete(request, db.mt_persona.apellidos,  min_length=4,  id_field=db.mt_persona.id) 
#db.mv_solicitud.mt_persona_id.widget=autocomplete_widget(db.mv_solicitud.mt_persona_id,db.mt_persona.id,["cedula","nombres","apellidos"])
db.mv_solicitud.mt_persona_id.widget=autocomplete_widget
db.mv_solicitud.mt_persona_id.represent=lambda val: db.mt_persona[val].nombres+', '+db.mt_persona[val].apellidos
db.mv_solicitud.cf_solicitud_tipo_id.represent=lambda val: db.cf_solicitud_tipo[val].nombre

#--------
db.define_table('mv_asignacion',
	Field('id','integer'),
	Field('descripcion','string'),
	Field('fecha_proceso','date'),    
	Field('status','integer'),
	Field('mt_vehiculo_id','integer'),
	Field('mt_persona_id','integer'),
	Field('mv_viaje_id','integer'),
	migrate=False)
db.mv_asignacion.mt_persona_id.widget = SQLFORM.widgets.autocomplete(request, db.mt_persona.apellidos,  min_length=4,  id_field=db.mt_persona.id) 
db.mv_asignacion.mv_viaje_id.widget = SQLFORM.widgets.autocomplete(request, db.mv_viaje.id,  min_length=1,  id_field=db.mv_viaje.id) 
db.mv_asignacion.mt_vehiculo_id.widget = SQLFORM.widgets.autocomplete(request, db.mt_vehiculo.placa,  min_length=3,  id_field=db.mt_vehiculo.id) 
db.mv_asignacion.mt_persona_id.represent=lambda val: db.mt_persona[val].nombres+', '+db.mt_persona[val].apellidos
db.mv_asignacion.mt_vehiculo_id.represent=lambda val: db.mt_vehiculo[val].placa
db.mv_asignacion.mv_viaje_id.represent=lambda val: db.mv_viaje[val].descripcion

#--------
db.define_table('mv_gasto',
	Field('id','integer'),
	Field('descripcion','string'),
	Field('fecha_registro','date'),
	Field('fecha_gasto','date'),
	Field('kilometraje','integer'),
	Field('mv_asignacion_id','integer'),
	Field('impuesto','double'),
	Field('descuento','double'),
	Field('recargo','double'),
	Field('subtotal','double'),
	Field('referencia','string'),
	Field('cf_proveedor_id','integer', db.cf_proveedor.nombre),  
    migrate=False)
#db.mv_gasto.cf_proveedor_id.requires = IS_IN_DB(db,db.cf_proveedor.id,'%(nombre)s')
db.mv_gasto.cf_proveedor_id.represent=lambda val: db.cf_proveedor[val].nombre
db.mv_gasto.mv_asignacion_id.represent=lambda val: db.mv_asignacion[val].descripcion
db.mv_gasto.mv_asignacion_id.widget = SQLFORM.widgets.autocomplete(request, db.mv_asignacion.descripcion,  min_length=4,  id_field=db.mv_asignacion.id) 
db.mv_gasto.cf_proveedor_id.widget = SQLFORM.widgets.autocomplete(request, db.cf_proveedor.nombre,  min_length=4,  id_field=db.cf_proveedor.id) 

#--------
db.define_table('mv_gasto_det',
    Field('id','integer'),
    Field('cantidad','double'),
    Field('unitario','double'),
    Field('total','double',compute=lambda r: r['unitario']*r['cantidad'] ) ,    
    Field('mv_gasto_id','integer'),
    Field('cf_item_id','integer'),
    migrate=False)
#db.mv_gasto_det.mv_gasto_id.requires = IS_IN_DB(db,db.mv_gasto.id)
db.mv_gasto_det.cf_item_id.requires = IS_IN_DB(db,db.cf_item.id,'%(nombre)s')
db.mv_gasto_det.cf_item_id.represent=lambda val: db.cf_item[val].nombre

#--------
db.define_table('fc_tipo_doc',
	Field('id','integer'),
	Field('naturaleza','string',  requires=IS_IN_SET(['+', '-',''])),
	Field('correlativo','integer'),
	Field('nombre','string'),format='%(nombre)s',
	migrate=False)
#--------
db.define_table('fc_banco',
    Field('id','integer'),	
    Field('nombre','string'),format='%(nombre)s',
    migrate=False)
#--------
db.define_table('fc_forma_pago',
    Field('id','integer'),	
    Field('nombre','string'),format='%(nombre)s',
    migrate=False)
#--------
db.define_table('fc_documento',
	Field('id','integer'),
	Field('correlativo','integer'),
	Field('fecha','date'),
	Field('fecha_vencimiento','date'),
	Field('contacto','string'),
	Field('nota_superior','string'),
	Field('nota_detalle','string'),
	Field('referencia','string'),	#referencia a facturas o presupuestos o notas de la misma tables
	Field('status','integer'),
	Field('fc_tipo_doc_id','integer'),
	Field('cf_proveedor_id','integer'),
	migrate=False)

db.fc_documento.cf_proveedor_id.requires = IS_IN_DB(db,db.cf_proveedor.id,'%(razon_social)s')
db.fc_documento.fc_tipo_doc_id.requires = IS_IN_DB(db,db.fc_tipo_doc.id,'%(nombre)s')
db.fc_documento.cf_proveedor_id.represent=lambda val: db.cf_proveedor[val].razon_social
db.fc_documento.fc_tipo_doc_id.represent=lambda val: db.fc_tipo_doc[val].nombre

db.define_table('fc_documento_det',
	Field('id','integer'),
	Field('descripcion','string'),
	Field('cantidad','float'),
	Field('importe','float'),
	Field('descuento','float'),
	Field('recargo','float'),
	Field('total','float'),
	Field('nota','string'),	#referencia a facturas o presupuestos o notas de la misma tables
	Field('fc_documento_id','integer'),
	Field('fc_servicio_id','integer'),
	migrate=False)

db.define_table('fc_servicio',
	Field('id','integer'),
	Field('codigo','string'),
	Field('descripcion','string'),
	Field('tarifa_cobro','float'),
	Field('tarifa_chofer','float'),
	Field('porcentaje','float'),
	Field('porcentaje_chofer','float'),
	Field('distancia','integer'),
	Field('mt_ciudad_desde','integer'),
	Field('mt_ciudad_hasta','integer'),
	Field('cf_vehiculo_tipo_id','integer'),
	Field('is_viaje','integer',  requires=IS_IN_SET([1,0])),
	migrate=False)

db.fc_servicio.cf_vehiculo_tipo_id.requires = IS_IN_DB(db,db.cf_vehiculo_tipo.id,'%(nombre)s')
db.fc_servicio.cf_vehiculo_tipo_id.represent=lambda val: db.cf_vehiculo_tipo[val].nombre
db.fc_servicio.mt_ciudad_desde.represent=lambda val: db.mt_ciudad[val].nombre
db.fc_servicio.mt_ciudad_hasta.represent=lambda val: db.mt_ciudad[val].nombre
cascade = CascadingSelect(db.mt_estado, db.mt_ciudad)
cascade.prompt = lambda table: "-- Seleccione --"  
#+ ("un " if str(table)[3] in 'aeiou' else "una ") + str(table)
db.fc_servicio.mt_ciudad_desde.widget = cascade.widget

cascade2 = CascadingSelect(db.mt_estado, db.mt_ciudad)
cascade2.prompt = lambda table: "-- Seleccione --"  
#+ ("un " if str(table)[3] in 'aeiou' else "una ") + str(table)
db.fc_servicio.mt_ciudad_hasta.widget = cascade2.widget

#--------
db.define_table('fc_cobro',
	Field('id','integer'),
	Field('fecha','date'),
	Field('total','double'),
	Field('descripcion','string'),	
	Field('cf_proveedor_id','integer'),
	migrate=False)

db.fc_cobro.cf_proveedor_id.requires = IS_IN_DB(db,db.cf_proveedor.id,'%(razon_social)s')
db.fc_cobro.cf_proveedor_id.represent=lambda val: db.cf_proveedor[val].razon_social

#--------
db.define_table('fc_cobro_det',
	Field('id','integer'),
	Field('fecha','date'),
	Field('referencia','string'),	
	Field('monto','float'),
	Field('descripcion','string'),	
	Field('fc_cobro_id','integer'),
	Field('fc_forma_pago_id','integer'),
	Field('fc_banco_id','integer'),
	Field('fc_documento_id','integer'),
	Field('status','integer'),
	migrate=False)

db.fc_cobro_det.fc_forma_pago_id.requires = IS_IN_DB(db,db.fc_forma_pago.id,'%(nombre)s')
db.fc_cobro_det.fc_banco_id.requires = IS_IN_DB(db,db.fc_banco.id,'%(nombre)s')
db.fc_cobro_det.fc_documento_id.requires = IS_IN_DB(db,db.fc_documento.id,'%(correlativo)s')
db.fc_cobro_det.fc_documento_id.widget = SQLFORM.widgets.autocomplete(request, db.fc_documento.correlativo,  min_length=2,  id_field=db.fc_documento.id) 
db.fc_cobro_det.fc_documento_id.represent=lambda val: db.fc_documento[val].correlativo

#--------
db.define_table('fc_pago',
	Field('id','integer'),
	Field('fecha','date'),
	Field('total','double'),
	Field('descripcion','string'),	
	Field('mt_persona_id','integer'),
	migrate=False)

db.fc_pago.mt_persona_id.requires = IS_IN_DB(db,db.mt_persona.id,'%(nombres)s %(apellidos)s' )
db.fc_pago.mt_persona_id.represent=lambda val: db.mt_persona[val].nombres

#--------
db.define_table('fc_pago_det',
	Field('id','integer'),
	Field('fecha','date'),
	Field('referencia','string'),	
	Field('monto','double'),
	Field('descripcion','string'),	
	Field('fc_pago_id','integer'),
	Field('fc_forma_pago_id','integer'),
	Field('fc_banco_id','integer'),		
	migrate=False)

db.fc_pago_det.fc_forma_pago_id.requires = IS_IN_DB(db,db.fc_forma_pago.id,'%(nombre)s')
db.fc_pago_det.fc_banco_id.requires = IS_IN_DB(db,db.fc_banco.id,'%(nombre)s')

#--------
db.define_table('fc_pago_viaje',
	Field('id','integer'),
	Field('fc_pago_id','integer'),
	Field('mv_viaje_id','integer'),
	migrate=False)

#--------
db.define_table('fc_pago_servicio',
	Field('id','integer'),
	Field('cantidad','integer'),
	Field('descripcion','string'),
	Field('importe','float'),
	Field('fc_pago_id','integer'),
	Field('fc_servicio_id','integer'),	
	migrate=False)
db.fc_pago_servicio.fc_servicio_id.requires = IS_IN_DB(db,db.fc_servicio.id,'%(descripcion)s')


def get_tarifa_ser(codigo):
	tarifarec=db( (db['fc_servicio'].codigo==codigo)).select()
	if len(tarifarec)  > 0:
		for row in tarifarec:			
			if row.porcentaje:
				tarifa=row.porcentaje
			else:
				tarifa=row.tarifa_cobro
			desc=row.descripcion
			id=row.id
	return [tarifa, desc, id]
	
def get_tarifa(desde,hasta, tipov):	
	tarifarec=db( (db['fc_servicio'].mt_ciudad_desde==desde)  &  (db['fc_servicio'].mt_ciudad_hasta==hasta)  & (db['fc_servicio'].cf_vehiculo_tipo_id==tipov) & (db['fc_servicio'].cf_vehiculo_tipo_id==db.cf_vehiculo_tipo.id) ).select()		
		#si tarifa no existe?
	if len(tarifarec)  > 0:
		for row in tarifarec:			
			tarifa=row.fc_servicio.tarifa_cobro
			desc=row.fc_servicio.descripcion
			vehi=row.cf_vehiculo_tipo.nombre			
			id =row.fc_servicio.id
		return [tarifa, desc, vehi, id]
	else:
		return None

def get_tarifa_chofer(id):
	tarifarec=db( (db['fc_servicio'].id==id)).select()
	if len(tarifarec)  > 0:
		for row in tarifarec:			
			if row.porcentaje_chofer:
				tarifa=row.porcentaje_chofer
			else:
				tarifa=row.tarifa_chofer
			desc=row.descripcion
			id=row.id
	return [tarifa, desc, id]
	
def get_tarifa_from_id(id):
	datarec=db( (db['fc_servicio'].id==id) ).select()
	for row in datarec:
		if row.is_viaje:
			tarifarec=db( (db['fc_servicio'].id==id) & (db['fc_servicio'].cf_vehiculo_tipo_id==db.cf_vehiculo_tipo.id) ).select()
		else:
			tarifarec=datarec
	if len(tarifarec)  > 0:
		return tarifarec
	else:
		return None

def get_correlativo(tipo):
		tabla='fc_tipo_doc'
		record=tarifarec=db( (db[tabla].id == tipo )  ).select()	
		for row in record:
			r = int(row.correlativo)
			nr = int(row.correlativo)+1
			db((db[tabla].id==tipo)).update(correlativo=nr)
		return nr
	
def build_query(field, op, value):
    if op == 'igual':
        return field == value
    elif op == 'no igual a':
        return field != value
    elif op == 'mayor que':
        return field > value
    elif op == 'menor que':
        return field < value
    elif op == 'comienza con':
        return field.like(value+'%')
    elif op == 'termina en':
        return field.like('%'+value)
    elif op == 'contiene':
        return field.like('%'+value+'%')

def dynamic_search(table,strfields):
	tbl = TABLE()
	selected = []
	ops = ['igual','no igual a','mayor que','menor que','comienza con','termina en','contiene']
	#print table.fields
	query = table.id > 0    
	for field in table.fields:
		if field in strfields:
			chkval = request.vars.get('chk'+field,None)
			txtval = request.vars.get('txt'+field,None)
			opval = request.vars.get('op'+field,None)
			row = TR(TD(INPUT(_type="checkbox",_name="chk"+field,value=chkval=='on')), \
					TD(field),TD(SELECT(ops,_name="op"+field,value=opval)), \
					TD(INPUT(_type="text",_name="txt"+field, _value=txtval)))
			tbl.append(row)
			if chkval:
				if txtval:					
					query &= build_query(table[field], opval,txtval)
					selected.append(table[field]) 
	
	if len(selected) > 0:
			selected.append(table.id) 
			results = db(query).select(*selected)
	else:
		results = None
	
	form = FORM(tbl,INPUT(_type="submit"))
	return form, results  

	
webgrid = local_import('webgrid')


class MyFPDF(FPDF, HTMLMixin):
	def header(self):
		self.set_font('Arial','B',12)
		self.cell(0,0, response.title ,0,0,'C')
		self.ln(10)
	def footer(self):
		self.set_y(-15)
		self.set_font('Arial','I',6)
		txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
		self.cell(0,10,txt,0,0,'C')
	
	
