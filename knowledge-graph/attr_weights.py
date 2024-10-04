import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def add_nodes(graph, nodes, node_type):
    for node in nodes:
        graph.add_node(
            f"{node_type}_{node['id']}", 
            type=node_type, 
            name=node.get('name'), 
            description=node.get('description'), 
            link=node.get('linkToStandard')
        )

def add_edges(graph, relationships, from_type, to_type, edge_attrs):

    # normlize = lambda tag: tag.replace('(', '').replace(')', '').replace(',', '').lower()
    
    for relation in relationships:
        
        if from_type=="ciodId":
            from_id = f"ciod_{relation[from_type]}"
            to_id = f"module_{relation[to_type]}"  
        else:
            from_id = f"module_{relation[from_type]}" 
            tmp = relation[to_type].split(":")
            if len(tmp) == 2:
                to_id = f"attribute_{tmp[1]}"
            else:
                continue
        
        relationship_attrs = {key: relation[key] for key in edge_attrs if key in relation}

        graph.add_edge(
            from_id, 
            to_id, 
            **relationship_attrs
        )

def build_dicom_graph(ciods_file, modules_file, attributes_file, ciod_to_modules_file, module_to_attributes_file):

    ciods = load_json(ciods_file)
    modules = load_json(modules_file)
    attributes = load_json(attributes_file)
    ciod_to_modules = load_json(ciod_to_modules_file)
    module_to_attributes = load_json(module_to_attributes_file)

    G = nx.DiGraph()

    add_nodes(G, ciods, "ciod")
    add_nodes(G, modules, "module")
    add_nodes(G, attributes, "attribute")

    add_edges(G, ciod_to_modules, "ciodId", "moduleId", ["usage", "conditionalStatement", "informationEntity"])

    add_edges(G, module_to_attributes, "moduleId", "path", ["type", "linkToStandard", "description"])

    return G

def get_attribute_name(graph, attribute_id):
    return graph.nodes[attribute_id]['name'] if graph.has_node(attribute_id) else None
    
def create_lookup_table(graph, node_type):
    lookup_table = dict()
    node_ids = sorted([node_id for node_id, data in graph.nodes(data=True) if data.get('type') == node_type])

    for index, node_id in enumerate(node_ids):
        lookup_table[node_id] = index

    return lookup_table

def get_relationship_matrix(graph, source_node_type, target_node_type, lookup_table_source, lookup_table_target, attr, weighting):
    
    num_source = len(lookup_table_source)
    num_target = len(lookup_table_target)
    relationship_matrix = np.zeros((num_target, num_source), dtype=np.int64)
    
    for from_id, to_id, data in graph.edges(data=True):
        if graph.nodes[from_id].get('type') == source_node_type and graph.nodes[to_id].get('type') == target_node_type:
            from_index = lookup_table_source.get(from_id)
            to_index = lookup_table_target.get(to_id)
            
            key = data[attr]
            if from_index is not None and to_index is not None and key != "None":
                relationship_matrix[to_index, from_index] = weighting[key]
                

    return relationship_matrix

def visualize_ciods_modules_matrix(matrix):
    ones_mask = (matrix == 1)
    twos_mask = (matrix == 2)    
    plt.figure(figsize=(10, 8))  
    plt.spy(ones_mask, markersize=2, color='red')    
    plt.spy(twos_mask, markersize=2, color='black')  
    plt.gca().set_aspect('auto')    
    plt.xlim(0, matrix.shape[1])    
    plt.ylim(0, matrix.shape[0])
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel('CIOD', fontsize=12)
    plt.ylabel('Module', fontsize=12)
    plt.tight_layout()
    plt.show()

def visualize_modules_attributes_matrix(matrix):
    ones_mask = (matrix == 1)
    twos_mask = (matrix == 2)
    threes_mask = (matrix == 3)
    fours_mask = (matrix == 4)
    plt.figure(figsize=(10, 8))  
    plt.spy(ones_mask, markersize=2, color='blue')    
    plt.spy(twos_mask, markersize=2, color='orange')  
    plt.spy(threes_mask, markersize=2, color='red')   
    plt.spy(fours_mask, markersize=2, color='black')  
    plt.gca().set_aspect('auto')  
    plt.xlim(0, matrix.shape[1])  
    plt.ylim(0, matrix.shape[0])
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel('Module', fontsize=12)
    plt.ylabel('Attribute', fontsize=12)
    plt.tight_layout()
    plt.show()

def histogramm_matrix(matrix):
    plt.hist(matrix.reshape(-1), bins=[_ for _ in range(1,101)], range=(1,100), density=True)


if __name__ == "__main__":

    ciods_file = '/home/charite/guide-it/knowledge-graph/dicom/ciods.json'
    modules_file = '/home/charite/guide-it/knowledge-graph/dicom/modules.json'
    attributes_file = '/home/charite/guide-it/knowledge-graph/dicom/attributes.json'
    ciod_to_modules_file = '/home/charite/guide-it/knowledge-graph/dicom/ciod_to_modules.json'
    module_to_attributes_file = '/home/charite/guide-it/knowledge-graph/dicom/module_to_attributes.json'

    dicom_graph = build_dicom_graph(ciods_file, modules_file, attributes_file, ciod_to_modules_file, module_to_attributes_file)

    lookup_table_ciod = create_lookup_table(dicom_graph, "ciod")
    lookup_table_module = create_lookup_table(dicom_graph, "module")
    lookup_table_attribute = create_lookup_table(dicom_graph, "attribute")

    weighting = {"M": 2, "C": 1, "U":0}
    ciods_modules_matrix = get_relationship_matrix(graph=dicom_graph, 
                                                  source_node_type="ciod",
                                                  target_node_type="module",
                                                  lookup_table_source=lookup_table_ciod, 
                                                  lookup_table_target=lookup_table_module,
                                                  attr="usage",
                                                  weighting=weighting)

    weighting = {"1":4, "2":3, "1C": 2, "2C":1, "3":0}
    modules_attributes_matrix = get_relationship_matrix(graph=dicom_graph, 
                                                  source_node_type="module",
                                                  target_node_type="attribute",
                                                  lookup_table_source=lookup_table_module, 
                                                  lookup_table_target=lookup_table_attribute,
                                                  attr="type",
                                                  weighting=weighting)

    visualize_ciods_modules_matrix(ciods_modules_matrix)
    visualize_modules_attributes_matrix(modules_attributes_matrix)

    ciods_attributes_matrix = modules_attributes_matrix @ ciods_modules_matrix 

    # ciod_w = np.ones(len(lookup_table_ciod))
    ciod_w = np.zeros(len(lookup_table_ciod))
    ciod_w[29] = 1 #CT
    ciod_w[77] = 1 #MRI

    attributes_w = ciods_attributes_matrix @ ciod_w

    indices_sorted = np.argsort(attributes_w)[::-1]
    values = attributes_w[indices_sorted]
    weights = values/values.sum()
    attributes_keys = [key for key, value in lookup_table_attribute.items() if value in list(indices_sorted[:10])]
    
    attr_names = [get_attribute_name(dicom_graph, attribute_key) for attribute_key in attributes_keys]
    
    print(attr_names)
    print(weights)
        