-- Cargar datos limpios
incidentes = LOAD 'eventos_limpios.csv'
  USING PigStorage(',')
  AS (
    uuid:chararray,
    tipo:chararray,
    subtipo:chararray,
    descripcion:chararray,
    latitud:double,
    longitud:double,
    comuna:chararray,
    timestamp:chararray
  );

-- Eliminar cabecera (si se arrastró)
sin_header = FILTER incidentes BY uuid != 'uuid';

-- Conteo por tipo
por_tipo = GROUP sin_header BY tipo;
conteo_tipo = FOREACH por_tipo GENERATE group AS tipo, COUNT(sin_header) AS cantidad;

-- Conteo por comuna
por_comuna = GROUP sin_header BY comuna;
conteo_comuna = FOREACH por_comuna GENERATE group AS comuna, COUNT(sin_header) AS cantidad;

-- Guardar resultados
STORE conteo_tipo INTO 'resultados_limpios/conteo_por_tipo' USING PigStorage(',');
STORE conteo_comuna INTO 'resultados_limpios/conteo_por_comuna' USING PigStorage(',');
