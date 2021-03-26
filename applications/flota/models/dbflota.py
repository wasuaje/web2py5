legacy_db = DAL('mysql://root:www4214@localhost/dbflota')

legacy_db.define_table('cf_asignacion_tipo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_aviso',
    Field('id','integer'),
    Field('mensaje','string'),
    Field('kilometraje','integer'),
    Field('dias','integer'),
    Field('cf_item_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('cf_cargo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_empresa',
    Field('id','integer'),
    Field('nombre','string'),
    Field('razon_social','string'),
    Field('direccion','string'),
    Field('rif','string'),
    Field('nit','string'),
    Field('email','string'),
    Field('tlf','string'),
    Field('fax','string'),
    Field('ruta_foto','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_item',
    Field('id','integer'),
    Field('nombre','string'),
    Field('cf_item_grupo_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('cf_item_grupo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_localidad',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_solicitud_tipo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_tipo_combustible',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_tipo_doc',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_vehiculo_marca',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('cf_vehiculo_modelo',
    Field('id','integer'),
    Field('nombre','string'),
    Field('cf_vehiculo_marca_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('cf_vehiculo_tipo',
    Field('id','integer'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('mt_ciudad',
    Field('id','integer'),
    Field('codigo','string'),
    Field('nombre','string'),
    Field('mt_estado_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mt_doc_persona',
    Field('id','integer'),
    Field('fecha_emision','date'),
    Field('fecha_vencimiento','date'),
    Field('numero','string'),
    Field('cf_tipo_doc_id','integer'),
    Field('mt_persona_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mt_doc_vehiculo',
    Field('id','integer'),
    Field('fecha_emision','date'),
    Field('fecha_vencimiento','date'),
    Field('numero','string'),
    Field('cf_tipo_doc_id','integer'),
    Field('mt_vehiculo_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mt_estado',
    Field('id','integer'),
    Field('codigo','string'),
    Field('nombre','string'),
    migrate=False)

#--------
legacy_db.define_table('mt_kilometraje',
    Field('id','integer'),
    Field('fecha','date'),
    Field('kilometraje','integer'),
    Field('mt_vehiculo_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mt_persona',
    Field('id','integer'),
    Field('cedula','string'),
    Field('codigo','string'),
    Field('nombres','string'),
    Field('apellidos','string'),
    Field('ruta_foto','string'),
    Field('sexo','string'),
    Field('user','string'),
    Field('password','string'),
    Field('cf_cargo_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mt_vehiculo',
    Field('id','integer'),
    Field('placa','string'),
    Field('color','string'),
    Field('serial_motor','string'),
    Field('serial_caja','string'),
    Field('serial_carroceria','string'),
    Field('nro_ejes','integer'),
    Field('nro_ruedas','integer'),
    Field('kilometraje','integer'),
    Field('cf_vehiculo_modelo_id','integer'),
    Field('cf_vehiculo_tipo_id','integer'),
    Field('cf_tipo_combustible_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mv_asignacion',
    Field('id','integer'),
    Field('descripcion','string'),
    Field('fecha_proceso','date'),
    Field('fecha_inicio','string'),
    Field('fecha_fin','string'),
    Field('status','integer'),
    Field('mt_vehiculo_id','integer'),
    Field('cf_asignacion_tipo_id','integer'),
    Field('cf_localidad_id','integer'),
    Field('mv_solicitud_id','integer'),
    Field('mt_persona_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mv_gasto',
    Field('id','integer'),
    Field('descripcion','string'),
    Field('fecha_registro','date'),
    Field('fecha_gasto','date'),
    Field('kilometraje','integer'),
    Field('mv_asignacion_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mv_gasto_det',
    Field('id','integer'),
    Field('cantidad','string'),
    Field('unitario','string'),
    Field('total','string'),
    Field('impuesto','string'),
    Field('mv_gasto_id','integer'),
    Field('cf_item_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mv_solicitud',
    Field('id','integer'),
    Field('descripcion','string'),
    Field('fecha_solicitud','date'),
    Field('fecha_inicio','date'),
    Field('fecha_fin','date'),
    Field('status','integer'),
    Field('cf_solicitud_tipo_id','integer'),
    Field('mt_persona_id','integer'),
    migrate=False)

#--------
legacy_db.define_table('mv_viaje',
    Field('id','integer'),
    Field('descripcion','string'),
    Field('fecha_inicio','date'),
    Field('fecha_fin','date'),
    Field('status','integer'),
    Field('mt_ciudad_desde','integer'),
    Field('mt_ciudad_hasta','integer'),
    Field('mv_asignacion_id','integer'),
    migrate=False)
