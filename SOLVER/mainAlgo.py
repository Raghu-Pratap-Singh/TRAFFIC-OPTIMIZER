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
            s.add((min(x,y), max(x,y)))
        return s
    
    # this is one of the main functions which return nearest hospital to accident site in concerned graph
    def find_nearest_hospital(self, graph:list[list[int]], blocked_roads:list[list[int]], accident_node:int, all_hospitals:list[dict[str, int | str]]) -> tuple[dict[str, int | str] | list[int] | set[tuple[int]]]:
        # get set of blocked roads
        blocked_set = self.make_set_of_blocked_roads(blocked_roads)
        hospitals = self.filter_empty_hospitals(all_hospitals)
        heap = [(0, accident_node)]
        visited = [float("inf")] * len(graph)
        
        visited[accident_node] = 0
        parent = [-1] * len(graph)

        while heap:

            distance, node = heapq.heappop(heap)
            
            if distance > visited[node]:
                continue
            
            for neighbour, length in graph[node]:
                if ((min(node, neighbour), max(node, neighbour))) in blocked_set:
                    continue
                next_distance = distance + length
                if next_distance<visited[neighbour]:
                    visited[neighbour] = next_distance
                    heapq.heappush(heap, (next_distance, neighbour))
                    parent[neighbour] = node
        
        nearest_hospital:dict[str, int] = None
        prev_min:int = float("inf")
        for hospital in hospitals:
            if visited[hospital["node"]] < prev_min:
                prev_min = visited[hospital["node"]]
                nearest_hospital = hospital
        if nearest_hospital is None:
            return None
        # now we will recontruct path and collect edges that are in shortest path from nearest_hospital to accident_node
        path = []
        roads_in_line:set[tuple[int]] = set()
        cur_node = nearest_hospital["node"]
        while cur_node != accident_node:
            if parent[cur_node] == -1:
                return None
            path.append(cur_node)
            roads_in_line.add((min(cur_node, parent[cur_node]), max(cur_node, parent[cur_node])))
            cur_node = parent[cur_node]
        path.append(accident_node)

        return (nearest_hospital, path, roads_in_line)

        

        
            


            



    
