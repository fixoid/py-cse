import os
import sys
import json
sys.path.append(os.path.dirname(__file__)+'/..')
import google_custom_search as gcs

links = []
path = os.path.dirname(__file__)+'/'
print (path)

#req = 'dual%20nozzle%203dprntbot'
req = 'my%20little%20pony'


print(gcs.all_links(req, True))



