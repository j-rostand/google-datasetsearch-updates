---
title: google-datasetsearch-updates
auhor: Jules Rostand
date: 4 juin 2020
---

Ce script python a pour objectif de permettre à l'utilisateur d'enregistrer, à partir de requêtes par mots-clés, l'historique des mises à jour de base de données recensées sur le service [Data Set Search](https://datasetsearch.research.google.com/) de Google.

## Introduction

Le moteur de recherche **Data Set Search** de Google, pensé comme un complément à Google Scholar, a pour objectif de "faciliter la découverte des ensembles de données", selon les termes mêmes de Natasha Noy (*Research Scientist*, Google AI) dans son [article de blog](https://www.blog.google/products/search/making-it-easier-discover-datasets/) du 5 septembre 2018. Ce service repose sur la description par les producteurs de leurs bases de données, principalement à travers l'utilisation la syntaxe open-source [schema.org](https://schema.org/Dataset) basée sur format [DCAT (Data Catalog Vocabulary)](https://www.w3.org/) de [W3C](https://www.w3.org/TR/vocab-dcat/). L'ensemble de ces informations sont présentées par Google dans son [guide sur les ensemble de données](https://developers.google.com/search/docs/data-types/dataset).  

Si ce service est d'une utilité réelle pour s'orienter dans la masse des ensemble de données, il ne répond toutefois pas à l'ensemble des questionnements que soulèvent la production et la publication de ces derniers. En particulier, ce service, qui associe à chaque ensemble de données un identifiant unique (```data-docid```) ne propose pas d'historique de la mise à jour de ces ensemble de données. Pourtant, l'historique des mises à jour de ces ensembles de données - largement issus de la philosophie de l'*open data* et notamment de l'[*Open Governement Data*](https://www.oecd.org/gov/digital-government/open-government-data.htm) - est riche de sens sur les préoccupations des organisations qui les construisent. Construit autour du moteur de recherche Google, ce programme a pour objectif de favoriser l'exercice d'un regard critique sur les ensemble de données mis à disposition du public.

## Fonctionnement

Ce script lit et écrit un fichier XML. À chaque utilisation du programme, l'utilisateur doit renseigner le nom du fichier souhaité avec l'extension `.xml`. Si le fichier renseigné n'est pas identifié, le script crée un fichier XML dans le répertoire actuel. 

L'interface de Google Data Set Search se présente, ici pour la requête `Alan Turing`, de la manière suivante :  

![Alan Turing](./alan-turing.png "Alan Turing")

Ce script interroge le moteur de recherche Data Set Search de Google par des requêtes sous forme de mots-clés. Il peut s'agir d'une simple chaîne de caractères ou de l'expression admettant les filtres proposés par Google, disponible dans l'URL affiché sur la plateforme - par exemple, la requête `Alan Turing&filters=WyJbXCJmaWxlX2Zvcm1hdF9jbGFzc1wiLFtcIjFcIl1dIl0%3D` reprend la requête `Alan Turing` avec le filtre `Tableau` pour le format de téléchargement. À partir du fichier XML ayant vocation à enregistrer un ensemble de requêtes distinctes, le programme construit une liste des requêtes par mots-clés, récupère les métadonnées simples des ensembles de données obtenus par la liste des requêtes, avant de se consacrer à obtenir les informations générales et les informations de mise à jour de chaque base de données ainsi sélectionnée. Il fonctionne de la manière suivante : 

### Construction de la liste des requêtes par mots-clés

Le script récupère tout d'abord, au sein du tag `<start></start>` du fichier XML donné, les requêtes enregistrées auparavant au sein des tags `<query></query>`. À partir de cette liste et de l'éventuelle requête soumise par l'utilisateur, le script construit une liste de requêtes par mots-clés valides. Dans l'exemple ci-dessus lors d'une première utilisation, la liste de requêtes comporte un seul élément : ` ["Alan Turing"]`.

### Récupèration des métadonnées simples des ensembles de données obtenus par la liste des requêtes

Le script récupère, pour chaque requête par mots-clés, l'identifiant unique `data-docid`, le titre, la source et la date de mise à jour de l'ensemble des bases de données dans la liste défilante à gauche de l'écran. Dans l'exemple évoqué ci-dessus, on obtient ainsi ces informations sur les 64 ensemble de données recensés.

### Écriture des entrées non-présentes dans le fichier XML lors des requêtes précédentes 

Le scirpt considère ensuite la différence entre la liste des identifiants uniques obtenus pour l'ensemble des requêtes et la liste des identifiants uniques recensées dans le fichier XML. Pour chacun des identifiants uniques non-présents dans le fichier XML, le script ajoute une entrée au sein du tag `<database></database>`. Après avoir interrogé à nouveau le moteur de recherche à partir de cet identifiant, le script adjoint à ce tag les métadonnées complètes, décrites dans la partie droite de l'écran. Cette opération, longue, n'est effectuée qu'une seule fois, lors de l'ajout de l'identifiant unique au fichier XML. Dans l'exemple ci-dessous, les métadonnées de la première entrée sont décrites dans ce fichier de la manière suivante : 

```xml
<about>
<n0 type="dict">
<dataset_url type="str">
https://www.researchgate.net/publication/313656111_Alan_Turing_The_founder_of_computer_science
</dataset_url>
<index type="str">-1</index>
<source_url type="str">
https://www.researchgate.net/publication/313656111_Alan_Turing_The_founder_of_computer_science
</source_url>
<num_replicas type="str">0</num_replicas>
</n0>
<Dataset_updated_ type="str">Oct 31, 2013</Dataset_updated_>
<Authors type="str"> Jonathan Peter Bowen </Authors>
<abstract type="str">
[<p>Alan Mathison Turing, OBE, FRS, has a rightful claim to the title of father of modern computing. He laid the theoretical groundwork for a universal machine that models a computer in its most general form before World War II. During the war, Turing was instrumental in developing and influencing actual computing devices that have been said to have shortened the war by up to two years by decoding encrypted enemy messages that were believed by others to be unbreakable. Unlike some theoreticians, he was willing to be involved with practical aspects, and was as happy to wield a soldering iron as he was to wrestle with a mathematical problem, normally from a unique angle compared to others.</p>]
</abstract>
</about>
```

### Écriture des informations de mise à jour des base de données

Pour chaque identifiant unique de la liste des requêtes, le script ajoute un tag \<update>\</update> spécifiant la date et l'heure de fonctionnement du programme au sein de l'attribut `datetime` et la dernière date de mise à jour disponible au sein de l'attribut `Dataset_updated_`. Ce tag dispose enfin d'une mention `True` ou `False` ìndiquant respectivement l'xistence ou non d'une mise à jour depuis le dernier fonctionnement du programme. Dans l'exemple ci-dessous, cette information de mise à jour s'écrit de la manière suivante : 

```xml
<update datetime="2020-06-04 14:49:47.111701" Dataset_updated_="Oct 31, 2013">True</update>
```

De manière plus générale, cette première entrée de la requête `Alan Turing` est enregistré de la manière suivante : 

```xml
<root>
<start time="2020-06-04 14:47:03.645517">
<query time="2020-06-04 14:47:16.683350">Alan Turing</query>
</start>
<database data-docid="GoHV6IpcE9Sty6U9AAAAAA==">
<about>
<n0 type="dict">
<dataset_url type="str">
https://www.researchgate.net/publication/313656111_Alan_Turing_The_founder_of_computer_science
</dataset_url>
<index type="str">-1</index>
<source_url type="str">
https://www.researchgate.net/publication/313656111_Alan_Turing_The_founder_of_computer_science
</source_url>
<num_replicas type="str">0</num_replicas>
</n0>
<Dataset_updated_ type="str">Oct 31, 2013</Dataset_updated_>
<Authors type="str"> Jonathan Peter Bowen </Authors>
<abstract type="str">
[<p>Alan Mathison Turing, OBE, FRS, has a rightful claim to the title of father of modern computing. He laid the theoretical groundwork for a universal machine that models a computer in its most general form before World War II. During the war, Turing was instrumental in developing and influencing actual computing devices that have been said to have shortened the war by up to two years by decoding encrypted enemy messages that were believed by others to be unbreakable. Unlike some theoreticians, he was willing to be involved with practical aspects, and was as happy to wield a soldering iron as he was to wrestle with a mathematical problem, normally from a unique angle compared to others.</p>]
</abstract>
</about>
<update datetime="2020-06-04 14:49:47.111701" Dataset_updated_="Oct 31, 2013">True</update>
</database>
</root>
```

## Installation

1. Cloner le dépôt : `git clone ...`

2. Se déplacer dans le répertoire du script : `cd google-datasetsearch-updates`

3. Installer les dépendances avec pip : `pip3 install -r requirements.txt`
