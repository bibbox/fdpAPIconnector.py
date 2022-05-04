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
                               publisher='Projectmanagementteam',
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               HOMEPAGE=fdpclient.baseurl)

pprint(newcat)
id=fdpclient.create(type='catalog',data=newcat)
print(id)
```

Read the created Catalog

```
cat_meta=fdpclient.read(type='catalog',id=id)
pprint(cat_meta.serialize(format="turtle"))
```

Update/Modify the created catalog

```
fdpclient.update(type='catalog', id=id, data=modified.cat_meta.serialize(format="turtle"))
```

Publish the created catalog

```
sate_published=json.dumps({"current":"PUBLISHED"})

fdpclient.update(type='catalog',id=id,subtype='meta/state',data=sate_published,format="json-ld")
```

Delete the created catalog
```
fdpclient.delete(type='catalog',id=id)
```

All functions are also available for datasets and distributions e.g. create:

```
newdat=fdpclient.createDatasetRDF(title="COVAC-DM Study",
                               version="1.0.0",
                               catalogid=id,
                               publishername="Projectmanagementteam",
                               ISSUED=datetime.datetime.now(),
                               MODIFIED=datetime.datetime.now(),
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               KEYWORDS=["diabetes mellitus type 1","diabetes mellitus type 2","COVID-19"],
                               DESCRIPTION="<https://biobank.medunigraz.at/.../biobank/pdf/Kohorten/5006_21_COVAC-DM_Study.pdf>",
                               CONTACTPOINT = "patrick.nitsche@medunigraz.at",
                               themes_list=["http://www.w3.org/ns/dcat#theme","http://identifiers.org/icd/Q87.8"])

newdis=fdpclient.createDistributionRDF(title="Distribution", # HTML distribution
                               version="1.0.0",
                               datasetid=dat_id,
                               publishername="Projectmanagementteam",
                               ISSUED=datetime.datetime.now(),
                               MODIFIED=datetime.datetime.now(),
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               mediatype="WSI", #text/html
                               FORMAT="SVS",
                               BYTESIZE="10737418240",
                               ACCESSURL="https://youtu.be/dQw4w9WgXcQ", # URL of OS
                               DOWNLOADURL="http://download.url")
dat_id=fdpclient.create(type='dataset',data=newdat)
dis_id=fdpclient.create(type='distribution',data=newdis)
```

### Subtypes

E.g. Get metadata (memberships and state) for Catalog
```
cat_meta_state=fdpclient.read(type='catalog',id=id,subtype='meta')
```

### Templates


Templates are used to create the RDF turtle format for the FDP resources. You might want to use your own templates:
```
fdpclient=FDPClient(fdp_baseurl,email,password,
                    catalog_template='./templates/catalog_template.ttl',
                    dataset_template='./templates/dataset_template.ttl',
                    distribution_template='./templates/distribution_template.ttl')
```

The template should look like this:

```
# default_catalog_template

@prefix dcat: <http://www.w3.org/ns/dcat#>.
@prefix dct: <http://purl.org/dc/terms/>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix loc: <§§BASEURL/>.
@prefix n0: <http://>.

loc:new
    a dcat:Catalog, dcat:Resource;
    dct:description "§§DESCRIPTION";
    dct:hasVersion "§§VERSION";
    dct:isPartOf <§§ISPARTOF>;
    dct:language <§§LANGUAGE>;
    dct:license <§§LICENSE>;
    dct:publisher [ a foaf:Agent; foaf:name "§§PUBLISHERNAME"];
    dct:rights <§§RIGHTS>;
    dct:title "§§TITLE";
    foaf:homePage <§§HOMEPAGE>;
    .
```
Variables that will be replaced have the prefix `§§`.


#### You might want to extend the information of the publisher:
**Important** you should only have one variable per line because each line containing a variable that was not set is thrown out.

```
@prefix dcat: <http://www.w3.org/ns/dcat#>.
@prefix dct: <http://purl.org/dc/terms/>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix loc: <§§BASEURL/>.
@prefix n0: <http://>.

loc:new
    a dcat:Catalog, dcat:Resource;
    dct:description "§§DESCRIPTION";
    dct:hasVersion "§§VERSION";
    dct:isPartOf <§§ISPARTOF>;
    dct:language <§§LANGUAGE>;
    dct:license <§§LICENSE>;
    dct:publisher [ a foaf:Agent; foaf:name "§§PUBLISHERNAME"; 
                                  rdf:Description [
                                      vcard:hasEmail [rdf:resource "§§PUBLISHEREMAIL"]; 
                                      vcard:hasUID [rdf:resource "§§PUBLISHERUID"]
                                  ]
                  ];
    dct:rights <§§RIGHTS>;
    dct:title "§§TITLE";
    foaf:homePage <§§HOMEPAGE>;
    .
 ```

### Build and upload to PyPI

```
# Intsall build and twine
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

# Build the package
python3 -m build

# to test the package first 
python3 -m twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fdpAPIconnector

# upload the package
python3 -m twine upload dist/*
```

## TODOs
 - [x] allow "login" via api-token instead of email and password
 - [ ] auto check for strings and urls(or iri) for RDF turtle creation
 - [ ] Create a **nice** documentation 
