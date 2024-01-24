import requests
from bs4 import BeautifulSoup



def bitstreamLinks(bundle_url):
   response = requests.get(bundle_url)
   if response.status_code == 200:
      results = response.json()
      bundles = results['_embedded'].get('bundles', [])
      
      if bundles:
         for bundle in bundles:
            bundleName = bundle['name']
            if 'ORIGINAL' in bundleName:
               links = bundle.get('_links', [])
               if links:
                  #return links['bitstreams']['href']
                  return file_info(links['bitstreams']['href'])
         
               
               
def file_info(bitstream_url):
    response = requests.get(bitstream_url)
    htm_links = []  # Lista para almacenar los enlaces que contienen ".htm"

    if response.status_code == 200:
        results = response.json()
        bitstreams = results.get('_embedded', {}).get('bitstreams', [])

        if bitstreams:
            for bitstream in bitstreams:
                bitstream_name = bitstream.get('name', '')
                if '.htm' in bitstream_name:
                   links = bitstream.get('_links', [])
                   content_link = links.get('content', {})
                   href_value = content_link.get('href')
                   if href_value:
                      enlaces_pdf = getPdfLink(href_value)
                      htm_links.extend(enlaces_pdf)
        return htm_links
   
def getPdfLink(contentLink):
   response = requests.get(contentLink)
   pdf_links = []  # Lista para almacenar los enlaces PDF encontrados

   if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      links = soup.find_all('a', href=True)

      for link in links:
         pdf_links.append(link['href'])

      return pdf_links