# -*- coding: utf-8 -*-
### required - do no delete

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
	#muestro form de busqueda de gastos
	tabla='mv_asignacion'
	grid = webgrid.WebGrid(crud)
	grid.fields = [tabla+'.fecha_proceso', tabla+'.descripcion']
	grid.field_headers = ['Fecha Proceso', 'Descripcion ']
	grid.action_links = ['view', 'edit']
	grid.action_headers = ['Accion', '']
	grid.datasource = db(db[tabla].id>0)
	grid.pagesize = 20
	grid.messages.confirm_delete = 'Seguro de realizar esta accion?'
	grid.messages.no_records = 'No hay registros'
	grid.messages.add_link = '[Agregar %s]'		
	grid.enabled_rows = ['header','add_links', 'pager']
	# acciones personalizadas
	grid.view_link= lambda row: A('Ver', _href= URL(f='show_form', args=[row['id'], 'True']))
	grid.edit_link= lambda row: A('Edit', _href= URL(f='show_form', args=[row['id']]))
	grid.add_links = lambda tables: TR(TD([A(' Nuevo ', _href= URL(f='show_form'))  for t in grid.tablenames]))
	return dict(grid=grid(), tabla=tabla) #notice the ()

def show_form():		
	tabla='mv_asignacion'
	thereistrue =  False	
	for i in range(0, len(request.args)):
		if request.args(i)=='True':
			thereistrue=True
	if thereistrue ==  True:
		readonly=True
		deletable=False
	else:		
		readonly=False
		deletable=True
				
	tabladb=db[tabla]
	registro=db[tabla](request.args(0))		
	
	labels = {'descripcion':'Descripcion', 'fecha_proceso':'Fecha Proceso',  'mt_vehiculo_id':'Vehiculo',  'mt_persona_id':'Chofer',   
				'mv_viaje_id':'ID Viaje'  }
	campos=['fecha_proceso','mv_viaje_id','mt_persona_id', 'mt_vehiculo_id',  'descripcion']			
			
	form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='cliente',  f='index') , \
		              	fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels, upload=URL('download'))

	if form.accepts(request.vars, session):
		response.flash = 'Operacion exitosa !'
		redirect(URL(c='asignacion',  f='index'))
	elif form.errors:
		response.flash = 'Ha habido un error !'

	return dict( form=form)

def run():
	pass

def error():
    return dict()

