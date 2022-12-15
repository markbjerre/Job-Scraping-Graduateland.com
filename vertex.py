from scraper import Scraper, Offline_test
from cache_functions import save_cache, open_cache
import yake
from deep_translator import GoogleTranslator

class Vertex:
    def __init__(self, url, cache={}, store_cache=True):

        attr_dict = Scraper(url, cache, store_cache)
        self.attr_dict = attr_dict
        self.title = attr_dict.get('title')
        self.blob = attr_dict.get('job_desc')
        self.company = attr_dict.get('company')
        self.industry = attr_dict.get('industry')
        self.expiration = attr_dict.get('expiration') 
        self.followers = attr_dict.get('followers')
        self.logo = attr_dict.get('logo')
        self.location = attr_dict.get('location')
        self.category = attr_dict.get('category')
        self.job_type = attr_dict.get('job_type')
        self.skills = attr_dict.get('skills')
        self.language_req = attr_dict.get('language')
        self.date_scraped = attr_dict.get('date_scraped')
        self.link = url

        self.neighbors = {}

    def add_neighbor(self, neighbor, word):
        if self.neighbors.get(neighbor):
            self.neighbors[neighbor].append(word)
        else: 
            self.neighbors[neighbor] = [word]

    def get(self):
        return self.link
        
def Generate_Vertices(vertices_count=9999):
    links_cache = 'link_cache.json'
    vert_cache = 'vertex_cache.json'
    link_dict = open_cache(links_cache)
    vert_dict = open_cache(vert_cache)
    iterations_count = 0
    vertices = []
    
    for i in link_dict:
        iterations_count += 1
        if not vert_dict.get(i):
            if Offline_test(i):
                continue
        vertices.append(Vertex(i, cache=vert_dict))

        if iterations_count == vertices_count:
            break
        
    return vertices
 
#vertices_list = Generate_Vertices(10)

def key_word_extractor(extractor, text):
    word_list = []
    keywords = extractor.extract_keywords(text)
    for kw in keywords:
        word_list.append(kw[0])
    return word_list


def generate_graph_dict(vertices_list, criteria):
    #cache load (3 categories, job_desc, skills, category)
    word_cache_str = 'word_cache.json'
    word_cache = open_cache(word_cache_str)
    word_dict = word_cache.get(criteria)
    if not word_dict:
        word_dict = {'words': {}, 'vertex':{}}

    #Yake (keyword generator) config
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.3
    numOfKeywords = 40
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    
    #Translator for non-english text
    translator = GoogleTranslator(source='auto', target='en')

    #graph
    vertices = {}

    for vertex_obj in vertices_list:
        vertex = vertex_obj.link
        if word_dict['vertex'].get(vertex):
            word_list = word_dict.get('vertex').get(vertex)

        else:
            word_dict['vertex'][vertex] = []
            text = vertex_obj.attr_dict.get(criteria)
            try: 
                text_translated = translator.translate(text[:3000])
            except:
                continue
            word_list = key_word_extractor(custom_kw_extractor, text_translated)
            for word in word_list:#doc.ents:
                if word_dict['words'].get(word):
                    #print(word_dict['words'].get(word))
                    word_dict['words'][word].append(vertex)
                else:
                    word_dict['words'][word] = [vertex]
                word_dict['vertex'].get(vertex).append(word)

        if not vertices.get(vertex):
            vertices[vertex] = vertex_obj

        for word in word_list:
            for neighbor in word_dict.get('words').get(word):
                if neighbor == vertex or not vertices.get(neighbor):
                    continue
                #print(vertices[neighbor])
                vertices[vertex].add_neighbor(vertices[neighbor], word)
                vertices[neighbor].add_neighbor(vertices[vertex], word)
        

    word_cache[criteria] = word_dict
    save_cache(word_cache, word_cache_str)
    return vertices

#vertices_list = Generate_Vertices(100)
#x = generate_graph_dict(vertices_list, 'job_desc')
