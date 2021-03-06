

default_catalog_template = ('@prefix dcat: <http://www.w3.org/ns/dcat#>.\n'
                   '@prefix dct: <http://purl.org/dc/terms/>.\n'
                   '@prefix foaf: <http://xmlns.com/foaf/0.1/>.\n'
                   '@prefix loc: <§§BASEURL/>.\n'
                   '@prefix n0: <http://>.\n'
                   '\n'
                   'loc:new\n'
                   '    a dcat:Catalog, dcat:Resource;\n'
                   '    dct:description "§§DESCRIPTION";\n'
                   '    dct:hasVersion "§§VERSION";\n'
                   '    dct:isPartOf <§§ISPARTOF>;\n'
                   '    dct:language <§§LANGUAGE>;\n'
                   '    dct:license <§§LICENSE>;\n'
                   '    dct:publisher [ a foaf:Agent; foaf:name "§§PUBLISHERNAME" ];\n'
                   '    dct:rights <§§RIGHTS>;\n'
                   '    dct:title "§§TITLE";\n'
                   '    foaf:homePage <§§HOMEPAGE>;\n'
                   '    .\n')

default_dataset_template = ('@prefix dcat: <http://www.w3.org/ns/dcat#>.\n'
                   '@prefix dct: <http://purl.org/dc/terms/>.\n'
                   '@prefix foaf: <http://xmlns.com/foaf/0.1/>.\n'
                   '@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n'
                   '@prefix loc: <§§BASEURL/>.\n'
                   '@prefix c: <§§BASEURL/catalog/>.\n'
                   '\n'
                   'loc:new\n'
                   '    a dcat:Dataset, dcat:Resource;\n'
                   '    dct:description "§§DESCRIPTION";\n'
                   '    dct:hasVersion "§§VERSION";\n'
                   '    dct:isPartOf c:§§CATALOGID;\n'
                   '    dct:issued §§ISSUED;\n'
                   '    dct:language <§§LANGUAGE>;\n'
                   '    dct:license <§§LICENSE>;\n'
                   '    dct:modified §§MODIFIED;\n'
                   '    dct:publisher [ a foaf:Agent; foaf:name "§§PUBLISHERNAME" ];\n'
                   '    dct:rights <§§RIGHTS>;\n'
                   '    dct:title "§§TITLE";\n'
                   '    dcat:contactPoint <§§CONTACTPOINT>;\n'
                   '    dcat:keyword §§KEYWORDS;\n'
                   '    dcat:landingPage <§§LANDINGPAGE>;\n'
                   '    dcat:theme §§THEMES;\n'
                   '    .\n')

default_distribution_template = ('@prefix dcat: <http://www.w3.org/ns/dcat#>.\n'
                        '@prefix dct: <http://purl.org/dc/terms/>.\n'
                        '@prefix foaf: <http://xmlns.com/foaf/0.1/>.\n'
                        '@prefix loc: <§§BASEURL/>.\n'
                        '@prefix d: <§§BASEURL/dataset/>.\n'
                        '\n'
                        'loc:new\n'
                        '    a dcat:Distribution, dcat:Resource;\n'
                        '    dct:description "§§DESCRIPTION";\n'
                        '    dct:hasVersion "§§VERSION";\n'
                        '    dct:isPartOf d:§§DATASETID;\n'
                        '    dct:issued §§ISSUED;\n'
                        '    dct:language <§§LANGUAGE>;\n'
                        '    dct:license <§§LICENSE>;\n'
                        '    dct:modified §§MODIFIED;\n'
                        '    dct:publisher [ a foaf:Agent; foaf:name "§§PUBLISHERNAME" ];\n'
                        '    dct:rights <§§RIGHTS>;\n'
                        '    dct:title "§§TITLE";\n'
                        '    dcat:accessURL <§§ACCESSURL>;\n'
                        '    dcat:byteSize "§§BYTESIZE";\n'
                        '    dcat:downloadURL <§§DOWNLOADURL>;\n'
                        '    dcat:format "§§FORMAT";\n'
                        '    dcat:mediaType "§§MEDIATYPE";\n'
                        '    .\n')