# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

  
def index():			
	tabla=request.args(0)
	grid = webgrid.WebGrid(crud)
	if tabla:
		if tabla=='mv_solicitud':
			grid.fields = [tabla+'.descripcion',tabla+'.fecha_solicitud',tabla+'.mt_persona_id']
			grid.field_headers = ['Descripcion','Fec. Sol.','Persona']
		elif 	tabla=='mv_asignacion':
			grid.fields = [tabla+'.descripcion',tabla+'.fecha_proceso',tabla+'.fecha_inicio']
			grid.field_headers = ['Descripcion','Fec. Sol.','Fecha Inicio']
		elif 	tabla=='mv_viaje':
			grid.fields = [tabla+'.descripcion',tabla+'.fecha_inicio',tabla+'.fecha_fin']
			grid.field_headers = ['Descripcion','Fecha Inicio.','Fecha Fin']
			
		#grid.crud_function = URL(c='movimientos',  f='show_form')
		grid.action_links = ['view', 'edit']
		grid.action_headers = ['Accion', '']
		grid.datasource = db(db[tabla].id>0)
		grid.pagesize = 10
		grid.messages.confirm_delete = 'Seguro de realizar esta accion?'
		grid.messages.no_records = 'No hay registros'
		grid.messages.add_link = '[Agregar %s]'		
		grid.enabled_rows = ['header','add_links', 'pager']
		# acciones personalizadas
		grid.view_link= lambda row: A('Ver', _href= URL(f='show_form/'+tabla, args=[row['id'], 'True']))
		grid.edit_link= lambda row: A('Edit', _href= URL(f='show_form/'+tabla, args=[row['id']]))
	 	grid.add_links = lambda tables: TR(TD([A(' Nuevo ', _href= URL(f='show_form/'+tabla))  for t in grid.tablenames]))
		return dict(grid=grid()) #notice the ()
	else:
		return dict() #

def show_form():		
	tabla=request.args(0)
	readonly=request.args(2)
	if readonly=='True':
		deletable='False'		
	else:		
		deletable='True'
		
	if tabla:
		tabladb=db[request.args(0)]
		registro=db[request.args(0)](request.args(1))
		if tabla=='mv_solicitud':
			campos=['cf_solicitud_tipo_id', 'mt_persona_id','fecha_solicitud','descripcion' , 'fecha_inicio',  'fecha_fin']
		elif tabla=='mv_asignacion':
			campos=[ 'mv_solicitud_id', 'mt_vehiculo_id','cf_asignacion_tipo_id', 'cf_localidad_id', 'mt_persona_id','fecha_proceso','descripcion' , 'fecha_inicio',  'fecha_fin']
		elif tabla=='mv_viaje':
			campos=['mv_asignacion_id', 'descripcion' , 'fecha_inicio',  'fecha_fin' , 'mt_ciudad_desde' , 'mt_ciudad_hasta']
			
		form=SQLFORM(tabladb, registro, submit_button='Enviar' , delete_label='Click para borrar:', next=URL(c='movimientos',  f='index/'+tabla)
							 , deletable=deletable , fields=campos ,showid=False , readonly=readonly )		
		if form.accepts(request.vars, session):
			response.flash = 'Operacion exitosa !'
			redirect(URL(c='movimientos',  f='index/'+tabla))
		elif form.errors:
			response.flash = 'Ha habido un error !'
		return dict(form=form,  tabla=tabla)
	else:
		return dict()

def search():
	tabla=request.args(0)
	registro=request.args(1)
	frmsearch,results = dynamic_search(db[tabla],'descripcion, fecha_registro, fecha_inicio, fecha_fin, fecha_solicitud')	
	if results <> None: 		
		return dict(tabla=tabla, frmsearch=frmsearch,  lista=results)			
	else: 
		return dict(tabla=tabla, frmsearch=frmsearch)	
	

def index_app():   
	elcrud=crud
	elcrud.settings.download_url = URL('download')
	if  request.args(0) <> None and request.args(1) == None	  :
		tabla=request.args(0)		
		#lista = db(db[tabla]).select()
		form = elcrud.create(db[tabla], next=URL('index'), message=T("Registro insertado con exito"))
		#print results.as_dict()
		return dict(form=form,  tabla=tabla)	
	elif request.args(0) <> None and request.args(1) <> None:	  	
	  	tabla=request.args(0)
		registro=request.args(1)
		form = elcrud.update(db[tabla], registro, next=URL('index'),  message=T("Registro actualizado con exito"))
		return dict(form=form,  tabla=tabla)
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

    
    
    
    
