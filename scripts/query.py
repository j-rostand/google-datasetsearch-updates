#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import dicttoxml
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def data_docid(docid):
    """Collecte les métadonnées générales sur une base de données à partir de son identifiant unique Google.
    Retourne un dictionnaire avec les différents types de métadonnées obtenus en index."""

    ### Préparation (BeautifulSoup) ###

    URL = 'https://datasetsearch.research.google.com/search?docid=' + str(docid)  
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
    
    try:
        results = soup.select_one("div.zPqhQb") 
    except:
        return False

    output = {}

    ### Titre ###

    try: 
        output['title'] = results.find('h1.SAyv5').text
    except AttributeError:
        pass

    ### Sources ###

    try:
        docid_urls = results.select("div.jqqkc") 
        i = 0

        for docid_url in docid_urls: # Informations sur les bases de données
            
            temp = {}

            try:
                temp['dataset_url'] = docid_url.get('data-dataset-url')
            except AttributeError:    
                pass
            try:
                temp['index'] = docid_url.get('data-index')
            except AttributeError:
                pass
            try: 
                temp['source_url'] = docid_url.get('data-source-url')
            except AttributeError:
                pass
            try:
                temp['num_replicas'] = docid_url.get('data-num-replicas') # Ou temp['data-replica-sorted'] = docid_url.get('data-replica-sorted')
            except AttributeError:
                pass
            try:
                replica_index = docid_url.get('data-replica-index')
            except AttributeError:
                pass
            if replica_index: # Exception (absence de replica_index)
                output[str(replica_index)] = temp
            else:
                output["default_(" + str(i) + ")"] = temp
                i = i + 1

    except AttributeError:
        pass
    
    ### Informations générales ###

    try:
        docid_elems = results.find_all(class_='ukddFf')

        for docid_elem in docid_elems:

            elem = docid_elem.find(class_='pXX2tb')

            try:
                output[str(elem.next)] = str(elem.next_sibling.next)
            except AttributeError:
                pass

    except AttributeError:
        pass

    ### License (mise en forme particulière par Google) ###

    try: 
        regex = r"(?<=>)[^<:]+(?=:?<)" 
        output['License '] = str(re.findall(regex,output['License '])[0])
    except:
        pass

    ### Abstract ###

    try:
        docid_abstract = results.find('div', class_="iH9v7b")
        output['abstract'] = str(docid_abstract.find_all('p'))
    except AttributeError:
        pass

    return output

def quick_query(keyword):
    """
    Collecte les informations basiques sur les base de données à partir d'une liste défilante de résultats.
    Retourne un dictionnaire de dictionnaires avec l'identifiant unique Google en index.
    """
    
    ### Préparation (Selenium) ###

    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US, en')
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://datasetsearch.research.google.com/search?query="+ str(keyword))
    
    results = driver.find_element_by_css_selector('ol.VAt4')

    res = {}

    ### Informations basiques ###

    query_elems = results.find_elements_by_css_selector("li.UnWQ5")

    del query_elems[-1]
    
    for query_elem in query_elems:

        data = {}

        data['title'] = query_elem.find_element_by_css_selector('h1.iKH1Bc').text
        data['source'] = query_elem.find_element_by_css_selector('li.iW1HZe').text
        try:
            data['update'] = query_elem.find_element_by_css_selector('span.zKF3u').text
        except:
            data['update'] = 'NA'
        docid = query_elem.find_element_by_css_selector('div.xdICpb').get_attribute("data-docid") # TO DO : test sur le "hover", souvent le premier élément de la liste, class = .bv5XQc

        if docid is not None:
            res[str(docid)] = data

    return res
