from data import *
import heapq

class ALGO:
    # this function filters hospitals with non zero ambulances availability only
    # Time Complexity : O(number of hospitals) : linear
    def filter_empty_hospitals(self, hospitals:list[dict])->list[dict]:
        filtered = []
        for h in hospitals:
            if h["ambulances"]>0:
                filtered.append(h)
        return filtered

    # this function converts node->grid_id TO grid_id->node
    # Time Complexity : O(number of nodes) : linear
    def reverse_grid_mapping(self, node_to_grid:dict)->dict:
        ans = {}
        for node in node_to_grid:
            grid_id = node_to_grid[node]
            if (grid_id in ans):
                ans[grid_id].append(node)
            else:
                ans[grid_id] = [node]
        return ans
    
    # this function makes set of boundary nodes for efficient checking during running dijkstra
    # Time Complexity : O(number of boundary nodes) : linear
    def make_set_of_boundary_nodes(self, boundary_nodes:list[int]) -> set[int]:
        return set(boundary_nodes)
    
    # this function makes set of blocked edges for efficient checking during running dijkstra
    # Time Complexity : O(number of blocked roads) : linear
    def make_set_of_blocked_roads(self, blocked_roads:list[list[int]]):
        s = set()
        for x,y in blocked_roads:
            s.add((x, y))
        return s
    
    # this is one of the main functions which return nearest hospital to accident site in concerned graph
    def find_nearest_hospital(self, graph:list[list[int]], blocked_roads:list[list[int]], accident_node:int, hospitals:list[dict]) -> int:
        pass




    
