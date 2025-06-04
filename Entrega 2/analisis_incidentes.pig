-- Cargar los datos
incidentes = LOAD 'eventos_convertidos.csv'
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

-- Eliminar cabecera (filtrar por UUID, asumimos que la cabecera tiene "uuid")
sin_header = FILTER incidentes BY uuid != 'uuid';

-- Eliminar registros incompletos (filtros básicos)
limpios = FILTER sin_header BY (tipo is not null) AND (comuna is not null) AND (tipo != '');

-- Conteo por tipo
por_tipo = GROUP limpios BY tipo;
conteo_tipo = FOREACH por_tipo GENERATE group AS tipo, COUNT(limpios) AS cantidad;

-- Conteo por comuna
por_comuna = GROUP limpios BY comuna;
conteo_comuna = FOREACH por_comuna GENERATE group AS comuna, COUNT(limpios) AS cantidad;

-- Guardar resultados
STORE conteo_tipo INTO 'resultados/conteo_por_tipo' USING PigStorage(',');
STORE conteo_comuna INTO 'resultados/conteo_por_comuna' USING PigStorage(',');
