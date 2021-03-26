# -*- coding: utf-8 -*-
### required - do no delete

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():   
    tabla='fc_tipo_doc'
    data = db[tabla].id>0
    fields = [db[tabla].nombre, db[tabla].correlativo, db[tabla].naturaleza ]
    db[tabla].id.readable=False
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

    grid = SQLFORM.grid(data, fields,  links=links, paginate=20,searchable=True,csv=False, \
                        editable=False, details=False, links_in_grid=True,  deletable=False, create=False, search_widget=searchform )
        
    return dict(grid=grid)

def show_form():		
	tabla='fc_tipo_doc'
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
	
	labels = {'nombre':'Nombre', 'naturaleza':'Naturaleza', 'correlativo':'Correlativo' }
	campos=['nombre','naturaleza', 'correlativo'	]			
			
	form=SQLFORM(tabladb, registro, submit_button='Enviar' ,    delete_label='Click para borrar:', next=URL(c='cliente',  f='index') , \
		              	fields=campos ,showid=False , deletable=deletable ,  readonly=readonly , labels=labels, upload=URL('download'))

	if form.accepts(request.vars, session):
		response.flash = 'Operacion exitosa !'
		redirect(URL(c='tipodoc',  f='index'))
	elif form.errors:
		response.flash = 'Ha habido un error !'

	return dict( form=form)

def run():
	pass

def error():
    return dict()

