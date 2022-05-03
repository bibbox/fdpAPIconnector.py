# fdpAPIconnector.py
Python package for communictaion with a FairDataPoint (FDP) API. 
This is based on the [fairdatapoint-client](https://github.com/fair-data/fairdatapoint-client) api client but adapted for [FAIRDataTeam/FAIRDataPoint](https://github.com/FAIRDataTeam/FAIRDataPoint).

## Usage

Import the FDPClient within your Python or Jupyter script.

```
from fdpAPIconnector.fdpclient import FDPClient
```

Create an instance of the client and login

```
fdp_baseurl = "http://localhost:8088"
email = "abmin@FDP.org"
password = "SuperSecretePassword"

fdpclient=FDPClient(fdp_baseurl,email,password)
```

You can also use an api_token
```
fdpclient=FDPClient(fdp_baseurl,api_token = 'APITOKEN123456789')
```

You may change the templates used for catalogs, datasets and distributions
```
fdpclient=FDPClient(fdp_baseurl,email,password,
                    catalog_template='./<pathToTemplates>/catalog_template.ttl',
                    dataset_template='./<pathToTemplates>/dataset_template.ttl,
                    distribution_template='./<pathToTemplates>/distribution_template.ttl
                    )
```


Create a new Catalog

```
newcat=fdpclient.createCatalogRDF(DESCRIPTION='My First Catalog',
                               title='My First Catalog',
                               version="1.0.0",
                               ispartof=fdpclient.publicurl,
                               publisher='Projektmanagementteam',
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               HOMEPAGE=fdpclient.baseurl)

pprint(newcat)
id=fdpclient.create(type='catalog',data=newcat)
print(id)
```


### TODOs
 - [x] allow "login" via api-token instead of email and password
 - [ ] auto check for strings and urls(or iri) for RDF turtle creation
 - [ ] Create a **nice** documentation 
