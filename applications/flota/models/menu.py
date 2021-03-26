# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html

response.meta.author = 'Wuelfhis Asuaje'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2012'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Inicio'), False, URL('default','index'), [])
    ]

##########################################
## this is here to provide shortcuts
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################

#########################################
## Make your own menus
##########################################

response.menu+=[
    (T('Configuracion'), False, URL( 'default', 'index'),
     [
            (T('Tablas'), False,
             URL('tablas','index')),
            (T('Maestros'), False,
             URL('maestros','index')),
#			(T('Movimientos'), False,
#            URL('movimientos','index')),
#            (T('Control Gastos'), False,
   #          URL('gastos','index')),
           
            ]
   )]

response.menu+=[                
    (T('Gastos'), False,  URL( 'default', 'index'),
     [
	         (T('Choferes'), False,
             URL('chofer','index')),
            (T('Vehiculos'), False,
             URL('vehiculo','index')),			             
            (T('Solicitud de Viajes'), False,
             URL('viaje','index')),
			(T('Asignacion de Viajes'), False,
             URL('asignacion','index')),
                     
            ]
   )]



   
response.menu+=[                
    (T('Traslados'), False,  URL( 'default', 'index'),
     [
	         (T('Choferes'), False,
             URL('chofer','index')),
            (T('Vehiculos'), False,
             URL('vehiculo','index')),			             
            (T('Solicitud de Viajes'), False,
             URL('viaje','index')),
			(T('Asignacion de Viajes'), False,
             URL('asignacion','index')),
                     
            ]
   )]


response.menu+=[
    (T('Facturacion'), False, URL('admin', 'default', 'design/%s' % request.application),
     [
            (T('Tipos de documento'), False,
             URL('tipodoc','index')),
            (T('Bancos'), False,
             URL('banco','index')),
			(T('Formas de pago'), False,
			URL('formapago','index')),
			(T('Tarifas por servicios'), False,
			URL('servicio','index')),
			(T('Presupuestos'), False,
             URL('presupuesto','index')),
			 (T('Facturar Presupuestos'), False,
             URL('facturar','index')),
			 (T('Facturas'), False,
             URL('factura','index')),
            (T('Cobros'), False,
             URL('cobro','index')),
            (T('Pagos'), False,
             URL('pago','index')),
            ]
   )]


##########################################
## this is here to provide shortcuts to some resources
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################


response.menu+=[
	(T('Reportes'), False,URL('reportes','index'),
     [
        (T('Configuracion'), False,URL('reportes','configs')),
        (T('Maestros'), False,URL('reportes','maestros')),
		(T('Presupuestos'), False, URL('index'), 
			[
			(T('Todos los presupestos'), False, URL('reportes','presupuestos/todos')), 
			]), 
		(T('Facturacion'), False, URL('index'), 
			[
			(T('Cuentas por cobrar'), False, URL('reportes','porcobrar/todos')), 
			]), 
        (T('Movimientos'), False,URL('reportes','movitos')),
        (T('Gastos'), False,URL('reportes','gastos')),
        
   ])]
