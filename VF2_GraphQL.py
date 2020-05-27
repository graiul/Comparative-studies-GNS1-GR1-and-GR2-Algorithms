import copy
from collections import OrderedDict

import networkx as nx
from networkx.algorithms import isomorphism
from py2neo import Graph, Subgraph

from GenericQueryProc import GenericQueryProc
from Query_Graph_Generator import Query_Graph_Generator
from Graph_Format import Graph_Format
from timeit import default_timer as timer

# https://stackoverflow.com/questions/6537487/changing-shell-text-color-windows
# https://pypi.org/project/colorama/
from colorama import init
from colorama import Fore, Back, Style
init()