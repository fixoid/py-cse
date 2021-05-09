import google_custom_search as gcs

#req = 'dual%20nozzle%203dprntbot'
req = 'my%20little%20pony'

links = gcs.all_links(req, pages_max = 3, show_info = True)
for i,link in enumerate(links, start=1):
    print(str(i) + '\t' + link)