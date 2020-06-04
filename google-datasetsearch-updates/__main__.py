#!/usr/bin/env python
# -*- coding: utf-8 -*-

### Interface en ligne de commande ###
import re
def query_style(string):
	res = str(string)
	regex = r"^$|\s{3,}"
	matches = re.search(regex, res)
	if matches:
		msg = "%r est une chaîne de caractères vide ou contenant plus de trois espaces consécutifs" % string
		raise argparse.ArgumentTypeError(msg)
	return res

import argparse
parser = argparse.ArgumentParser(description="Construire l'historique des base de données recensées sur Google DataSetSearch à partir de mots-clés")
parser.add_argument("file", help="Fichier XML de sauvegarde de l'historique des bases de données recensées sur Google DataSetSearch")
parser.add_argument("-q", "--query", type=query_style, help="Requête par mots-clés sur Google DataSetSearch.")
args = parser.parse_args()

#### Scripts dédiés ###

import query, save

### Bibliothèques ###

import dicttoxml
import os
import time
import progressbar

### PATH ###

dirpath = os.getcwd()
PATH = dirpath + "/" + args.file

if not os.path.isfile(PATH):
	save.add_xml(PATH)
else:
	pass

### Construction de la liste des requêtes par mots-clés ###

historique = []
historique = save.get_queries(PATH)
historique = list(set(historique))

if args.query is not None:
	if args.query not in historique:
		historique.append(args.query)
	else:
		pass
else:
	if not historique:
		print("Fichier XML créé. Aucune requête enregistrée.")
		raise SystemExit
	else:
		pass

queries = []

for item in historique: 
    if item != 'None' : 
        queries.append(item)

queries = list(set(queries))

### Récupèration des métadonnées simples des ensembles de données obtenus par la liste des requêtes ###

docids = {}

print(str(len(queries)) + " requête(s) par mots-clés.")

for item in queries:

	search = query.quick_query(item)

	if search is not False:
		print("Requête obtenue :", item)
		save.add_start(PATH, "query", args.query) # Sauvegarde de la requête dans le fichier XML
		docids.update(search)
	else:
		print("! Échec de la requête : ", item)

keys = list(filter(None, docids.keys())) # Index par identifiant unique

### Écriture des entrées non-présentes dans le fichier XML lors des requêtes précédentes ### 

new = []

if save.get_docid(PATH):
	diff = list(set(keys) - set(save.get_docid(PATH)))
	new = list(filter(None, diff))
else:
	new = keys

if new:

	for item in progressbar.progressbar(new, widgets=['Écriture des métadonnées complètes pour les nouveaux identifiants uniques :', progressbar.Bar('#', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.Timer()]):

		save.add_docid(PATH, item)
		metadata = query.data_docid(item)
		metadata_xml = dicttoxml.dicttoxml(metadata, custom_root='about') 
		save.add_about(PATH, item, metadata_xml)

### Écriture des informations de mise à jour des base de données ###

res = []
	
for item in progressbar.progressbar(keys, widgets=['Écriture des informations de mises à jour :', progressbar.Bar('#', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.Timer()]):

	update = docids[item]['update']
	update = update[8::] # Retrait des 8 premiers caractères : "Updated "

	updates = save.get_updates(PATH, item)
	
	if update in updates:
		save.add_update(PATH, item, update, "False")
	else:
		save.add_update(PATH, item, update, "True")
		res.append(item)
