# -*- coding: utf-8 -*-

from lxml import etree

tree = etree.parse("dataSMS1.xml")
compteur = 0
for sms in tree.xpath("/corpus/sms/cont"):
    compteur +=1
    if compteur>10:
        break
    print(sms.text)
