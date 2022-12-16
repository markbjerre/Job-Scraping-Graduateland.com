# Job-Scraping-Graduateland.com

This program analysis job postings on the danish job advert site Graduateland.com. To see the standard output see networkx_graph.html, no library needed. 

To customize graph via main python file the following libraries are needed:
- NetworkX
- Bokeh

For full functionality of the program the following (non-standard) libraries are needed
Crawler: Selenium
Scraper: BeautifulSoup
vertex: Yake, deep_translator
graph_visualize: NetworkX, Bokeh


This program is comprised of 6 seperate files, run in the following progression:

1. Cache functions.py - Adds cache functionality used at various stages of the program
Methods:
- Open_cache - Opens cache file, loads dictionary object from JSON
- Save_cache - Saves dict to cache file
2. Crawler.py - scrapes the webpage Graduateland
Methods:
- job_scrape - scrapes job-listing-page for job page links
- Crawler - opens graduateland using Selenium, enters search criteria and iterates through x amount of pages, stores in link_cache.json
3. scraper.py - scrapes job pages (gathered by crawler function) using BeautifulSoup.
Methods: 
- Offline-test - tests whether the job posting has expired
- Scraper - scrapes a job listing webpage using BeautifulSoup for a variety of information, stores in vertex_cache.json
- Scraper Methods:
- attribute_extract - extracts job attributes from information box in the lefthand side of the job-posting page
4. vertex.py - generates Vertex objects based on information scraped by scraping function, then translates text using GoogleTranslator and generates keywords from a given criteria (job_desc, category or skills), and assigns neighbors based on keywords
Class:
Vertex - holds information on individual job postings as well as graph neighbors
Methods: 
- Generate_Vertices - Generates a dictionary of Vertex Objects based on information collected by scraper function
- key_word_extractor - extracts list of keywords using Yake library
- generate_graph_dict - takes vertices dictionary and assigns neighbors given the criteria chosen for keyword generation (job_desc, category, skills). Neighbors decided by shared keywords between two vertices
5. graph_visualize - Visualizes graph network using networkx and bokeh libraries
Methods: 
- generate_graph_network - generates graph network using network x, using Vertices as nodes and Vertex object neighbors as edges
- visualize - visualizes graph network interactively with custamizable minimum edge threshold, nodes-with-no-neighbors filter and the option to get either edge information or node information when hovering over graph. node colors are based on company
6. main - compilation of library - allows user to change configs: #jobs in graph, minimum neighbors, remove isolates, inspect edges
Methods:
- intro_q - asks if any changes to the config should be made
- change_menu - interface for changing configs, iterative through recursion
- Verify_vertlen - function for changing #jobs to be analyzed
- Verify_Min_Neighbors - function for changing minimum neighbors in graph visualization
- Verify_Rm_Isolates - function for toggling whether isolated nodes should be included in graph
- Verify_Inspect_Edges - function for toggling whether edges or nodes should be interactive in the graph
- Make_Graph - constructs graph based on configs


