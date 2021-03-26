def index():   
#muestro form de busqueda de gastos
	tabla='mv_gasto'
	grid = webgrid.WebGrid(crud)
	grid.fields = [tabla+'.descripcion',tabla+'.fecha_registro',tabla+'.fecha_gasto']
	grid.field_headers = ['Descripcion','Fecha Reg.','Fecha Gasto']
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
	return dict(grid=grid(), tabla=tabla) #notice the ()

def show_form():		
	tabla=request.args(0)
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
				
	if tabla:
		tabladb=db[request.args(0)]
		registro=db[request.args(0)](request.args(1))		
		if tabla=='mv_gasto':
			labels = {'mv_asignacion_id':'Asignacion', 'cf_proveedor_id':'Proveedor'}
			campos=['mv_asignacion_id','descripcion','fecha_registro','fecha_gasto' , 'kilometraje','cf_proveedor_id','referencia', 'subtotal', 'impuesto', 'recargo', 'descuento']			
			
			form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='gastos',  f='index/'+tabla) , \
		              	fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels)

		elif tabla=='mv_gasto_det':
			for i in range(0, len(request.args)):
				if 'master' in request.args(i):					
					master=request.args(i).split('_')[1]										
			
			campos=['cf_item_id','cantidad','unitario' ]							
			labels = {'cf_item_id':'Item '}
			form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', \
									next=URL(c='gastos',  f='show_form', args=['mv_gasto','master','True']) , \
									 fields=campos ,showid=False , deletable=deletable, readonly=readonly ,  labels=labels)
			form.vars.mv_gasto_id=master

		if form.accepts(request.vars, session):
			response.flash = 'Operacion exitosa !'
			if tabla=='mv_gasto':
				redirect(URL(c='gastos',  f='index/'+tabla))
			elif tabla=='mv_gasto_det':			
				redirect(URL(c='gastos',  f='show_form',  args=['mv_gasto',master,'True']))
		elif form.errors:
			response.flash = 'Ha habido un error !'
		
		if registro and readonly and  tabla=='mv_gasto':
			grid2=detail_grid(request.args(1))
			return dict( form=form,  tabla=tabla,  grid2=grid2())
		else:
			return dict( form=form,  tabla=tabla)
	else:
		return dict()

		
def detail_grid(registro):
	tabla='mv_gasto_det'
	grid2 = webgrid.WebGrid(crud)
	data  = db((db.mv_gasto_det.mv_gasto_id==db.mv_gasto.id)  & (db.mv_gasto_det.cf_item_id==db.cf_item.id)  &  (db.mv_gasto_det.mv_gasto_id==registro)).select('mv_gasto_det.id','cf_item.nombre', 'mv_gasto_det.cantidad', 'mv_gasto_det.unitario', 'mv_gasto_det.total')	
	#print db._lastsql
	#print tabla, registro	
	grid2.fields = ['mv_gasto_det.id','cf_item.nombre', 'mv_gasto_det.cantidad', 'mv_gasto_det.unitario', 'mv_gasto_det.total']
	grid2.field_headers = ['Id','Item.','Cantidad', 'Unit.', 'Total']
	grid2.action_links = ['view', 'edit']
	grid2.action_headers = ['Accion', '']
	grid2.datasource = data
	#db(db[tabla].id>0)
	grid2.pagesize = 10
	grid2.messages.confirm_delete = 'Seguro de realizar esta accion?'
	grid2.messages.no_records = 'No hay registros'
	grid2.messages.add_link = '[Agregar %s]'		
	grid2.enabled_rows = ['header','add_links', 'pager']
	# acciones personalizadas
	
	#values="'Items','height=700,width=800,left=10,top=10,resizable=yes,scrollbars=no,toolbar=no,menubar=no,location=no,directories=no,status=no'"
	#grid2.view_link= lambda row: A('Ver',  _onclick="javascript:window.open('"+URL(f='show_form/'+tabla, args=[row['mv_gasto_det.id'],  'True','master_'+str(registro) ])+"',"+values+")")
	grid2.view_link= lambda row: A('Ver', _href= URL(f='show_form/'+tabla, args=[row['mv_gasto_det.id'],  'True','master_'+str(registro) ]))
	grid2.edit_link= lambda row: A('Edit', _href= URL(f='show_form/'+tabla, args=[row['mv_gasto_det.id'], 'master_'+str(registro) ]))
	grid2.add_links = lambda tables: TR(TD([A(' Nuevo ', _href= URL(f='show_form/'+tabla, args=['master_'+str(registro)] ))  ]))
	return grid2


def search():
	tabla=request.args(0)
	registro=request.args(1)
	frmsearch,results = dynamic_search(db[tabla],'descripcion, fecha_registro, fecha_gasto')
	if results <> None: 		
		return dict(tabla=tabla, frmsearch=frmsearch,  lista=results)			
	else: 
		return dict(tabla=tabla, frmsearch=frmsearch)	



def movimiento():
#procesamiento del form
	record = db.mv_gasto(request.args(0))
	form = SQLFORM(db.mv_gasto, record)
	if form.accepts(request.vars, session):
		response.flash = 'Registro Exitoso'
	elif form.errors:
		response.flash = 'Se encontraron Errores'
	return dict(form=form)

