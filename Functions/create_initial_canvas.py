import json
import pandas as pd
import networkx as nx
from sentence_transformers import SentenceTransformer
from pathlib import Path
from scores_metric import *
from steiner_subtree_on_tree import *
from CanvasCoordinates import *
from orient_layout_by_diameter import *
from layout_to_canvas_coords import *
from build_edges_undirected_perp import *
from LeavesOneWay import *
from branches_from_the_heart import *
from BranchExpansion import *
from FirstEntryLogFile import *

def create_initial_canvas(Fraction_of_Questions=0.2,
                          MetricV=["degree"], 
                          N=20, 
                          routeCanvas="initial.canvas",
                          psi=0.3, 
                          card_width=500, 
                          card_height=120, 
                          padding=50,
                          Develop=0,
                          colorsPalette='Colors.csv'):


    AdjacencyFolder=MainFolder+'/Adjacency'
    AdjacencyMatrixFileName='adjacency_matrix_Questions-Concepts_20250730.csv'
    IdConceptsFileName='concept_id_mapping_20250730.csv'
    QuestionsConceptsDF=pd.read_csv(AdjacencyFolder+'/'+AdjacencyMatrixFileName,index_col=0)
    idsDF=pd.read_csv(AdjacencyFolder+'/'+IdConceptsFileName,index_col=0)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    QL=QuestionsConceptsDF.index
    embeddings = model.encode(QL)
    similarities = model.similarity(embeddings, embeddings)

    #GraphQ=nx.from_numpy_array(QAdjacencyMatrix)
    GraphQ=nx.from_numpy_array(np.array(similarities))
    GraphQ.remove_nodes_from(list(nx.isolates(GraphQ)))

    #mst = nx.minimum_spanning_tree(GraphQ)
    MaximumSimilarityTree=nx.maximum_spanning_tree(G=GraphQ, weight="weight")


    routeLog=routeCanvas.replace('.canvas','.xlsx')
    canvas_nodes=scores_metric(G=MaximumSimilarityTree, 
                               MetricV=MetricV,
                               N=N)
    canvas_nodes_tree=steiner_subtree_on_tree(G=MaximumSimilarityTree,
                                              terminals=canvas_nodes)
    spacing_x = card_width+padding
    ColorsDF=pd.read_csv(colorsPalette,index_col=0)
    spacing_y = card_height+padding
    nodes_json = []
    edges_json = []
    LittleTree= MaximumSimilarityTree.subgraph(canvas_nodes_tree.nodes)  # induced subgraph
    Branches_Heart_and_Leaves=branches_from_the_heart(Tree=LittleTree,
                                                      MaximumSimilarityTree=MaximumSimilarityTree)
    Leaves=Branches_Heart_and_Leaves[2]
    Heart=Branches_Heart_and_Leaves[1]
    nodes_to_render= list(LittleTree.nodes())
    pos=CanvasCoordinates(Branches_Heart_and_Leaves=Branches_Heart_and_Leaves,
                           psi=psi,
                           card_width=card_width,
                           card_height=card_height, 
                           padding=padding)
    canvas_xy=pos
    nodes_json = []  
    LeavesOnewayMatrix=LeavesOneWay(MaximumSimilarityTree=MaximumSimilarityTree,
                                    Heart=Heart,
                                    Leaves=Leaves)   
    minL_list=[]
    maxL_list=[]

    for node in nodes_to_render:
        ExpandingPotential=0
        text = str(QuestionsConceptsDF.iloc[int(node)].name) if str(node).isdigit() else str(node)
        x, y         = canvas_xy[node]
        ExtraText=''
        minL,maxL,NBranches=[0,0,0]
        if node in list(canvas_nodes):
            color=ColorsDF.iloc[0].name
        else:
            color=ColorsDF.iloc[2].name      
        color_background=ColorsDF['Complement'][color]
        if node in Leaves:            
            minL,maxL,NBranches=BranchExpansion(node=node,
                                                LeavesPathwayMatrix=LeavesOnewayMatrix)
            minL_list.append(minL)
            maxL_list.append(maxL)
            ExtraText='\nmin: '+str(minL)+'\tmax: '+str(maxL)+'\nBranches: '+str(NBranches)
            color_background="#000"
        nodes_json.append({
            "type": "text",
            "id": str(node),
            "layer": 0,
            "branches":NBranches,
            "min":minL,
            "max":maxL,
            "heart":Heart,
            "text":'id: '+str(node)+'\n'+ text+ExtraText,
            "x": int(x),
            "y": int(y),
            "width": card_width,
            "height": card_height,
            "default_color":color,
            "color": color_background
        })
        nodes_json.append({
            "type": "group",
            "id": str(node)+'G',
            "x": int(x)-padding*0.3,
            "y": int(y)-padding*0.3,            
            "width": card_width+padding*0.6,
            "height": card_height+padding*0.6,
            "color": color
        })        
        
    edges_json =build_edges_undirected_perp(LittleTree, nodes_json, card_w=card_width, card_h=card_height)

    data = {"nodes": nodes_json, "edges": edges_json}

    Path(routeCanvas).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    StatusDF=FirstEntryLogFile(LittleTree=LittleTree,
                               MaximumSimilarityTree=MaximumSimilarityTree,
                               routeLog=routeLog,
                               Leaves=Leaves,
                               minL_list=minL_list,
                               maxL_list=maxL_list,
                               Fraction_of_Questions=Fraction_of_Questions)
    return StatusDF
