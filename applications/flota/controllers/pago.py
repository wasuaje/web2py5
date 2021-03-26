# -*- coding: utf-8 -*-
### required - do no delete

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
	#muestro form de busqueda de gastos
	tabla='fc_pago'
	tabla2='mt_persona'
	grid = webgrid.WebGrid(crud)
	grid.fields = [tabla+'.fecha', tabla+'.total',  tabla+'.descripcion', tabla2+'.nombres', tabla2+'.apellidos']
	grid.field_headers = ['Fecha', 'Total', 'Descripcion','Nombres', 'Apellidos']
	grid.action_links = ['view', 'edit']
	grid.action_headers = ['Accion', '']
	tabla=	db((db[tabla].mt_persona_id==db.mt_persona.id) ).select()
	grid.datasource = tabla
	grid.pagesize = 20
	grid.messages.confirm_delete = 'Seguro de realizar esta accion?'
	grid.messages.no_records = 'No hay registros'
	grid.messages.add_link = '[Agregar %s]'		
	grid.enabled_rows = ['header','add_links', 'pager']
	# acciones personalizadas
	grid.view_link= lambda row: A('Ver', _href= URL(f='show_form', args=[row['fc_pago.id'], 'True']))
	grid.edit_link= lambda row: A('Edit', _href= URL(f='show_form', args=[row['fc_pago.id']]))	
	grid.add_links =  lambda tables: TR(TD([A(' Nuevo ', _href= URL(f='show_form'))  ]))	
	return dict(grid=grid(), tabla=tabla) #notice the ()

def show_form():		
	tabla='fc_pago'
	thereistrue =  False	
	agregardetalle= False
	agregarservicio=False
	for i in range(0, len(request.args)):
		if request.args(i)=='True':
			thereistrue=True
		elif 	request.args(i)=='Detalle':
			agregardetalle= True
		elif 	request.args(i)=='Servicio':
			agregarservicio=True
			
	if thereistrue ==  True:
		readonly=True
		deletable=False
	else:		
		readonly=False
		deletable=True

	tabladb=db[tabla]
	registro=db[tabla](request.args(0))		
	
	labels = {'fecha':'Fecha', 'descripcion':'Descripcion',  'total':'Total Pago',  'mt_persona_id':'Conductor'}
	campos=[ 'mt_persona_id',  'fecha',  'descripcion', 'total']			
			
	form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='cliente',  f='index') , \
		              	fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels, upload=URL('download'))		

	total=0
	cobrado=0
	rec = db(db.fc_pago.id==request.args(0)).select()
	for row in rec:
		total=row.total
	
	rec = db(db.fc_pago_det.fc_pago_id==request.args(0)).select()
	for row in rec:
		cobrado+=row.monto
	print cobrado, total
	
	if thereistrue:
		elform=''
		lineas=''
		if  agregardetalle:			
			tabladet='fc_pago_det'
			tabladb=db[tabladet]
			registro=''
			labels = {'fecha':'Fecha', 'descripcion':'Descripcion',  'monto':'Monto Pago',  
						  'referencia':'Referencia',  'fc_forma_pago_id':'Forma de Pago',  'fc_banco_id':'Banco', 
						  }
			campos=[ 'fecha',  'fc_forma_pago_id',  'fc_banco_id',  'referencia',  'monto',  'descripcion']
			formdet=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='pago',  f='show_form/'+request.args(0)+'True') , \
							fields=campos ,showid=False , deletable=deletable ,  readonly=False , labels=labels, upload=URL('download'))		
			formdet.vars.fc_pago_id=request.args(0)
			lineas=show_detail(request.args(0))		
			elform=formdet		
		#if formdet.accepts(request.vars, session):		
			if formdet.process(onvalidation=validarDo).accepted:
				response.flash = 'Detalle Agregado !'
				redirect(URL(c='pago',  f='show_form/'+str(request.args(0))+'/True/Detalle'))	
		elif agregarservicio:
			tabladet='fc_pago_servicio'
			tabladb=db[tabladet]
			elid=request.args(0)
			registro=''
			labels = {'cantidad':'Cantidad', 'descripcion':'Descripcion',  'importe':'importe',  
		               'fc_servicio_id':'Servicio'
					  }
			campos=[ 'fc_servicio_id',  'descripcion',  'cantidad',  'importe']
			formdet=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:',  \
		              	fields=campos ,showid=False , deletable=deletable ,  readonly=False , labels=labels, upload=URL('download'))		
			formdet.vars.fc_pago_id=request.args(0)		
			lineas=show_detail_pago(request.args(0))		
			elform=formdet		
			if formdet.accepts(request.vars, session):					
				totalpago=0
				totalimp=float(request.vars.importe)
				rec1=db(db.fc_pago.id==elid).select()
				for i in rec1:
					if i.total:
						totalpago=i.total
					else:
						totalpago=0
				rec = db(db.fc_pago.id==elid).update(total=totalpago+totalimp)		
				response.flash = 'Servicio Agregado !'
				redirect(URL(c='pago',  f='show_form/'+str(request.args(0))+'/True/Servicio'))	
	else:
		elform=''
		printform=''
		lineas=''

	#lineas=show_detail(request.args(0))		
	if form.accepts(request.vars, session):
		response.flash = 'Operacion exitosa !'
		myid = form.vars.id		
		if form.vars.delete_this_record=="on":
			# me aseguro de borrar el detalle
			db((db["fc_pago_det"].fc_pago_id==myid)).delete()
			redirect(URL(c='pago',  f='index'))		
		else:
			redirect(URL(c='pago',  f='selectviaje/'+str(myid)))
	elif form.errors:
		response.flash = 'Ha habido un error !'
		
	#return dict( form=form,   printform=printform)
	if request.args(0):
		printform = DIV(TABLE(TR(A('Agregar Servicio', _href=URL('show_form/'+str(request.args(0)+'/True/Servicio'))), 
												 A(' - '), 
												 A('Agregar Pago', _href=URL('show_form/'+str(request.args(0))+'/True/Detalle')), 
												 A(' - '), 
											     A('Volver', _href=URL('index/'))
												 )))			
	else:
		printform = DIV(TABLE(TR(
											     A('Volver', _href=URL('index/'))
												 )))			
		
	return dict( form=form,  frmdet=elform,  printform=printform,  lineas= DIV((lineas)))

def selectviaje():
	tabla='mv_viaje'
	idpago=request.args(0)
	#data  = db((db[tabla].mv_campania_id==id_camp)).select()	
	#regions=data.as_list()
	#form = SQLFORM.factory(Field('preguntas', requires=IS_IN_SET([r['id'] for r in regions], labels=[r['descripcion'] for r in regions],multiple=True )))
	
	form = SQLFORM.factory(
								Field('viajes', requires=IS_IN_DB(db(db.mv_viaje.status==0), 
														db.mv_viaje.id, '%(descripcion)s %(fecha_solicitud)s', multiple=True )))
	
	if form.process().accepted:		
		id_viajes=request.vars.viajes
		#inserto en la union de pagos y viajes para marcar viajes como pagados
		for i in id_viajes:
			db.fc_pago_viaje.insert(mv_viaje_id=i, fc_pago_id=idpago)
		redirect(URL(c='pago',  f='show_form/'+str(idpago)+'/True'))
		
		#redirect(URL(c='pago',  f='showform/'+str(idpago)+'True'))
	return dict( form=form)

def confirm():
	id_viajes=request.args(0)
	header=[]
	header.append(['Accion', 'Cant.','Descripcion', 'Monto'])
	listado = []   
	total=0
	for i in id_viajes:
		#busco el detalle de cada viaje en documento
		rec = db((db.fc_documento_det.mv_viaje_id==i) & 
		         (db.fc_documento.id==db.fc_documento_det.fc_documento_id) &
				 (db.fc_documento_det.fc_servicio_id==db.fc_servicio._id) &
				 (db.fc_documento.fc_tipo_doc_id==2) 
				 ).select(orderby=db.fc_documento_det.id)
		k=0
		importe2=0
		for vj in rec:
			k+=1						
			if k==1:
				importe_viaje=vj.fc_documento_det.importe
				cantidad=vj.fc_documento_det.cantidad
			else:
				if vj.fc_servicio.codigo=='HRD':					
					cantidad=vj.fc_documento_det.cantidad-1					
					importe2=vj.fc_servicio.tarifa_chofer*cantidad
				elif vj.fc_servicio.codigo=='DEA':					
					cantidad=vj.fc_documento_det.cantidad
					importe2=vj.fc_servicio.tarifa_chofer*cantidad
				elif vj.fc_servicio.codigo=='FER' or vj.fc_servicio.codigo=='ONW' or vj.fc_servicio.codigo=='ENC':				
					cantidad=vj.fc_documento_det.cantidad
					importe2=(vj.fc_servicio.porcentaje_chofer*importe_viaje)/100
			if k==1:				
				importe=importe_viaje
			else:
				importe=importe2
				
			listado.append(TR(A(IMG(_src=URL('static/img','database_delete.png'), _alt="Eliminar", ),	
									_href=URL('delete/'+str(i))  )
									 ,  cantidad,  vj.fc_documento_det.descripcion, importe)) 
			total+=importe
	pie=[]
	pie.append((TD(),TD('Total Pago: '),TD(str(total))))
	#pie.append((TD(),TD(),TD('Total Procesado: '),TD(str(cobrado))))
	#pie.append((TD(),TD(),TD('Diferencia: '),TD(str(total-cobrado))))	
	tabla=TABLE( TR(*header), TR(*listado) , TR(TD(HR(), _colspan=5)), *TR(pie) )	
			#inserto en la union de pagos y viajes para marcar viajes como pagados
			#db.fc_pago_viaje.insert(mv_viaje_id=i, fc_pago_id=idpago)
	#response.flash = 'Viajes y detalle ingresados'
	return dict(   lineas= DIV((tabla))) 

def validarDo2(formdet):
	pass
def validarDo(formdet):
	total=0.00
	cobrado=0.00	
	elid=formdet.vars.fc_pago_id
	montoacobrar=float(formdet.vars.monto)
	rec = db(db.fc_pago.id==elid).select()
	for row in rec:
		total=row.total
	
	rec = db(db.fc_pago_det.fc_pago_id==elid).select()
	for row in rec:
		cobrado+=row.monto
	if  cobrado+montoacobrar > total :
		session.flash = 'Pago excede el total'
		redirect(URL(c='pago',  f='show_form/'+str(elid)+'/True/Detalle'))	


def show_detail(elid):
	header=[]
	header.append(['Accion', 'Fecha','Forma Pago', 'Banco', 'Monto'])
	listado = []    
	for elem in db((db.fc_pago_det.fc_pago_id==elid) & (db.fc_pago_det.fc_forma_pago_id==db.fc_forma_pago.id)  & (db.fc_pago_det.fc_banco_id==db.fc_banco.id) 
	               ).select(orderby=db.fc_pago_det.id):		
		#listado += elem.nombre + "<br/>" 		
		#_onclick="ajax('"+URL('delete/'+str(elem.fc_cobro_det.id)+'/'+str(elid))+"',[''],'target');") 
		listado.append(TR(A(IMG(_src=URL('static/img','database_delete.png'), _alt="Eliminar", ),	
									_href=URL('delete/'+str(elem.fc_pago_det.id)+'/'+str(elid))  )
									 ,  elem.fc_pago_det.fecha,  elem.fc_forma_pago.nombre, elem.fc_banco.nombre[:25], elem.fc_pago_det.monto)) 
	total=0
	cobrado=0
	rec = db(db.fc_pago.id==elid).select()
	for row in rec:
		if row.total:
			total=row.total
	
	rec = db(db.fc_pago_det.fc_pago_id==elid).select()
	for row in rec:
		if row.monto:
			cobrado+=row.monto
	
	pie=[]
	pie.append((TD(),TD(),TD('Total Pago: '),TD(str(total))))
	pie.append((TD(),TD(),TD('Total Procesado: '),TD(str(cobrado))))
	pie.append((TD(),TD(),TD('Diferencia: '),TD(str(total-cobrado))))	
	tabla=TABLE( TR(*header), TR(*listado) , TR(TD(HR(), _colspan=5)), *TR(pie) )	
	return tabla

def show_detail_pago(elid):
	header=[]
	header.append(['Accion', 'Cantidad','Descripcion', 'Importe'])
	listado = []    
	totalimp=0
	for elem in db((db.fc_pago_servicio.fc_pago_id==elid) ).select(orderby=db.fc_pago_servicio.id):		
		#listado += elem.nombre + "<br/>" 		
		#_onclick="ajax('"+URL('delete/'+str(elem.fc_cobro_det.id)+'/'+str(elid))+"',[''],'target');") 
		listado.append(TR(A(IMG(_src=URL('static/img','database_delete.png'), _alt="Eliminar", ),	
									_href=URL('deleteservicio/'+str(elem.id)+'/'+str(elid)  ))
									 ,  elem.cantidad,  elem.descripcion, elem.importe)) 
		totalimp+=elem.importe
		
	pie=[]
	pie.append((TD(),TD('Total a Pagar: '),TD(str(totalimp))))
	tabla=TABLE( TR(*header), TR(*listado) , TR(TD(HR(), _colspan=5)), *TR(pie) )	
	return tabla

def delete():
	 if request.args(0):       
		db(db.fc_cobro_det.id == request.args(0)).delete()
		redirect(URL(c='cobro',  f='show_form/'+request.args(1)+'/True'))

		#return show_detail(request.args(1))

def deleteservicio():
	 if request.args(0):       
		db(db.fc_pago_servicio.id == request.args(0)).delete()
		redirect(URL(c='pago',  f='show_form/'+request.args(1)+'/True/Servicio'))



def imprimir():
	import csv, time
	from gluon.contrib.pyfpdf import Template
	import os.path
	import sys
	es_para_guardar = False
	if request.args(0):
		doc_id=request.args(0)
	if request.args(1):
		es_para_guardar = True 
	doc_record=db(db.fc_documento.id == request.args(0)).select()
	doc_det_rec=db(db.fc_documento_det.fc_documento_id == request.args(0)).select(orderby=db.fc_documento_det.id)
	emp_rec=db(db.cf_empresa.id == 1).select()
	#print emp_rec
	f = Template(format="A4",
             title="Presupuesto", author="w.a",
             subject="w.a", keywords="")	
	if es_para_guardar:
		f.parse_csv(infile=request.folder+'/static/rpt/presupuesto_save.csv', delimiter=";", decimal_sep=",")
	else:
		f.parse_csv(infile=request.folder+'/static/rpt/presupuesto.csv', delimiter=";", decimal_sep=",")

#	 # calculate pages:
	lines = len(doc_det_rec)
	max_lines_per_page = 24
	pages = lines / (max_lines_per_page - 1)
	if lines % (max_lines_per_page - 1): pages = pages + 1
#
#    # fill placeholders for each page
	for page in range(1, pages+1):
		f.add_page()
		f['page'] = 'Page %s of %s' % (page, pages)
		if pages>1 and page<pages:
			s = 'Continues on page %s' % (page+1)
		else:
			s = ''			
# setting data from company
		for row in emp_rec:
			f["EMPRESA"] = row.razon_social
			f["Logo"] = os.path.join(request.env.web2py_path,"applications","flota","uploads",row.ruta_foto) 
			f["membrete1"] = 'Rif.:'+row.rif +'  -   Nit.: '+row.nit
			f["membrete2"] = 'Tel.:'+row.tlf +'  -   Fax.: '+row.fax
			f["iva"] = 'Email.:'+row.email

#data from document
		for row in doc_record:
			f["numero"]	= row.correlativo
			lafecha=row.fecha.strftime("%d/%m/%Y")
			f["Fecha.L"]	= 'Fecha: '+lafecha			
			f["cliente.localidad.l"] = 'Contacto: '
			f["cliente.localidad"] = row.contacto
			lafecha2=row.fecha_vencimiento.strftime("%d/%m/%Y")
			f["cuit"]	= 'Fecha Vencimiento: '+lafecha2
			f["vencimiento"] = ''
			f["vencimientol"] = ''
			f['PeriodoFacturadoL']=''
			f['Periodo.Hasta']=''
			f['Periodo.Desde']=''	
			f['cae']=''
			#f['cae.l']=''	
			f['cae.vencimiento']=''
			f['cae.vencimiento.l']=''	
			f['codigobarras']=str(row.id)+str(row.correlativo)
			f['codigobarraslegible']=str(row.id)+str(row.correlativo)
			f['neto.L']='Sub-Total'	
			f['iva.L']='I.V.A. 12%'	
			notainf=row.nota_detalle
#data from client
			f["cliente.iva.l"] = ''
			f["cliente.cuit.l"] = ''
			clt_rec=db(db.cf_proveedor.id == row.cf_proveedor_id ).select()
			for row in clt_rec:
				f["cliente.nombre"] = row.razon_social
				f["cliente.domicilio"] = row.direccion
				f["cliente.telefono"] = row.tlf + '     Fax: '+row.fax + '        Email: '+row.email				
		# print line item...
		li = 0 
		k = 0
		total = float("0.00")
		for row in doc_det_rec:
			k = k + 1
			if k > page * (max_lines_per_page - 1):
				break
			if row.importe:
				total += float("%.6f" % row.total)
			if k > (page - 1) * (max_lines_per_page - 1):
				li += 1                
				f['item.descripcion%02d' % li] = row.descripcion
				if row.importe is not None:
					f['item.importe%02d' % li] = "%0.2f" % row.total
				if row.cantidad is not None:
					f['item.cantidad%02d' % li] = "%0.2f" % row.cantidad
				
			# ojo para la nota del detalle
			# split detail into each line description
				k=k+2
		if k > (page - 1) * (max_lines_per_page - 1):
			obs="\n<U>Nota:</U>\n\n" + notainf	
			for ds in f.split_multicell(obs,'item.descripcion%02d' % k ):
				for ml in ds.splitlines():
					f['item.descripcion%02d' % k ] = ml
					k=k+1
		
	if pages == page:
			f['neto'] = "%0.2f" % (total)
            #f['vat'] = "%0.2f" % (total*(1-1/float("1.12")))
			f['iva21'] = float("0.00")
			f['total_label'] = 'Total:'
        else:
            f['total_label'] = 'SubTotal:'
        f['total'] = "%0.2f" % total
	
	
	if es_para_guardar:
		f.render("./presupuesto_"+doc_id+".pdf",dest='F')	
		if sys.platform.startswith("linux"):	
			#print os.getcwd()
			os.system("evince ./presupuesto_"+doc_id+".pdf")
		else:
			os.system("./presupuesto_"+doc_id+".pdf")
		redirect(URL(c='presupuesto',  f='email/'+"presupuesto_"+doc_id+".pdf"))	
	else:
		f.render("./presupuesto_"+doc_id+".pdf")	
		if sys.platform.startswith("linux"):	
			#print os.getcwd()
			os.system("evince ./presupuesto_"+doc_id+".pdf")
		else:
			os.system("./presupuesto_"+doc_id+".pdf")
		redirect(URL(c='presupuesto',  f='index'))

def email():	
	if request.args(0):
		documento=request.args(0)
	form = SQLFORM.factory(
	Field('Email_Destinatario', requires=[IS_NOT_EMPTY(), IS_EMAIL() ]),
	Field('Asunto', requires=IS_NOT_EMPTY()), 
	Field('Mensaje', requires=IS_NOT_EMPTY()), 		
		)
	my_extra_element = TR(LABEL('Archivo a adjuntar'), documento, INPUT(_type='hidden',_name='documento',_value=documento ) )		                 
	form[0].insert(-1,my_extra_element)
	
	if form.process().accepted:
		response.flash = 'Mensaje Enviado'
		mail.send(form.vars.Email_Destinatario,
					form.vars.Asunto,
				'<html>'+form.vars.Mensaje+'</html>',
				attachments = Mail.Attachment(form.vars.documento, content_id='documento'))		
	elif form.errors:
		response.flash = 'Ha ocurrido un error'
	return dict(form=form)

def run():
	pass

def error():
    return dict()

