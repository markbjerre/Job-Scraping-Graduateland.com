import json

def open_cache(cache_name):
    '''
    opens the cache file if it exists and loads the JSON into a dictionary, which it then returns
    If the cahce file doesn't exist, creates a new chace dictionary
    Parameters
    ---
    None 
    Returns
    ---
    The opened cache
    '''
    try:
        cache_file = open(cache_name, 'r', encoding='utf8')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict, cache_name):
    '''
    saves the current state of the cache to disk
    Parameters
    ---
    cache_dict: dict
        the dictionary to save
    Returns
    ---
    None
    '''
    dumped_json_cache = json.dumps(cache_dict, indent=4, ensure_ascii=False)
    fw = open(cache_name,'w', encoding='utf8')
    fw.write(dumped_json_cache)
    fw.close()

def test():
    print('hello')