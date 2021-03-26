# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#@auth.requires_login()
@auth.requires_permission('Config')
def index():   
	#elcrud=crud
	#elcrud.settings.download_url = URL('download')

	if  request.args(0) <> None :
		tabla=request.args(0)		
		registro=db[request.args(0)](request.args(1))		
		labels={'mt_persona_id':'Cedula', 'cf_cargo_id':'Cargo', 'cf_tipo_doc_id':'Tipo Doc', 'mt_vehiculo_id':'Placa',\
					'cf_item_id':'Item',  'cf_item_grupo_id':'Item Grupo', 'cf_vehiculo_marca_id': 'Marca'}
		
		if registro:
			borrable=True
		else:
			borrable=False
		
		form = SQLFORM(db[tabla], registro,  submit_button='Enviar' ,    delete_label='Click para borrar:',  next=URL(c='tablas',  f='index/'+tabla), \
								message=T("Operacion Exitosa !"), labels=labels, upload=URL('download'), deletable=borrable)	
		
		if 'asignacion_tipo' in tabla:
			lista = db(db.cf_asignacion_tipo).select()
			tipo = 'asignacion_tipo'
		elif 	'aviso' in tabla:
			lista = db(db.cf_aviso).select()
			tipo = 'aviso'
		elif 	'cargo' in tabla:
			lista = db(db.cf_cargo).select()
			tipo = 'cargo'
		elif 	'item_grupo' in tabla:
			lista = db(db.cf_item_grupo).select()
			tipo = 'item_grupo'
		elif 'item' in tabla and 'grupo' not in tabla:
			lista = db(db.cf_item.cf_item_grupo_id==db.cf_item_grupo.id).select(orderby=db.cf_item_grupo.nombre|db.cf_item.nombre)
			tipo = 'item'			
		elif 	'localidad' in tabla:
			lista = db(db.cf_localidad).select()
			tipo = 'localidad'	
		elif 	'solicitud_tipo' in tabla:
			lista = db(db.cf_solicitud_tipo).select()
			tipo = 'solicitud_tipo'	
		elif 	'tipo_combustible' in tabla:
			lista = db(db.cf_tipo_combustible).select()
			tipo = 'tipo_combustible'	
		elif 	'tipo_doc' in tabla:
			lista = db(db.cf_tipo_doc).select()
			tipo = 'tipo_doc'	
		elif 	'vehiculo_marca' in tabla:
			lista = db(db.cf_vehiculo_marca).select()
			tipo = 'vehiculo_marca'	
		elif 'vehiculo_modelo' in tabla :
			lista = db(db.cf_vehiculo_modelo.cf_vehiculo_marca_id==db.cf_vehiculo_marca.id).select(orderby=db.cf_vehiculo_marca.nombre|db.cf_vehiculo_modelo.nombre)
			tipo = 'vehiculo_modelo'			
		elif 	'vehiculo_tipo' in tabla:
			lista = db(db.cf_vehiculo_tipo).select()
			tipo = 'vehiculo_tipo'				
		elif 	'viaje_tipo' in tabla:
			lista = db(db.cf_viaje_tipo).select()
			tipo = 'viaje_tipo'				
			
		if form.accepts(request.vars, session):
			response.flash = 'Operacion exitosa !'
			redirect(URL(c='tablas',  f='index/'+tabla))
		elif form.errors:
			response.flash = 'Ha habido un error !'		
		return dict(form=form, lista=lista, tabla=tabla, tipo=tipo)		
		
	else:
		return dict(message='Listado de Tablas', tablas=db.tables)
			
	

def download():
	return response.download(request, db)    

def vehiculo_report():
	from reports import ReportVehiculo
	from geraldo.generators import PDFGenerator
	import gluon.contenttype
	import StringIO
	resp = StringIO.StringIO()
	vehiculos = db(db.mt_vehiculo.id > 0).select(orderby=db.mt_vehiculo.placa)
	report = ReportVehiculo(queryset=vehiculos)
	report.generate_by(PDFGenerator, filename=resp)
	resp.seek(0)
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.pdf')
	filename = "%s_Vehiculos.pdf" % (request.env.server_name)
	response.headers['Content-disposition'] = "attachment; filename=\"%s\"" % filename
	return resp.read()
    
    
    
    
    
    
    
    
