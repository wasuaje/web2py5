# -*- coding: utf-8 -*-
### required - do no delete
import math 
import json

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
	set_sessions()		
	row=db((db.in_categoria.id >0) & (db.in_categoria.show_in_menu == True) ).select()
	first=db((db.in_categoria.id >0) & (db.in_categoria.show_in_menu == True) ).select().first()	
	firstid=first.id
	mydiv=[]
	for rw in row:		
		mydiv.append(DIV(A(IMG(_src=URL('download/%s' % rw.ruta_foto),  _width="80", _height="80", _class="none"),
										callback=URL('pos','get_productos', vars={'id_cat':rw.id} ), target="prods"), CENTER(P(B(rw.nombre))) , _class="imgmed"))

		mydiv2=XML("".join(["%s" % (k) for k in mydiv]))

	return dict(cats=mydiv2, prods=get_productos2(firstid), tools=tools(), prb=mydiv2)

def set_sessions():
	session.pos = session.pos or {}
	session.mesa = session.mesa or {}
	session.cliente = session.cliente or {}
	
	if 'id' not in session.mesa.keys() :
		session.mesa['id']=1
		session.mesa['codigo']='00'
	
	if 'id' not in session.cliente.keys() :
		session.cliente['id']=0
		session.cliente['codigo']='00'
	
	orden_cnt=db((db.fc_orden.mesa_id == session.mesa['id']) & (db.fc_orden.closed == False) )
	orden_cnt=orden_cnt.count()
	
	if orden_cnt>0:
		orden=db((db.fc_orden.mesa_id == session.mesa['id']) & (db.fc_orden.closed == False) ).select().first()
		session.mesa['orden_id']=orden.id
	else:
		session.mesa['orden_id']=0

def error():
    return dict()

def tools():
	mydiv=[]	
	mydiv.append(DIV(H1(T("Opciones")), _class="title"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','letra_a.jpeg'), _alt="Acciones con tickets",  _width="60", _height="60", _class="none"), callback=URL('pos','ticket'), target='tools')
							, CENTER(P(B("Ticket"))), _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','mesas.jpeg'), _alt="Seleccionas mesas",  _width="60", _height="60", _class="none"), callback=URL('pos','get_mesas'), target='tools')
							, CENTER(P(B("Mesas"))), _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','meseros.jpeg'), _alt="Otras acciones",  _width="60", _height="60", _class="none"), _href=URL('configserv','index'))
							, CENTER(P(B("Varios"))), _class="imgmed"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','flecha.jpeg'), _alt="Sale al menu principal",  _width="60", _height="60", _class="none"),  _href=URL('default','index'))
							, CENTER(P(B("Salir"))), _class="imgmed"))
	
	mydiv2=XML("".join(["%s" % (k) for k in mydiv]))
	return mydiv2
	
def ticket():
	mydiv=[]	
	mydiv.append(DIV(A(IMG(_src=URL('static/images','agregar.jpg'), _alt="Punto de venta, POS",  _width="40", _height="40", _class="none"),
										callback=URL('pos','ticket_nuevo'), target="ticket"), CENTER(P(B("Nuevo"))) , _class="imgsmall"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','papeleras.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="40", _height="40", _class="none"),
										_href=URL('configserv','index')), CENTER(P(B("Borrar"))) , _class="imgsmall"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','imprimir.jpg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="40", _height="40", _class="none"),
										_href=URL('configserv','index')), CENTER(P(B("Facturar"))) , _class="imgsmall"))
	mydiv.append(DIV(A(IMG(_src=URL('static/images','buscar.jpeg'), _alt="categorias, productos, ingredientes, combos, etc.",  _width="40", _height="40", _class="none"),
										_href=URL('configserv','index')), CENTER(P(B("Buscar"))) , _class="imgsmall"))									
	mydiv.append(DIV(A(IMG(_src=URL('static/images','flecha.jpeg'), _alt="Volver al inicio",  _width="40", _height="40", _class="none"),
	                                      callback=URL('pos','tools'), target="tools"), CENTER(P(B("Volver"))) , _class="imgsmall"))
	
	mydiv2=DIV(DIV(H1(T("Acciones con tickets")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])))
	
	return dict(mydiv=mydiv2)


def get_productos():
	id_cat=request.vars.id_cat
	row=db((db.in_producto.id >0) & (db.in_producto.categoria_id==id_cat) ).select()
	mydiv=[]
	for rw in row:		
		mydiv.append(DIV(A(IMG(_src=URL('download/%s' % rw.ruta_foto),  _width="80", _height="80", _class="none"),
										callback=URL('pos','handle_items', vars={'id_prod':rw.id, 'action':'Add' } ), target="tots" ) , CENTER(P(B(rw.nombre))) , _class="imgmed"))

		mydiv2=XML("".join(["%s" % (k) for k in mydiv]))
	
	return dict(prods=mydiv2)

def get_productos2(id_cat):
	row=db((db.in_producto.id >0) & (db.in_producto.categoria_id==id_cat) ).select()
	mydiv=[]
	for rw in row:		
		mydiv.append(DIV(A(IMG(_src=URL('download/%s' % rw.ruta_foto),  _width="80", _height="80", _class="none"),
										callback=URL('pos','handle_items', vars={'id_prod':rw.id, 'action':'Add'} ), target="tots" ) , CENTER(P(B(rw.nombre))) , _class="imgmed"))


		mydiv2=XML("".join(["%s" % (k) for k in mydiv]))
	
	return mydiv2

def get_mesas():		
	row=db(db.cf_mesa.id >0 ).select()
	mydiv=[]
	for rw in row:
		if rw.ruta_foto<>"":
			foto=URL('download/%s' % rw.foto)
		else:
			foto=''
		#mydiv.append(DIV(A(IMG(_src=foto,   _width="40", _height="40", _class="none"),
		#								callback=URL('pos','select_mesa', vars={'id_mesa':rw.id} ), target="tots" ) , CENTER(P(B(rw.codigo))) , _class="imgsmall", 
		#								_onclick="jQuery.ajax("+URL('pos','select_mesa', vars={'id_mesa':rw.id})+");" ) )
		#mydiv.append(DIV( CENTER(H1(B(rw.codigo))) , _onclick="jQuery.ajax('"+URL('pos','select_mesa', vars={'id_mesa':rw.id, 'cod_mesa':rw.codigo})+"');  setTimeout(function(){ window.location.reload()}, 500);;" 
		 #                                                                                                    , _class='imgsmall' ) )
		 
		mydiv.append(DIV(A(H1(rw.codigo) ,  callback=URL('pos','select_mesa',  vars={'id_mesa':rw.id, 'cod_mesa':rw.codigo} ), target="mesa" ) ,  _class="imgsmallbrd"))
	
	mydiv2=DIV(DIV(H1(T("Seleccione mesa")), _class="title"),XML("".join(["%s" % (k) for k in mydiv])))
	
	return dict(mesas=mydiv2)

def select_mesa():
	mesa=request.vars.id_mesa
	cod_mesa=request.vars.cod_mesa
	session.mesa['id']=mesa
	session.mesa['codigo']=cod_mesa	
	scr="""			
			$("#list10").trigger("reloadGrid"); 			
			updateGridTotals();
			showTools();
			"""
	mes=CENTER(H1(cod_mesa), SCRIPT(scr))
	set_sessions()	#antes de actualizar la pagina me aseguro que esten las nuevas variables de session seteadas
	return mes

def grid_totals():	
	orden_id=session.mesa['orden_id']		
	rec=db(db.fc_orden_det.orden_id == orden_id ).select()
	subtotal=0	
	tiva=0
	ttotal=0
	ttiva=0
	for row in rec:
		subtotal+=row.importe
		tiva+=row.importe*(row.iva/100)
		ttotal+=row.total
		ttiva=row.iva
	#mando a ejecutar este script para actualizar el grid
	
	mydiv2=DIV(TABLE(TR(TD(H2('Sub Total :'),  _width='350', _align='right'), 
										TD(H2("{:10,.2f}".format(subtotal) ) ,  _width='100') , _align='right') , 
										TR(TD(H2('I.V.A. ('+str(ttiva)+')' ,  _width='350', _align='right')), 
										TD(H2("{:10,.2f}".format(tiva) ) , _width='100') , _align='right') , 
										TR(TD(H2('Total :'),  _width='350', _align='right'), 
										TD(H2("{:10,.2f}".format(ttotal) ) ,  _width='100') , _align='right') 
									, _border='0', _width='430'))

	return mydiv2				

def handle_items():
	id_prod=request.vars.id_prod or 0
	action=request.vars.action
	laorden=session.mesa['orden_id']
	ordendet=request.vars.id_orden_det or 0
	if action=='Add':
		first=db(db.in_producto.id == id_prod ).select().first()	
		importe=first.importe
		iva=first.iva
		imp1=first.imp1
		imp2=first.imp2
		descuento=first.descuento
		total=importe+(importe*(iva/100))+(importe*(imp1/100))+(importe*(imp2/100))-(importe*(descuento/100))
		if laorden>0:
			orden_id=laorden
		else:
			orden_id=db.fc_orden.insert(cliente_id=session.cliente['id'],mesa_id=session.mesa['id'])
			session.mesa['orden_id']=orden_id
		if orden_id > 0:
			orden_det_id=db.fc_orden_det.insert(orden_id=orden_id, producto_id=id_prod, cantidad=1, importe=importe, iva=iva, imp1=imp1, imp2=imp2, descuento=descuento, total=total)		
		else:
			response.flash = 'no se pudo insertar'
	elif action=='Delete' :
		id_orden_det=ordendet
		db(db.fc_orden_det.id==ordendet).delete()
		db.commit()
	
	#print "orden", laorden
	orden_id=laorden
	#para los totals
	#"{:10,.2f}".format(total)
	rec=db(db.fc_orden_det.orden_id == orden_id ).select()
	subtotal=0	
	tiva=0
	ttotal=0
	ttiva=0
	for row in rec:
		subtotal+=row.importe
		tiva+=row.importe*(row.iva/100)
		ttotal+=row.total
		ttiva=row.iva
	
	#mando a ejecutar este script para actualizar el grid	
	scr="""			
			$("#list10").trigger("reloadGrid"); 			
			updateGridTotals();
			""" 
	mydiv2=DIV(TABLE(TR(TD(H2('Sub Total :'),  _width='350', _align='right'), 
										TD(H2("{:10,.2f}".format(subtotal) ) ,  _width='100') , _align='right') , 
										TR(TD(H2('I.V.A. ('+str(ttiva)+')' ,  _width='350', _align='right')), 
										TD(H2("{:10,.2f}".format(tiva) ) , _width='100') , _align='right') , 
										TR(TD(H2('Total :'),  _width='350', _align='right'), 
										TD(H2("{:10,.2f}".format(ttotal) ) ,  _width='100') , _align='right') 
									, _border='0', _width='430'),  SCRIPT(scr))	
	return dict(prb=mydiv2)

			

def get_ticket_data():
	tabla='fc_orden_det'
	if 'orden_id' in session.mesa.keys():
		orden= session.mesa['orden_id']
	else:
		orden=0
	searching=False
	page = request.vars.page #// get the requested page 
	limit = request.vars.rows  #// get how many rows we want to have into the grid 
	limitini = int(request.vars.rows) #// get how many rows we want to have into the grid 
	sidx =  request.vars.sidx #// get index row - i.e. user click to sort $sord = 
	sord =  request.vars.sord  #// get the direction
	if request.vars.searchField:
		searching=True
		searchopt=request.vars.searchOper
		searchfield=request.vars.searchField
		searchstring=request.vars.searchString		
		searchquery=search(tabla, searchopt, searchfield,searchstring )
		
	if not page:
		page = 1
	else:
		page=int(page)
		
	if not limit:
		limit = 10
	else:		
		limit=int(limit)
		
	if not sidx:
		sidx =1 # // connect to the database 

	count =db(db[tabla].id > 0).count() 
	if  count > 0:
		total_pages = int(math.ceil(float(count)/float(limit)))
	else:		
		total_pages = 0
		
	#print total_pages	
	
	if page >= total_pages:		
		page=total_pages
		limit=count		
		start = limitini*page - limitini # // do not put $limit*($page - 1)		
	else:		
		limit=limit*page
		#start = limit*page - limit # // do not put $limit*($page - 1)
		start = limit-limitini # // do not put $limit*($page - 1)
	if limit < 0 :		
		limit = 0		
	
	if start < 0  :
		start = 0;	
	
	resp={}
	resp={'page':page,'total':total_pages,'records':count,'rows':[]}
		
	if searching:
		query=db( (eval(searchquery)) & (db.fc_orden_det.orden_id==orden)   & (db.fc_orden_det.producto_id==db.in_producto.id)  ).select()
	else:				
		query=db((db.fc_orden_det.orden_id==orden)  & (db.fc_orden_det.producto_id==db.in_producto.id) ).select( limitby=( start, limit) )	
	
	for row in  query:
		rw={}
		rw['id']=row.fc_orden_det.id
		rw['cell']=[row.fc_orden_det.id,row.in_producto.codigo,row.in_producto.nombre,row.fc_orden_det.cantidad, row.fc_orden_det.importe, row.fc_orden_det.total]
		resp['rows'].append(rw)

	data=json.dumps(resp)	
	return data

def ticket_nuevo():
	
	mydiv=[]
	ticket=""
	ticket+="SENIAT <br>"
	ticket+="Factura Nro. 94849 <br>"
	ticket+="=======================<br>"
	ticket+="Item. Cant. Unt. Total<br>"
	ticket+="=======================<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="PEPSI   1  12.00  12.00<br>"
	ticket+="=======================<br>"
	ticket+="Total          1.250.00<br>"
	mydiv.append(ticket)
	mydiv=DIV(DIV(H1(T("Tickect Actual")), _class="title"),DIV(XML(ticket), _class="entry"))
	return dict(myticket=mydiv)

	
