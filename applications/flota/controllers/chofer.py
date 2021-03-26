# -*- coding: utf-8 -*-
### required - do no delete

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

def index():   
    tabla='mt_persona'
    a = db.mt_persona.id>0
    fields = [db.mt_persona.id, db.mt_persona.cedula,  db.mt_persona.nombres, db.mt_persona.apellidos]
    db.mt_persona.id.readable=False
    links = [{'header':'', \
              'body': lambda row: A(('Ver'),   _class='button', 
              _title=('Ver registro' ),  _href=URL(f='show_form/%s/True' % row.id))}, 
              {'header':'', \
              'body': lambda row: A(('Editar'),   _class='button', 
              _title=('Editar registro' ),  _href=URL(f='show_form/%s' % row.id))},               
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

    grid = SQLFORM.grid(a, fields,  links=links, paginate=20,searchable=True,csv=False, \
                        editable=False, details=False, links_in_grid=True,  deletable=False, create=False, search_widget=searchform )
        
    return dict(grid=grid)


def show_form():		
	tabla='mt_persona'
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
	
	labels = {'nombres':'Nombres', 'apellidos':'Apellidos',  'direccion':'Direccion',   'cedula':'Cedula',   'email':'E-mail'  ,
	'tlf_hab':'Tlf. Hab', 'tlf_cel':'Tlf. Cel',  'ruta_foto':'Imagen',  'cf_cargo_id':'Cargo'}
	campos=['cedula', 'nombres', 'apellidos', 'sexo', 'tlf_hab', 'tlf_cel', 'email', 'direccion','ruta_foto','cf_cargo_id']			
			
	form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='cliente',  f='index') , \
		              	fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels, upload=URL('download'))

	if form.accepts(request.vars, session):
		response.flash = 'Operacion exitosa !'
		redirect(URL(c='chofer',  f='index'))
	elif form.errors:
		response.flash = 'Ha habido un error !'

	return dict( form=form)

def run():
	pass

def error():
    return dict()

def index_old():
	#muestro form de busqueda de gastos
	tabla='mt_persona'
	grid = webgrid.WebGrid(crud)
	grid.fields = [tabla+'.cedula', tabla+'.nombres', tabla+'.apellidos']
	grid.field_headers = ['Cedula', 'Nombres',  'Apellidos']
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
