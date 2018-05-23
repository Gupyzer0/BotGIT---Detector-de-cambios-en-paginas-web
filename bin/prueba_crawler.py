#pruebaCrawler
import pprint
from Crawler import Araña

spider = Araña('http://localhost',5,5)
spider.caminar()

pprint.pprint(spider.arregloLinks)