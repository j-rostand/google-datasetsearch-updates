#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree as ET
import os
import os.path
from datetime import datetime

def add_xml(PATH):
	"""Création d'un fichier XML avec un tag 'start' reprenant la date du jour."""

	root = ET.Element("root")
	start = ET.SubElement(root, "start")

	now = datetime.now()
	start.attrib["time"] = str(now)

	tree = ET.ElementTree(root)
	tree.write(PATH, xml_declaration=True, encoding='utf-8') # Writes XMl in current PATH with usual decleration

def add_docid(PATH, docid):
	"""Ajout d'une entrée par identifiant Google unique dans le fichier XML."""

	tree = ET.parse(PATH)
	root = tree.getroot()

	add_docid = ET.SubElement(root, 'database')
	add_docid.attrib["data-docid"] = str(docid)
	
	tree.write(PATH)

def add_start(PATH, statut, query):
	"""Ajout d'une entrée de type requête ou de type docid dans le fichier XML."""

	tree = ET.parse(PATH)
	root = tree.getroot()

	now = datetime.now()

	add_query = ET.SubElement(root.find("./start"), statut)
	add_query.attrib['time'] = str(now)
	add_query.text = str(query)

	tree.write(PATH)

def add_about(PATH, docid, metadata_xml):
	"""Ajout des métadonnées sur les entrées uniques Google."""

	tree = ET.parse(PATH)
	root = tree.getroot()
	
	path_about = "./database[@data-docid='" + docid + "']"
	add_about = ET.fromstring(metadata_xml)
	root.find(path_about).append(add_about)
	
	tree.write(PATH)

def add_update(PATH, docid, Dataset_updated_, answer):
	"""Ajout d'une entrée précisant la mise à jour ou non de la base de données."""

	tree = ET.parse(PATH)
	root = tree.getroot()

	now = datetime.now()

	path_docid = "./database[@data-docid='" + docid + "']"
	add_update = ET.SubElement(root.find(path_docid), 'update')
	add_update.attrib["datetime"] = str(now)
	add_update.attrib["Dataset_updated_"] = str(Dataset_updated_)
	add_update.text = answer
	
	tree.write(PATH)

def get_updates(PATH, docid):
	"""Récupère les listes de mises à jour enregistrées dans le fichier XML."""

	tree = ET.parse(PATH)
	root = tree.getroot()

	res = []

	for date in	root.findall(".//*[@data-docid='" + docid + "']/update"): 
		res.append(date.get('Dataset_updated_'))

	return res

def get_docid(PATH):
	"""Récupère les identifiants uniques Google présents dans le fichier XML."""

	tree = ET.parse(PATH)
	root = tree.getroot()

	res = []

	for docid in root.findall("./database"): 
		res.append(docid.get('data-docid'))
	
	return res

def get_queries(PATH): 
	"""Récupère l'historique des requêtes soumises au programme."""

	tree = ET.parse(PATH)
	root = tree.getroot()

	res = []

	for query in root.findall("./start/query"):
		res.append(query.text)

	return res
