from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

top = Element('Data')

comment = Comment('Almacena las transacciones de cada tarjeta')
top.append(comment)

child_card = SubElement(top, 'Card')

child_pan = SubElement(child_card, 'PAN')
child_pan.text = '000085d51fc7ca2879750f7850bd7db1'

child_transactions = SubElement(child_card, "Transactions")

child_transaction = SubElement(child_transactions, "T")
child_transaction.text = "(25.00,18/03/2015,6385)"
child_transaction = SubElement(child_transactions, "T")
child_transaction.text = "(7425.00,05/11/2014,3301)"
child_transaction = SubElement(child_transactions, "T")
child_transaction.text = "(682.00,23/02/2014,9000)"
child_transaction = SubElement(child_transactions, "T")
child_transaction.text = "(99.00,11/07/2015,1234)"


child_card = SubElement(top, 'Card')

child_pan = SubElement(child_card, 'PAN')
child_pan.text = 'b34a4110506e21bb1bf1a46676b8212'

child_transactions = SubElement(child_card, "Transactions")

child_transaction = SubElement(child_transactions, "T")
child_transaction.text = "(7425.00,05/11/2014,3301)"
child_transaction = SubElement(child_transactions, "T")
child_transaction.text = "(25.00,18/03/2015,6385)"


print prettify(top)