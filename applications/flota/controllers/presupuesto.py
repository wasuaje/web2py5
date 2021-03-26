# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():   
	tabla='fc_documento'
	tabla2='cf_proveedor'
#  	 data = db[tabla].id>0
	data=((db[tabla].cf_proveedor_id==db.cf_proveedor.id) & (db[tabla].fc_tipo_doc_id==1)  &  (db[tabla].status==None))
	#SQLFORM.grid(db.parent,left=db.child.on(db.child.parent=db.parent.id))
	db[tabla].id.readable=False
	fields = [db[tabla].id,  db[tabla].correlativo,  db[tabla].fecha,db[tabla2].razon_social  ]
	head = {}

	links = [{'header':'', \
				'body': lambda row:  A(('Detalle'),   _class='button',   _title=('Manejar el detalle' ),   _href=URL(f='show_form/%s/True' % row['fc_documento'].id) )                                                
												}, 
			{'header':'', \
			'body': lambda row: A(('Encab.'),   _class='button',   _title=('Manejar encabezado' ),   _href=URL(f='show_form/%s' % row['fc_documento'].id) )              
			},               
			]

	def searchform(self,  args):
		form = FORM(INPUT(_name='keywords',_value=request.vars.keywords,
					_id='web2py_keywords'),                        
					INPUT(_type='submit',_value=T('Buscar')),
					INPUT(_type='submit',_value=T('Limpiar'),                       
							_onclick="jQuery('#web2py_keywords').val('');"),
					BR(), A('Agregar', _href=URL(f='show_form')), 
					_method="GET",_action=URL())
		return form           
	# left=(db.cf_proveedor.on(db.cf_proveedor.id==db.fc_documento.cf_proveedor_id))
	grid = SQLFORM.grid(data, fields,  links=links, paginate=20,searchable=True,csv=False, \
					editable=False, details=False, links_in_grid=True,  deletable=False, create=False, \
						search_widget=searchform, headers=head,  maxtextlength=100,  \
						)
	
	return dict(grid=grid)


def show_form():		
	tabla='fc_documento'
	thereistrue =  False		
	funcion=""
	for i in range(0, len(request.args)):
		if request.args(i)=='True':
			thereistrue=True            
			funcion="/select/presupuesto/insert_detail/"+request.args(0)
	if thereistrue ==  True:
		readonly=True
		deletable=False
	else:		
		readonly=False
		deletable=True

	tabladb=db[tabla]
	registro=db[tabla](request.args(0))		

	labels = {'fecha':'Fecha', 'fecha_vencimiento':'Fecha Vencimiento',  'contacto':'Contacto',   'nota_superior':'Nota',  
				'nota_detalle':'Nota Inferior', 'cf_proveedor_id':'Proveedor',  'fc_tipo_doc_id':'Tipo Documento'}
	campos=[ 'cf_proveedor_id',  'fecha',  'fecha_vencimiento', 'contacto', 'nota_superior', 'nota_detalle']			

	form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='presupuesto',  f='index') , \
			fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels, upload=URL('download'))	
	rectipdoc=db(db.fc_tipo_doc.nombre.like('%Presupuesto%')).select()

	for row in rectipdoc:
		form.vars.fc_tipo_doc_id=row.id
		eltipodoc=row.id

	if thereistrue :		
		printform = DIV(TABLE(TR(A('Imprimir', _href=URL('imprimir/'+str(request.args(0)))), 
												A(' - '), 
												A('Enviar por email', _href=URL('imprimir/'+request.args(0)+'/email')), 
												A(' - '), 
												A('Volver', _href=URL('index/'))
													)))
		lineas=show_detail(request.args(0))
	else:
		elform=''
		printform=''
		lineas=''
	if form.accepts(request.vars, session):
		response.flash = 'Operacion exitosa !'
		myid = form.vars.id
		if not request.args(0):			
			newcor=get_correlativo(eltipodoc)
			db((db[tabla].id==myid)).update(correlativo=newcor)
		if form.vars.delete_this_record=="on":
			# me aseguro de borrar el detalle
			db((db["fc_documento_det"].fc_documento_id==myid)).delete()
			redirect(URL(c='presupuesto',  f='index'))
		else:
			redirect(URL(c='presupuesto',  f='show_form/'+str(myid)+'/True'))
	elif form.errors:
		response.flash = 'Ha habido un error !'
	#print get_tarifa(298, 1027, 1)
	return dict( form=form,  printform=printform,  lineas= lineas, funcion=funcion)

def insert_detail():
	#document_id=request.vars.document_id	
	#dscto=float(request.vars.dscto)
	#recargo=float(request.vars.recargo)
	#nota=request.vars.nota
	document_id=request.args(0)
	servicio_id=request.args(1)    
	if request.args(2):
		base=float(request.args(2))
	if request.args(3):
		cantidad=float(request.args(3))
	else:
		cantidad=1.0
	#busco data del viaje    
	# busco con data del el viaje en la tarifa para armar descripcion e importe
	taridata=get_tarifa_from_id(servicio_id)	
	#print taridata, servicio_id
	nota=''
	total=0.00	
	dscto=0.00	
	recargo=0.00	
	if taridata:		
		for row in taridata:
			if 'fc_servicio' in row:		#si es un viaje tiene j oin a vehiculo_tipo				
				importe=row.fc_servicio.tarifa_cobro
				veh=row.cf_vehiculo_tipo.nombre
				dc=row.fc_servicio.descripcion				
				#print dc,  veh
				desc='Servicio de transporte: %s en vehiculo tipo %s' %  (dc, veh)
			else:		#es un servicio con porcentaje o bsf
				if row.porcentaje>0:
					#print type(base), type(row.porcentaje)
					desc= row.descripcion+"a razon de %s x %s"  %  (base, row.porcentaje) +"%"
					importe = base * (row.porcentaje/100)
				elif row.tarifa_cobro>0:
					desc= row.descripcion+"a razon de %s Bsf c/u" % row.tarifa_cobro
					importe = row.tarifa_cobro                                    				
		idser=servicio_id
		total=importe-(importe*(dscto/100))+(importe*(recargo/100))
		total = cantidad * total
		inserted=db.fc_documento_det.insert(fc_documento_id=document_id, descuento=dscto,  \
					importe=importe, cantidad=cantidad, recargo=recargo, nota=nota, total=total, descripcion=desc, \
					fc_servicio_id=idser)		
		# con el importe hago cant=1, y calculo el total restandole dscto y sum recargo
	if inserted and inserted > 0:        
		#db.fc_documento_detalle.insert(name="Alex")					
		#return show_detail(document_id)			
		redirect(URL(c='presupuesto',  f='show_form/'+document_id+'/True'))
		response.flash = 'Detalle Agregado'		
	else:
		return DIV(B('No se pudo insertar !'))

def show_detail(elid):
    header=[]
    header.append(['Accion','Cant.',  'Descripcion','Importe'])	
    listado = []    
    total=0
    funcion="/select/presupuesto/insert_detail/"+request.args(0)
    for elem in db(db.fc_documento_det.fc_documento_id==elid).select(orderby=db.fc_documento_det.id):		
        #listado += elem.nombre + "<br/>" 
        listado.append(BR())
        listado.append(TR((A(IMG(_src=URL('static/img','delete.png'), _alt="Eliminar",), 
                                          _onclick="if(confirm('Seguro de Eliminar?')) ajax('"+URL('delete/'+str(elem.id)+'/'+str(elid))+"',[''],'target');" , _title="Eliminar Detalle"), 
                                        A(IMG(_src=URL('static/img','money_add.png'), _alt="Eliminar",), 
                                          _onclick="window.open('"+URL(c='servicio', f='index'+funcion+"/"+str(elem.total))+"'+'/'+$('#cant').val(), 'Tarifas y Servicios','width=600,height=500,scrollbars=yes') ; "  ,  _title="Tomar este importe como base para calcular el siguiente detalle a insertar")), 
								SPAN(elem.cantidad,_style='margin-left:0.5%'), 
								SPAN(elem.descripcion,_style='margin-left:0.5%'), 
								SPAN(elem.total,_style='margin-left:0.5%')
                                ))
                                #if(confirm('Tomar como base de calculo?'))
           
        total+=elem.total

    lineas = DIV(listado)
    pie=[]
    pie.append((TD(), TD('Total Presupuesto: '),TD(str(total))))
    #print lineas
    lineas=TABLE( TR(*header), TR(*listado) , TR(TD(HR(), _colspan=4)), *TR(pie) )		
    return lineas

def delete():
    if request.args(0):       
        db(db.fc_documento_det.id == request.args(0)).delete()
        return show_detail(request.args(1))

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
	f = Template(format="A4",     title="Presupuesto", author="w.a",             subject="w.a", keywords="")	
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
	Field('Mensaje', requires=IS_NOT_EMPTY()), )
	my_extra_element = TR(LABEL('Archivo a adjuntar'), documento, INPUT(_type='hidden',_name='documento',_value=documento ) )		                 
	form[0].insert(-1,my_extra_element)

	if form.process().accepted:
		response.flash = 'Mensaje Enviado'
		mail.send(form.vars.Email_Destinatario,		form.vars.Asunto,				'<html>'+form.vars.Mensaje+'</html>',
			attachments = Mail.Attachment(form.vars.documento, content_id='documento'))		
	elif form.errors:
		response.flash = 'Ha ocurrido un error'
	return dict(form=form)

def run():
	pass

def error():
	return dict()	
