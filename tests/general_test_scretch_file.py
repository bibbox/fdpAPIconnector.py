import datetime
import fdpAPIconnector as fdpconn
from src.fdpAPIconnector.fdpclient import FDPClient
from pprint import pprint
import datetime
import json

#my_headers = {'Accept' : 'application/json','Content-Type':'application/json'}
fdpclient=FDPClient("http://localhost:8088","albert.einstein@example.com","password",publicurl="http://localhost:8088")
fdpclient.headers

# Create a new Catalog
newcat=fdpclient.createCatalogRDF(DESCRIPTION='Hauptkatalog Biobank Graz',
                               title='Hauptkatalog Biobank Graz',
                               version="1.0.0",
                               ispartof=fdpclient.publicurl,
                               publishername='Projektmanagementteam',
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/de',
                               HOMEPAGE=fdpclient.baseurl)

pprint(newcat)
id=fdpclient.create(type='catalog',data=newcat)
print(id)


# Create a new Dataset

newdat=fdpclient.createDatasetRDF(title="COVAC-DM Study",
                               version="1.0.0",
                               catalogid=id,
                               publishername="Projektmanagementteam",
                               ISSUED=datetime.datetime.now(),
                               MODIFIED=datetime.datetime.now(),
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               KEYWORDS=["diabetes mellitus type 1","diabetes mellitus type 2","COVID-19"],
                               DESCRIPTION="<https://biobank.medunigraz.at/.../biobank/pdf/Kohorten/5006_21_COVAC-DM_Study.pdf>",
                               CONTACTPOINT = "patrick.nitsche@medunigraz.at",
                               themes_list=["http://www.w3.org/ns/dcat#theme","http://identifiers.org/icd/Q87.8"])
pprint(newdat)
dat_id=fdpclient.create(type='dataset',data=newdat)
print(dat_id)


# Create a new Distribution

newdis=fdpclient.createDistributionRDF(title="Distribution", # HTML distribution
                               version="1.0.0",
                               datasetid=dat_id,
                               publishername="Projektmanagementteam",
                               ISSUED=datetime.datetime.now(),
                               MODIFIED=datetime.datetime.now(),
                               LANGUAGE='http://id.loc.gov/vocabulary/iso639-1/en',
                               mediatype="WSI", #text/html
                               FORMAT="SVS",
                               BYTESIZE="10737418240",
                               ACCESSURL="https://youtu.be/dQw4w9WgXcQ", # URL of OS
                               DOWNLOADURL="http://download.url")
pprint(newdis)
dis_id=fdpclient.create(type='distribution',data=newdis)
print(dis_id)


# Publish the catalog and data set
sate_published=json.dumps({"current":"PUBLISHED"})

fdpclient.update(type='catalog',id=id,subtype='meta/state',data=sate_published,format="json-ld")
fdpclient.update(type='dataset',id=dat_id,subtype='meta/state',data=sate_published,format="json-ld")

# Delete Distribution
fdpclient.delete(type='distribution',id=dis_id)

# Read the created Catalog

cat_meta=fdpclient.read(type='catalog',id=id)
pprint(cat_meta.serialize(format="turtle"))


# Update the version of the catalog
qres = cat_meta.query("SELECT ?s ?o WHERE { ?s dcterms:hasVersion ?o }")
for row in qres:
    print(f"{row.s} dcterms:hasVersion {row.o}")

cat_meta.update("""
         DELETE { ?s dcterms:hasVersion '1.0.0' }
         INSERT { ?s dcterms:hasVersion '2.0.0' }
         WHERE { ?s dcterms:hasVersion '1.0.0' }
         """)

print("After Update")
qres = cat_meta.query("SELECT ?s ?o WHERE { ?s dcterms:hasVersion ?o }")
for row in qres:
    print(f"{row.s} dcterms:hasVersion {row.o}")


fdpclient.update(type='catalog', id=id, data=cat_meta.serialize(format="turtle"))
