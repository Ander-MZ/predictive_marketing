#!/bin/bash

psql -d banamex -U eglobal -F "," -A -c "select pan, amount, mcc, date_part('year',fecha) as year, date_part('month',fecha) as month, date_part('day',fecha) as day, date_part('hour',fecha) as hour, date_part('min',fecha) as min, extract(dow from fecha::timestamp) as dow, numero_afiliacion as com_id from log_bmx_eglobal where fecha::date >= '${1}'::date and fecha::date < '${2}'::date" > ~/Storage/data/${1}_${2}_data.csv