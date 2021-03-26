
def index():
	return dict(message='Listado de Disponibles')

def configs():	
	if request.args(0):
		tabla = request.args(0)	
	
		form = SQLFORM.factory(Field('Nombre_contiene') )		
		#URL(c='reportes',  f='impresion', 
		if form.process().accepted:
			response.flash = 'Procesando'
			session.valorbusqueda = form.vars.Nombre_contiene
			redirect(URL(c='reportes',  f='impresion', args=[tabla,session.valorbusqueda ]))
	
		return dict(message='Listado de Tablas', tablas=db.tables, form=form, tabla=tabla)
	else:
	
		return dict(message='Listado de Tablas', tablas=db.tables)

def maestros():
	return dict(message='Listados Mastros', tablas=db.tables)
	
def impresion():
	valor=""
	if request.args(0):
		#para todas las tablitas sin ruptura de control 		
		tabla = request.args(0)		
		rows = []
		col = 0				
		if tabla in "cf_asignacion_tipo, cf_cargo, cf_tipo_combustible, cf_tipo_doc, cf_vehiculo_tipo, cf_solicitud_tipo, cf_vehiculo_marca":
			if tabla == "cf_asignacion_tipo":
				response.title = "Tipos de Asignacion de vehiculos"					
			if tabla == "cf_cargo":
				response.title = "Cargos de personas"			
			if tabla == "cf_tipo_combustible":
				response.title = "Tipos de combustible"	
			if tabla == "cf_tipo_doc":
				response.title = "Tipos de documentos"	
			if tabla == "cf_vehiculo_tipo":
				response.title = "Tipos de vehiculo"	
			if tabla == "cf_solicitud_tipo":
				response.title = "Tipos de solicitudes para vehiculos"							
			if tabla == "cf_vehiculo_marca":
				response.title = "Marcas de vehiculo"							
			
			if request.args(1):
				valor = request.args(1)
				lineas=db(db[tabla].nombre.like('%'+valor+'%')).select(orderby=db[tabla].nombre)				
			else:
				lineas=db(db[tabla]).select(orderby=db[tabla].nombre)
				
			head = THEAD(TR(TH("Id",_width="20%"), 
                    TH("Nombre",_width="80%"),                    
                    _bgcolor="#585858"))
			foot=""
			
			for i in lineas:		
				col=col+1	
				bak = col % 2 and "#BDBDBD" or ""				
				rows.append(TR(TD(i.id, _align="center"),
					   TD(i.nombre, _align="left"),						
						_bgcolor=bak)) 		
				# make the table object
			body = TBODY(*rows)
			table = TABLE(*[head,foot, body], _border="1", _align="center", _width="100%")			
			html=table
		
		#items********************************************
		if tabla in "cf_item_grupo,  cf_item":
			head = THEAD(TR(TH("Id",_width="25%"), 
                    TH("Nombre",_width="75%"),                    
                    _bgcolor="#585858"))
			foot=""
			response.title = "Items para gastos"	
			linmaster=db(db.cf_item_grupo).select(orderby=db.cf_item_grupo.nombre)			
			for h in linmaster:
				rows.append(TR(TD("*** Grupo de gasto: "+h.nombre,    _align="left" ))) 				
				lineas = db(db.cf_item.cf_item_grupo_id==h.id).select(orderby=db.cf_item.nombre)				
				col=0
				for i in lineas:
					col=col+1	
					bak = col % 2 and "#BDBDBD" or ""				
					rows.append(TR(TD(i.id, _align="center"),
								   TD(i.nombre, _align="left"),						
									_bgcolor="")) 
					if col==len(lineas):
						rows.append(TR(TD("*** Total items: "+str(len(lineas)),    _align="left" ))) 													
									
			body = TBODY(*rows)
			table = TABLE(*[head,foot, body], _border="0", _align="center", _width="100%")
			html=table
		#fin items ******************************************

		#modelos********************************************
		if tabla == "cf_vehiculo_modelo":
			
			head = THEAD(TR(TH("Id",_width="25%"), 
                    TH("Nombre",_width="75%"),                    
                    _bgcolor="#585858"))
			foot=""
			if request.args(1):
				valor = request.args(1)				
				linmaster=db((db.cf_vehiculo_marca.id==db.cf_vehiculo_modelo.cf_vehiculo_marca_id)&(db.cf_vehiculo_modelo.nombre.like('%'+valor+'%'))).select( orderby=db.cf_vehiculo_marca.nombre)						
			else:
				linmaster=db(db.cf_vehiculo_marca).select( orderby=db.cf_vehiculo_marca.nombre)						
			response.title = "Modelos de Vehiculos"	
			
			
			for h in linmaster:				
				if valor<>"":
					rows.append(TR(TD("*** Marca: "+h.cf_vehiculo_marca.nombre,    _align="left" ))) 				
					lineas = db((db.cf_vehiculo_modelo.cf_vehiculo_marca_id==h.cf_vehiculo_marca.id)&(db.cf_vehiculo_modelo.nombre.like('%'+valor+'%'))).select(orderby=db.cf_vehiculo_modelo.nombre)	
				else:
					rows.append(TR(TD("*** Marca: "+h.nombre,    _align="left" ))) 				
					lineas = db((db.cf_vehiculo_modelo.cf_vehiculo_marca_id==h.id)).select(orderby=db.cf_vehiculo_modelo.nombre)	
				col=0
				for i in lineas:
					col=col+1	
					bak = col % 2 and "#BDBDBD" or ""				
					rows.append(TR(TD(i.id, _align="center"),
								   TD(i.nombre, _align="left"),						
									_bgcolor="")) 
					if col==len(lineas):
						rows.append(TR(TD("*** Total modelos: "+str(len(lineas)),    _align="left" ))) 													
									
			body = TBODY(*rows)
			table = TABLE(*[head,foot, body], _border="0", _align="center", _width="100%")
			html=table
		#fin modelos ******************************************

	if request.extension=="pdf":		                            
		pdf=MyFPDF()
		# first page:
		pdf.add_page()
		pdf.write_html(str(XML(html, sanitize=False)))
		#puede haber mas de un write html con variable distintas para completar el html
		#pdf.write_html(str(XML(CENTER(chart), sanitize=False)))

		response.headers['Content-Type']='application/pdf'
		return pdf.output(dest='S')
	else:
		# normal html view:		
		return dict(table=table, titulo=response.title, tabla=tabla, valor=valor)
	
def presupuestos():	
	if request.args(0):
		#para todas las tablitas sin ruptura de control 		
		tipo = request.args(0)
	if tipo == "todos":
		pass


def index_2():   
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

def porcobrar():		
	import csv, time, math
	from gluon.contrib.pyfpdf import Template
	import os.path
	import sys	
	if request.args(0):
		if request.args(0) == 'todos' :
			sql="SELECT cf_proveedor_id, cf_proveedor.razon_social,fc_documento.fecha, \
					fc_documento.correlativo,fc_documento.fecha_vencimiento,DATEDIFF(CURDATE(), 	\
					fc_documento.fecha_vencimiento) dias,\
					(select sum(total) from fc_documento_det where fc_documento_det.fc_documento_id=fc_documento.id) total,\
					(select sum(monto) from fc_cobro_det where fc_cobro_det.fc_documento_id=fc_documento.id) cobrado \
					FROM fc_documento \
				inner join cf_proveedor on fc_documento.cf_proveedor_id=cf_proveedor.id \
				where fc_documento.fc_tipo_doc_id=2\
				having total=cobrado \
				order by cf_proveedor_id;"				
			sqlid="SELECT cf_proveedor_id id, count(cf_proveedor_id) count, \
				(select sum(total) from fc_documento_det where fc_documento_det.fc_documento_id=fc_documento.id) total, \
				(select sum(monto) from fc_cobro_det where fc_cobro_det.fc_documento_id=fc_documento.id) cobrado \
				FROM fc_documento \
				inner join cf_proveedor on fc_documento.cf_proveedor_id=cf_proveedor.id \
				where fc_documento.fc_tipo_doc_id=2  \
				having total=cobrado \
				order by cf_proveedor_id;"
			rec = db.executesql(sql, as_dict=True)		
			rec_id=db.executesql(sqlid, as_dict=True)		
			#doc_record=db(db.fc_documento.id == request.args(0)).select()
			#doc_det_rec=db(db.fc_documento_det.fc_documento_id == request.args(0)).select(orderby=db.fc_documento_det.id)			
	emp_rec=db(db.cf_empresa.id == 1).select()
	#print emp_rec
	f = Template(format="A4",
	title="Cuentas por Cobrar", author="w.a", subject="w.a", keywords="")	
	f.parse_csv(infile=request.folder+'/static/rpt/porcobrar.csv', delimiter=";", decimal_sep=",")
	
	max_lines_per_page = 49.0
	lines = len(rec)	
	ids = len(rec_id)	
	if ids > lines:
		pages=ids
	else:
		pages = int(math.ceil( float(lines / (max_lines_per_page - 1)) ))	
	page=0
#
#    # fill placeholders for each page
	total = float("0.00")	
	for row in range(len(rec_id)):		#primer proveedor para ruptura de control				
		#nro paginas para este proveedore
		#print rec_id.index()
		subpages=int(math.ceil( float(rec_id[row]['count'] / (max_lines_per_page - 1)) ))	
		for pg in range(subpages):
			f.add_page()
			page+=1
			f['page'] = 'Pagina %s de %s' % (page, pages)
			if pages>1 and page<pages:
				s = 'Continua en la pagina %s' % (page+1)
			else:
				s = ''					
			# setting data from company
			rowemp = emp_rec[0]
			f["EMPRESA"] = rowemp.razon_social
			f["Logo"] = os.path.join(request.env.web2py_path,"applications","flota","uploads",rowemp.ruta_foto) 
			f["membrete1"] = 'Rif.:'+rowemp.rif +'  -   Nit.: '+rowemp.nit
			f["membrete2"] = 'Tel.:'+rowemp.tlf +'  -   Fax.: '+rowemp.fax + 'Email.:'+rowemp.email					
			#datos del proveedor
			f["proveedor.nombre"] = rowemp['razon_social']
			proveedor=rec_id[row]['id']
			# print line item...			
			li = 0 
			k = 0			
			subtotal=float("0.00")						
			for rowdet in rec:
				if rowdet['cf_proveedor_id']	== proveedor:				
					k = k + 1
					if k > page * (max_lines_per_page - 1):
						break					
					if k > (page - 1) * (max_lines_per_page - 1):
						if rowdet['total']==rowdet['cobrado']:						
							li += 1
							f['factura%02d' % li] = rowdet['correlativo']							
							f['fecha%02d' % li] =  rowdet['fecha']							
							f['vencimiento%02d' % li] = rowdet['fecha_vencimiento']							
							f['dias%02d' % li] = rowdet['dias']							
							f['monto%02d' % li] = "%0.2f" % rowdet['total']
							subtotal+=rowdet['total']
							total+=subtotal
				else:
					f['subtotal.monto' ] = "%0.2f" % subtotal
					break
			if subtotal > 0:
				f['subtotal.monto' ] = "%0.2f" % subtotal
	f['total.monto'] = "%0.2f" % total
	
	f.render("./porcobrar.pdf")	
	if sys.platform.startswith("linux"):	
		#print os.getcwd()
		os.system("evince ./porcobrar.pdf")
	else:
		os.system("./porcobrar.pdf")
	redirect(URL(c='default',  f='index'))
