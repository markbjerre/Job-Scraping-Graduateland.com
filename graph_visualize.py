import networkx as nx
import random
from bokeh.palettes import Turbo256
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show, from_networkx
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, NodesOnly)
from bokeh.palettes import Spectral4, Turbo256


def generate_graph_network(graph_dict, threshold=5, rm_isolates=True):
    G = nx.Graph()
    x = graph_dict
    G.add_nodes_from(x)

    #generate color_map
    unique_companies = list(set([x[i].company for i in x]))
    colors = list(Turbo256)
    random.shuffle(colors)
    color_dict = {}
    for i in range(len(unique_companies)):
        color_dict[unique_companies[i]] = colors[i]

    edges = []
    node_attrs = {}
    
    def joiner(inp):
        if type(inp) == list:
            out = ", ".join(inp)
        else:
            out = inp
        return out

    for k in x:
        
        node_attrs[k] = {'company':x[k].company, 'title':x[k].title, 'category':joiner(x[k].category), 'skills':joiner(x[k].skills), 'color':color_dict[x[k].company], 'url':x[k].link}
        node_edges = [(k, i.link, {'company': x[k].company, 'title':x[k].title, 'words': x[k].neighbors[i], 'weight':len(x[k].neighbors[i])}) for i in x[k].neighbors if len(x[k].neighbors[i]) > threshold]
        edges = edges + node_edges

    G.add_edges_from(edges)
    nx.set_node_attributes(G,node_attrs)

    if rm_isolates:
        isolates = nx.isolates(G)
        G.remove_nodes_from(list(isolates))

    return G
#graph = generate_graph_network(x)


#output_file('output_graph.html', title='graph_network')
def visualize(G, inspect_edges=False):
    random.seed(42)

    output_file("networkx_graph.html")
    plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1))
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0,0))
    if not inspect_edges:
        graph_renderer.selection_policy = NodesAndLinkedEdges()
        graph_renderer.inspection_policy = NodesOnly()
        plot.add_tools(HoverTool(tooltips=[('company','@company'), ('title','@title'), ('category','@category'), ('skills','@skills'), ('url', '@url')]), TapTool(), BoxSelectTool())
    else:
        graph_renderer.selection_policy = NodesAndLinkedEdges()
        graph_renderer.inspection_policy = EdgesAndLinkedNodes()
        
        plot.add_tools(HoverTool(tooltips=[('company','@company'), ('title','@title'), ('url', '@url'), ('keywords', '@words')]), TapTool(), BoxSelectTool())
    


    graph_renderer.node_renderer.data_source.data['color'] = [i[1]['color'] for i in G.nodes(data=True)]
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color='color', )
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)
    
    plot.renderers.append(graph_renderer)

    show(plot)
#visualize(graph)