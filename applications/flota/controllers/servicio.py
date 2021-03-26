# -*- coding: utf-8 -*-
### required - do no delete

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():   
	tabla='fc_servicio'
	data = db[tabla].id>0
	fields = [db[tabla].codigo, db[tabla].descripcion,  db[tabla].tarifa_cobro,  db[tabla].tarifa_chofer,   db[tabla].porcentaje,  db[tabla].porcentaje_chofer,db[tabla].is_viaje]
	head = {tabla+'.descripcion':'Descripcion', tabla+'.tarifa_cobro':'Cobro Bsf',
				tabla+'.tarifa_chofer':'Pago Bsf.',  tabla+'.porcentaje':'% Cobro', tabla+'.porcentaje_chofer':'% Pago'}
	db[tabla].id.readable=False
	db[tabla].is_viaje.readable=False
	if request.args(0) and request.args(0) == 'select':
		ctrl=request.args(1) 
		if request.args(4):
			base=request.args(4) 
		else:
			base=0
		if request.args(5):
			cantidad=request.args(5) 
		fnc=request.args(2) +"/"+request.args(3) 
		links = [{'header':'', \
				'body': lambda row:   A(('Insertar'),   _class='button',   _title=('Insertar registro' ),   \
                                        _href= "javascript: window.opener.document.location=\""+URL(c=ctrl, f=fnc)+"/"+str(row.id)+"/"+str(base)+"/"+str(cantidad)+"\"; window.close();" )                                                
													}]
	else:        
		links = [{'header':'', \
                'body': lambda row:  (row.is_viaje)  and \
                                                A(('Ver'),   _class='button',   _title=('Ver registro' ),   _href=URL(f='show_form/%s/True' % row.id) )
                                                or \
                                                    A(('Ver'),   _class='button',   _title=('Ver registro' ),_href=URL(f='show_form/%s/True/Servicio' % row.id)) 
                                                    }, 
              {'header':'', \
                'body': lambda row:  (row.is_viaje)  and \
                                                A(('Editar'),   _class='button',   _title=('Ver registro' ),   _href=URL(f='show_form/%s' % row.id) )
                                                or \
                                                    A(('Editar'),   _class='button',   _title=('Ver registro' ),_href=URL(f='show_form/%s/Servicio' % row.id))                                                     
              },               
               ]
	
	def searchform(self,  args):
		form = FORM(INPUT(_name='keywords',_value=request.vars.keywords,
                              _id='web2py_keywords'),                        
                        INPUT(_type='submit',_value=T('Buscar')),
                        INPUT(_type='submit',_value=T('Limpiar'),                       
                              _onclick="jQuery('#web2py_keywords').val('');"),
                        BR(), A('Agregar Viaje', _href=URL(f='show_form')), ' - ', 
                                 A('Agregar Servicio', _href=URL(f='show_form/Servicio')), 
						_method="GET",_action=URL())
		return form           

	grid = SQLFORM.grid(data, fields,  links=links, paginate=20,searchable=True,csv=False, \
                        editable=False, details=False, links_in_grid=True,  deletable=False, create=False, \
                        search_widget=searchform, headers=head,  maxtextlength=100 )
        
	return dict(grid=grid)

def show_form():		
    tabla='fc_servicio'
    thereistrue =  False
    thereisservicio = False			
    for i in range(0, len(request.args)):
        if request.args(i)=='True':			
            thereistrue=True
        if request.args(i)=='Servicio':
            thereisservicio=True
    if thereistrue ==  True:
        readonly=True
        deletable=False
    else:		
        readonly=False
        deletable=True
    
    tabladb=db[tabla]
    registro=db[tabla](request.args(0))
    labels = {'descripcion':'Descripcion', 'codigo':'Codigo',  'tarifa_cobro':'Tarifa a  Cobrar',  'tarifa_chofer':'Tarifa a pagar',   
                'porcentaje':'(%) Cobro', 'porcentaje_chofer':'(%) Pago'  ,	'distancia':'Distancia', 'mt_ciudad_desde':'Origen',   \
                'mt_ciudad_hasta':'Destino','cf_proveedor_id':'Proveedor',  'cf_vehiculo_tipo_id':'Tipo de Vehiculo', \
                }

    if not thereisservicio:		
        campos=['mt_ciudad_desde', 'mt_ciudad_hasta', 'cf_vehiculo_tipo_id', 'descripcion', 'tarifa_cobro', 'tarifa_chofer',  \
          'distancia']
    else:
        campos=['codigo', 'descripcion', 'tarifa_cobro', 'tarifa_chofer','porcentaje' , 'porcentaje_chofer']
    
    form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='servicio',  f='index') , \
                 fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels, upload=URL('download'))

    if form.accepts(request.vars, session):
        response.flash = 'Operacion exitosa !'
        redirect(URL(c='servicio',  f='index'))
    elif form.errors:
        response.flash = 'Ha habido un error !'
    
    return dict( form=form)

def run():
	pass

def error():
    return dict()

def index_old():
	#muestro form de busqueda de gastos
	tabla='fc_servicio'
	header=[]
	data=[]
	registro=db(db[tabla].id>0).select(orderby=db[tabla].codigo)
	header.append(TR(B('Accion'), B('Descripcion'), B('Tarifa al cobro'),  B('Tarifa al pago')))
	for row in registro:
		if row.mt_ciudad_desde and row.mt_ciudad_hasta and row.cf_vehiculo_tipo_id:
			add_link=A('Ver  ',  _href=URL('show_form/'+str(row.id)+'/True'))
			edit_link=A('Edit ',  _href=URL('show_form/')+str(row.id))
		else:
			add_link=A('Ver  ',  _href=URL('show_form/'+str(row.id)+'/True/Servicio'))
			edit_link=A('Edit ',  _href=URL('show_form/')+str(row.id)+'/Servicio')
		data.append(TR( [add_link, '- ', edit_link], row.descripcion, row.tarifa_cobro, row.tarifa_chofer))
	
	nuevo_link=A('Nuevo Viaje ',  _href=URL('show_form'))
	nuevo_link_ser=A('Nuevo Servicio ',  _href=URL('show_form/Servicio'))
	tabla=DIV(TABLE(TR(header), TR(data), TR([nuevo_link,  nuevo_link_ser])))
	return dict(tabla=tabla)
