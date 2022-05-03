import rdflib
import requests
import logging
import json
import datetime
from os import path
from fdpAPIconnector.default_templates import default_catalog_template, default_dataset_template, default_distribution_template

logger = logging.getLogger(__name__)

class FDPClient:
    DATA_FORMATS = {
        'n3': 'text/n3',
        'turtle': 'text/turtle',
        'xml': 'application/rdf+xml',
        'json-ld': 'application/ld+json',
        'nt': 'application/n-triples'
    }


    def __init__(self, baseurl, email = "",
                 password = "",
                 api_token=None,
                 publicurl='',
                 catalog_template=None,
                 dataset_template=None,
                 distribution_template=None
                 ):
        self.baseurl = baseurl.rstrip('/')
        if publicurl is not None and publicurl != "":
            self.publicurl = publicurl.rstrip('/')
        else:
            self.publicurl = self.baseurl
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        if api_token is not None and api_token != "":
            self.headers['Authorization'] = f'Bearer {api_token}'
        elif (email is not None and email != "") and (password is not None or password != ""):
            self.headers['Authorization'] = f'Bearer {self.gettoken(email, password)}'
        else:
            logger.error("Neither login email and password nor api_token are provided!")
            raise Exception("Invalid login data provided! Please provide either email and password or api_token")

        del self.headers['Accept']
        self._catalog_template = self._load_template(default_catalog_template)
        self._dataset_template = self._load_template(default_dataset_template)
        self._distribution_template = self._load_template(default_distribution_template)

        if catalog_template is not None:
            self._catalog_template = self._load_template(catalog_template)
        if dataset_template is not None:
            self._dataset_template = self._load_template(dataset_template)
        if distribution_template is not None:
            self._distribution_template = self._load_template(distribution_template)


    def gettoken(self, email, password):
        """
        Login to the FDP
        :param email:
        :param password:
        :return:
        """
        login = {"email":email,
               "password": password}
        #logger.info(json.dumps(login))
        response = requests.post(f"{self.baseurl}/tokens",
                      data=json.dumps(login), headers=self.headers)
        #response = requests.post(f"{self.baseurl}/tokens", data={"email": email, "password": password})
        if response.status_code == 200:
            return response.json()['token']

        logger.error ("Problem with the login: " + str(response))
        raise Exception("Problem with the login",response)
        # return response['token']

    def create(self, type, data, format='turtle'):
        """
        create a FDP resource of the type <type>
        :param type: type of resource to create
        :param data: resource data in format <format> (default turtle)
        :param format: format of data possible turtle (default), n3, xml ,nl, json-ld
        :return: id of newly created resource
        """
        logger.debug(f'Create metadata on {self.baseurl}/{type} with the content: \n{data}')
        create_headers=self.headers.copy()
        create_headers.update({'Content-Type': self.DATA_FORMATS[format]})
        #print(create_headers)
        try:
            data = self._convertRDFGraphtoString(data, format)
            r = requests.post(f'{self.baseurl}/{type}', data=data, headers=create_headers)
            return self._removePrefix(r.headers['Location'],f'{self.publicurl}/{type}/')
        except Exception as error:
            print(f'Unexpected error when connecting to {self.baseurl}/{type}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {self.baseurl}/{type}',
                      f'\nResponse message: {r.text}')
                raise

    def read(self, type='', id='' , subtype='',format='turtle', **kwargs):
        """
        read a FDP rescource of the type <type>
        :param type: type of resource to read
        :param id: id of resource to read
        :param subtype: subtype (e.g. expanded, members, meta)
        :param format: format of data possible turtle (default), n3, xml ,nl, json-ld
        :param kwargs: any additional requests parameter
        :return: redflib.Graph of the requested resource
        """
        url = f'{self.baseurl}'
        if type is not None and type != "":
            url = f'{url}/{type}'
            if id is not None and id != "":
                url = f'{url}/{id}'
            if subtype is not None and subtype != "":
                url = f'{url}/{subtype}'

        logger.debug(f'Read metadata: {url}')
        read_headers = self.headers.copy()
        read_headers.update({'Content-Type': self.DATA_FORMATS[format]})

        try:
            r = requests.get(url, headers=read_headers, **kwargs)
        except Exception as error:
            print(f'Unexpected error when connecting to {url}\n')
            raise error
        else:
            if r.status_code != 200:
                print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                      f'\nResponse message: {r.text}')
                raise

        g = rdflib.Graph()
        g.parse(data=r.text, format=format)
        return g

    def delete(self,type, id, **kwargs):
        """
        delete a FDP resource.
        :param type: type of resource to delete
        :param id: id of resource to delete
        :param kwargs: any additional requests parameter
        """
        logger.debug(f'Delete metadata: {self.baseurl}/{type}/{id}')
        del_headers = self.headers.copy()
        del del_headers['Content-Type']

        try:
            r = requests.delete(f'{self.baseurl}/{type}/{id}', headers = del_headers ,**kwargs)
        except Exception as error:
            print(f'Unexpected error when connecting to {self.baseurl}/{type}/{id}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {self.baseurl}/{type}/{id}',
                      f'\nResponse message: {r.text}')
                raise

    def update(self,type='', id='' , subtype='', data="", format='turtle', **kwargs):
        """
        update a FDP resource.
        :param type: type of resource to update
        :param id: id of resource to update
        :param subtype: subtype (e.g. meta/state, members/{userUuid})
        :param data: string or rdflib.Graph
        :param format: <string> 'turtle', 'n3', 'nt', 'xml' and 'json-ld'.
        :param kwargs: any additional requests parameter
        """
        url = f'{self.baseurl}'
        if type is not None and type != "":
            url = f'{url}/{type}'
            if id is not None and id != "":
                url = f'{url}/{id}'
            if subtype is not None and subtype != "":
                url = f'{url}/{subtype}'

        logger.debug(f'Update metadata on {url} with the content: \n{data}')
        update_headers = self.headers.copy()
        update_headers.update({'Content-Type': self.DATA_FORMATS[format]})

        try:
            data = self._convertRDFGraphtoString(data, format)
            r = requests.put(f'{url}', data=data, headers=update_headers, **kwargs)
            #print(f'{r.status_code} {r.reason}')
        except Exception as error:
            print(f'Unexpected error when connecting to {url}\n')
            raise error
        else:
            if r.status_code >= 300:
                print(f'HTTP error: {r.status_code} {r.reason} for {url}',
                      f'\nResponse message: {r.text}')
                raise

    def _convertRDFGraphtoString(self, data, format):
        """
        convert a rdflibGraph in string of format <format>
        :param data: string or rdflib.Graph
        :param format: format of data (e.g. turtle)
        :return: string in <format>
        """
        if isinstance(data, rdflib.Graph):
            return data.serialize(format=format)
        else:
            return data

    def _load_template(self, filepath):
        """load a template (file) or use the tmeplate string"""
        data = filepath
        if path.isfile(filepath):
            with open(filepath) as f:
                data = f.read()
        if '§§BASEURL' not in data:
            raise Exception("Invaild template does not contain §§BASEURL!")
        return data.replace("§§BASEURL",self.publicurl)
        #graph = rdflib.Graph()
        #graph.parse(path, format='ttl')
        #qres = graph.query("SELECT ?s ?o WHERE { ?s dcterms:hasVersion ?o }")
        #for row in qres:
        #    print(f"{row.s} dcterms:hasVersion {row.o}")

    def createCatalogRDF(self,title,version,publisher,ispartof=None,**kwargs):
        """
        create a RDF turte string for a Catalog resource based on catalog template
        :param title: title of catalog
        :param version: version of catalog
        :param publisher: publisher
        :param ispartof: id repository (default: url of FDP)
        :param kwargs: any additional Catalog parameters as defined in the template with the prefix '§§' matching is case sensitive
        :return: new catalog data in RDF turtle format
        """
        catalog = self._catalog_template
        catalog = catalog.replace(f'§§TITLE', str(title))
        if ispartof is None:
            catalog = catalog.replace(f'§§ISPARTOF', str(self.publicurl))
        else:
            catalog = catalog.replace(f'§§ISPARTOF', str(ispartof))
        catalog = catalog.replace(f'§§VERSION', str(version))
        catalog = catalog.replace(f'§§PUBLISHER', str(publisher))

        for key, value in kwargs.items():
            catalog = catalog.replace(f'§§{key}',str(value))

        result_catalog=""
        for line in catalog.split('\n'):
            if line.find('§§')>0:
                continue
            result_catalog=f'{result_catalog}\n{line}'
        result_catalog=result_catalog.strip()
        return result_catalog

    def createDatasetRDF(self, title, catalogid, version, publisher, themes_list, **kwargs):
        """
        create a RDF turte string for a dataset resource based on dataset template
        :param title: title of dataset
        :param catalogid: id of catalog the dataset belongs to
        :param version: version string
        :param publisher: publisher
        :param themes_list: list of themes
        :param kwargs: any additional dataset parameters as defined in the template with the prefix '§§' matching is case sensitive
        :return: new dataset data in RDF turtle format
        """
        dataset = self._dataset_template
        dataset = dataset.replace(f'§§TITLE', str(title))
        dataset = dataset.replace(f'§§CATALOGID', str(catalogid))
        dataset = dataset.replace(f'§§VERSION', str(version))
        dataset = dataset.replace(f'§§PUBLISHER', str(publisher))

        themes_string = self._join_list_to_string(themes_list, seperator=">, <", prefix="<", suffix=">")
        dataset = dataset.replace('§§THEMES', themes_string)

        for key, value in kwargs.items():
            if key in ['ISSUED','MODIFIED']:
                dataset = dataset.replace(f'§§{key}', self.dateTimeToXSDString(value))
                continue
            if key == "KEYWORDS":
                keywords_string = self._join_list_to_string(value,seperator="\", \"",prefix="\"",suffix="\"")
                dataset = dataset.replace(f'§§{key}', keywords_string)
                continue
            dataset = dataset.replace(f'§§{key}',str(value))

        result_=""
        for line in dataset.split('\n'):
            if line.find('§§')>0:
                continue
            result_=f'{result_}\n{line}'
        result_=result_.strip()
        return result_

    def createDistributionRDF(self, title, datasetid, version, publisher, mediatype, **kwargs):
        """
        create a RDF turte string for a distribution resource based on dataset template
        :param title: title of distribution
        :param datasetid: id of catalog the dataset belongs to
        :param version: version
        :param publisher: publisher
        :param mediatype: mediatype of distribution (e.g. "text/html")
        :param kwargs: any additional distribution parameters as defined in the template with the prefix '§§' matching is case sensitive
        :return: new dataset data in RDF turtle format
        """
        dataset = self._distribution_template
        dataset = dataset.replace(f'§§TITLE', str(title))
        dataset = dataset.replace(f'§§DATASETID', str(datasetid))
        dataset = dataset.replace(f'§§VERSION', str(version))
        dataset = dataset.replace(f'§§PUBLISHER', str(publisher))
        dataset = dataset.replace(f'§§MEDIATYPE', str(mediatype))


        for key, value in kwargs.items():
            if key in ['ISSUED','MODIFIED']:
                dataset = dataset.replace(f'§§{key}', self.dateTimeToXSDString(value))
                continue
            dataset = dataset.replace(f'§§{key}',str(value))

        result_=""
        for line in dataset.split('\n'):
            if line.find('§§')>0:
                continue
            result_=f'{result_}\n{line}'
        result_=result_.strip()
        return result_

    def dateTimeToXSDString(self,date_obj):
        """
        convert a datetime to FDP compatible string
        :param date_obj:
        :return:
        """
        if isinstance(date_obj,datetime.datetime):
            return f'"{date_obj.isoformat()}"^^xsd:dateTime'
        return date_obj

    def _join_list_to_string(self, elements,seperator, prefix,suffix):
        """
        join strings
        :param elements:
        :param seperator:
        :param prefix:
        :param suffix:
        :return:
        """
        if isinstance(elements, list):
            ret_string = seperator.join(elements)
            ret_string = f'{prefix}{ret_string}{suffix}'
            return ret_string

        return str(elements)

    def _removePrefix(self,text,prefix):
        """
        Remove a prefix from text
        :param text:
        :param prefix:
        :return:
        """
        if text.startswith(prefix):
            return text[len(prefix):]
        return text
