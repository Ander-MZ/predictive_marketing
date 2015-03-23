# -*- coding: utf-8 -*-

from collections import Counter

# Permite activar niveles de detalle en mensajes de depuración
debug_lv1 = True
debug_lv2 = True
debug_lv3 = True

# Recibe una lista de elementos y un entero n positivo, regresando los n valores más comúnes
# en un formato de (elemento,frecuencia). Por default regresa el más frecuente
def most_common(lst,n=1):
    return Counter(lst).most_common(n)

# Recibe una cadena de texto que anexa a la bitácora indicada. Por default lo anexa a 'log.txt'
def logInfo(msg,log='log.txt'):
    log = open(log,'a')
    log.write(msg+"\n")
    log.close()
    return

# Recibe una colección y anexa cada entrada a la bitácora indicada de manera eficiente. Por default lo anexa a 'log.txt'
def logCollection(col,log='log.txt'):
    log = open(log,'a')
    for entry in col:
        log.write(str(entry)+"\n")
    log.close()
    return

def show(msg):
    if (debug_lv1):
        print msg

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return float('{0:.{1}f}'.format(f, n))
    i, p, d = s.partition('.')
    return float('.'.join([i, (d+'0'*n)[:n]]))