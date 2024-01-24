import requests
import pandas as pd
import getDspaceItemFile
import time

data_to_save = []

startTime = time.time()
page = 0  # Página inicial
page_size = 100  # Tamaño de la página

while page < 1:

    print(page)
    # URL del endpoint de búsqueda de DSpace
    url = f'https://repositorio.utalca.cl/repositorio/server/api/discover/search/objects?query=".htm*"&page={page}&size={page_size}'

    # Realizar la solicitud GET a la API de DSpace
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Convertir la respuesta a formato JSON
        results = response.json()



        # Obtener la lista de objetos
        objects = results['_embedded']['searchResult']['_embedded'].get('objects', [])

        if objects:
            for obj in objects:
                indexable_object_name = obj['_embedded']['indexableObject']['name']
                links = obj['_embedded']['indexableObject'].get('_links',[])
                uuid = obj['_embedded']['indexableObject']['id']
                indexable_object_description = None

                if 'bundles' in links:
                    if links['bundles']:
                        indexable_object_description = links['bundles']['href']
                        fileLink = getDspaceItemFile.bitstreamLinks(indexable_object_description)
                        #print(f'{uuid} Enlaces: {fileLink}')
                        for pdf_link in fileLink:
                            data_to_save.append({'uuid': uuid, 'pdfLink': pdf_link})

        else:
            # No hay más resultados, terminar el bucle
            break

    else:
        print('La solicitud no fue exitosa:', response.status_code)
        break

    # Avanzar a la siguiente página
    page += 1


end_time = time.time()
elapsed_time = end_time - startTime

df = pd.DataFrame(data_to_save)
df.to_excel('resultados.xlsx', index=False)
print(f'Ejecución finalizada en {elapsed_time:.2f} segundos. Se ha creado el archivo Excel "resultados.xlsx".')