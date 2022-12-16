import json
from vertex import Generate_Vertices, generate_graph_dict
from graph_visualize import generate_graph_network, visualize

def Verify_vertlen(num):
    while True:
        try:
            x = int(input('\nhow many jobs would you like to visualize?'))
        except:
            print('please enter valid number')
        if x == 0:
            return 0
        if type(x) == int:
            return x
        else:
            print('please enter an integer or enter \'0\' to exit')


def Verify_Min_Neighborsa(min_neighbors):
    while True:
        print('\nmin_neighbors describes the minimum edges for a node to be excluded')
        try:
            x = int(input('\nplease enter an integer'))
        except:
            print('please enter a valid number or type \'0\' to exit')
        if x == 0:
            return min_neighbors
        else:
            return x

def Verify_Rm_Isolates(remove_isolates):
    print('\nRemoving isolates excludes nodes without neighbors from the graph')
    while True:
        x = input('would you like to remove isolates from graph? [yes/no]')
        if x == 'yes':
            return True
        if x == 'no':
            return False
        if x == 'exit':
            return remove_isolates
        else:
            print('please enter a yes or no or exit')

def Verify_Inspect_Edges(inspect_edges):
    print('\nToggling Inspect Edges lets you examine edges instead of nodes by hovering over them in the graph')
    while True:
        x = input('would you like to toggle inspect edges on? [yes/no]')
        if x == 'yes':
            return True
        if x == 'no':
            return False
        if x == 'exit':
            return inspect_edges
        else:
            print('please enter a yes or no or exit')


def change_menu(config):
    print('\nwhat configuration would you like to change?')
    print('1. jobs_in_graph -', config['jobs_in_graph'],  '\n2. neighbors -', config['min_neighbors'],  '\n3. remove_isolates -',config['remove_isolates'],'\n4. inspect_edges -', config['inspect_edges'], '\n0. exit')
    while True:
        try:
            x = int(input('\nplease enter the number of the config you would like to change'))
            break
        except:
            print('please enter valid number or \'0\' to exit')
        
        
    if x == 1:
        config['jobs_in_graph'] = Verify_vertlen(config['jobs_in_graph'])
    elif x == 2:
        config['min_neighbors'] = Verify_Min_Neighborsa(config['min_neighbors'])
    elif x == 3:
        config['remove_isolates'] = Verify_Rm_Isolates(config['remove_isolates'])
    elif x == 4:
        config['inspect_edges'] = Verify_Inspect_Edges(config['inspect_edges'])
    elif x == 0:
        return config
    else:
        print('did not recognize input, please try again')
        return change_menu(config)
    
    while True:
        x = input('Do you want to make more changes?[yes/no]')
        if x == 'yes':
            return change_menu(config)
        elif x == 'no':
            print('new config:')
            print('1. jobs_in_graph -', config['jobs_in_graph'], '\n2. criteria - ', config['criteria'], '\n3. neighbors -', config['min_neighbors'],  '\n4. remove_isolates -',config['remove_isolates'],'\n5. inspect_edges -', config['inspect_edges'])
            return config
        elif x == 'exit':
            return config
        else:
            print('did not recognize input, please enter yes or no or exit')

def intro_q(config):
    while True:
        q1 = input('Do you want to change any settings [yes/no]\n')
        if q1 == 'yes':
            return change_menu(config)
        elif q1 == 'no':
            return config
        elif q1 == 'exit':
            return config
        else:
            print('did not recognize answer, please enter yes, no or exit')

def Make_Graph(config):
    verts = Generate_Vertices(config['jobs_in_graph'])
    dict = generate_graph_dict(verts)
    network = generate_graph_network(dict, config['min_neighbors'],config['remove_isolates'])
    visualize(network, config['inspect_edges'])

def Repeat_Process():
    while True:
        x = input('would you like to generate another graph? [yes/no]')
        if x == 'yes':
            return True
        elif x == 'no' or x == 'exit':
            return False
        else:
            print('please enter valid input or \'exit\'')


if __name__=='__main__':
    config = {'jobs_in_graph': 150, 
            'min_neighbors': 5, 
            'remove_isolates':True, 
            'inspect_edges': False} 


    print('welcome to Graduateland Job Exploration')
    print('All data used for this program is stored in cache files. \nIf you would like to try the complete process with new data, please run crawler.py for fresh data or delete cache files (WARNING: this may take a long time, if crawler input and vertices input are big')
    while True:
        print('Current settings are:')
        print(json.dumps(config, indent=4))
        config = intro_q(config)
        print('Generating Graph...')
        Make_Graph(config)
        if Repeat_Process() == False:
            break
    




