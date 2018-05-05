import graphviz as gv
import Model

default_style = {
    'graph': {
        'rankdir': 'LR'
    },
    'nodes': {
        'shape': 'circle',

    },
    'edges': {
        'arrowhead': 'open',
    }
}

#Pasted from graphviz
def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

def ConstructGraph():
     graph = gv.Digraph(format='jpg')
     apply_styles(graph, default_style)

     for i in Model.arguments:
         graph.node(i, i)

     ed = []
     for i in Model.relations:
         ed.append((i[0],i[1]))

     print(ed)
     graph.edges(ed)
     graph.render('data/graph')


def ConstructColouredGraph(colargs):
    graph = gv.Digraph(format='jpg')
    apply_styles(graph, default_style)

    for i in Model.arguments:
        if i in colargs:
            graph.node(i, i, color = "red")

    ed = []
    for i in Model.relations:
        ed.append((i[0], i[1]))

    graph.edges(ed)
    graph.render('data/graph')