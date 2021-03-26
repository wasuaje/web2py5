# -*- coding: utf-8 -*-
### required - do no delete

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():   
	tabla='fc_documento'
	tabla2='cf_proveedor'
	data=((db[tabla].cf_proveedor_id==db.cf_proveedor.id) & (db[tabla].fc_tipo_doc_id==1)  &  (db[tabla].status==None))	
	db[tabla].id.readable=False
	fields = [db[tabla].id,  db[tabla].correlativo,  db[tabla].fecha,db[tabla2].razon_social  ]
	head = {}
	ctrl='presupuesto'
	fnc='show_form'
	links = [{'header':'', \
				'body': lambda row:  A(('Facturar'),   _class='button',   _title=('Facturar presupuesto' ),   _href="javascript: if(confirm('Seguro de Facturar?')) document.location.href='"+URL(f='run/%s' % row['fc_documento'].id)+"'" )                                                
												}, 
			{'header':'', \
			'body': lambda row:  A(IMG(_src=URL('static/img','magnifier.png'), _alt="Eliminar",), 
                                          _onclick="window.open('"+URL(c=ctrl, f=fnc+'/'+str(row['fc_documento'].id))+'/True'+"'" + ", 'Tarifas y Servicios','width=600,height=700,scrollbars=yes') ; "  ,  _title="Mostrar detalle de este presupuesto")             
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




def index_old():
	tabla='fc_documento'
	tabladata=	db((db[tabla].cf_proveedor_id==db.cf_proveedor.id) & (db[tabla].fc_tipo_doc_id==1)  &  (db[tabla].status==None) ).select()	
	
	lista=[]
	
	for row in tabladata:
		lista.append(A('Facturar', _href=URL('run/'+str(row.fc_documento.id))))
		lista.append(' - ')
		lista.append(row.fc_documento.correlativo)
		lista.append(' - ')
		lista.append(row.cf_proveedor.razon_social)
		lista.append(BR())
	
	if len(tabladata):
		lista=DIV(lista)	
	else:
		lista.append(B(' No hay prespuestos por facturar'))
		lista=DIV(lista)	
	return dict(lista=lista)

def run():	
	tabla='fc_documento'
	tbldet='fc_documento_det'
	rec_ori=request.args(0)	
	document_id= rec_ori
	inserted=desde=hasta=tipoveh=0
	
	#duplico el master con el nuevo correlativo y tipo de documento de prespuesto a factura
	myrecord = db.fc_documento[int(rec_ori)]						
	newrec = db.fc_documento.insert(**db.fc_documento._filter_fields(myrecord)) 
	newcor=get_correlativo(2)
	inserted=db(db.fc_documento.id==newrec).update(correlativo=newcor,  fc_tipo_doc_id = 2)	

	#duplico el detalle
	#myrecord = db.fc_documento_det(fc_docuemento_idint(rec_ori)).select()
	ids=[]
	myrecord = db(db.fc_documento_det.fc_documento_id==int(rec_ori)).select()
	for i in myrecord:
		ids.append(i['id'])
		new = db.fc_documento_det.insert(**db.fc_documento_det._filter_fields(i)) 
		inserted=db((db.fc_documento_det.id==new)  ).update(fc_documento_id=newrec)	
	
	if inserted:
		#marco el presupuesto como facturado
		db(db.fc_documento.id==rec_ori).update(status=0)
		
		response.flash = 'Facturado Exitosamente'
		redirect(URL(c='facturar',  f='index'))
	return dict(lista=lista, listadet=listadet ,  form=form )
			
			
