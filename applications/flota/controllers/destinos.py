def index():    
	lista = db(db.cf_viaje_tipo).select()   
	return dict(lista=lista)

def lista():
	listado = []
	if request.vars.q:            
		db.cf_viaje_tipo.insert(nombre = request.vars.q)      	
	return genera_lista()
	  
def delete():
       if request.args(0):       
            db(db.cf_viaje_tipo.id == request.args(0)).delete()
       return genera_lista()

def genera_lista():
	listado = []    
	for elem in db(db.cf_viaje_tipo).select():
		#listado += elem.nombre + "<br/>" 
		listado.append(BR())
		listado.append(A(IMG(_src=URL('static/img','database_delete.png'), _alt="Eliminar",
								 ),  _onclick="ajax('"+URL('delete/'+str(elem.id))+"',[''],'target');") )
		listado.append(INPUT(_type='checkbox',_name='hijos',_value=elem.id))
		listado.append(SPAN(elem.nombre,_style='margin-left:0.5%'))         
 
	lista = DIV(listado)
	#lista = db(db.cf_viaje_tipo).select()   
	return lista	
