from data import *
import heapq
import math
from collections import deque
class ALGO:
    # this function filters hospitals with non zero ambulances availability only
    # Time Complexity : O(number of hospitals) : linear
    def filter_empty_hospitals(self, hospitals:list[dict])->list[dict]:
        filtered = []
        for h in hospitals:
            if h["ambulances"]>0:
                filtered.append(h)
        return filtered

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
    def find_nearest_hospital(self, graph:list[list[list[int]]], blocked_roads:list[list[int]], accident_node:int, all_hospitals:list[dict[str, int | str]]) -> tuple[dict[str, int | str] | list[int] | set[tuple[int]]]:
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


    def bfs(self, node:int, graph:list[list[list[int]]], visited:list[int], block_size:int, node_to_block:list[int], group_number:int):
        q = deque([node])
        visited[node] = 1
        node_to_block[node] = group_number

        covered_cnt:int = 1
        while q:
            node = q.popleft()
            for neighbour, weight in graph[node]:
                if not visited[neighbour]:
                    visited[neighbour] = 1
                    covered_cnt+=1
                    # assign group
                    node_to_block[neighbour] = group_number

                    # before appending to q, check if limit reached or not
                    if covered_cnt == block_size:
                        break
                    # else, push in q
                    q.append(neighbour)
            if covered_cnt == block_size:
                break
    
    def close_root_seperator(self, graph:list[list[list[int]]]) -> tuple[list[int] | int]:
        # we will try to seperate groups of closely packed nodes in packs of root n nodes
        n:int = len(graph)
        block_size:int = math.floor(math.sqrt(n))

        # now we will bfs block_size times onlt and map them in one group : O(V + E)
        visited:list[int] = [0] * n
        
        # this list will tell node_to_block[node]->will give us the group it is assigned to
        node_to_block:list[int] = [-1] * n

        group_number:int = 0
        for node in range(n):
            if not visited[node]:
                # IMPORTANT: (V + E) "For sparse, locally connected road networks, 
                # a BFS limited to √N nodes should produce connected groups that are geographically close."
                # start bfs from here until root n nodes are covered
                # also in reality, road lengths are almost similar, so bfs will work fine
                # as we are considering graph very dense (of a district or region)
                # therefore almost root(n) + (∆) nodes will be covered in each group
                self.bfs(node, graph, visited, block_size, node_to_block, group_number)
                group_number+=1

        # now the graph isdivided into approx root(N) groups in (V + E) time complexity
        return (node_to_block, group_number)
    
    def mark_boundary_grids(self,n:int,  node_to_block:list[int], group_number:int, boundary_nodes:list[int], bloacked_roads:list[list[int]],graph:list[list[list[int]]], roads_in_line:set[tuple[int, int]]) -> list[int]:
        # get set of boundary nodes
        boundary_nodes_set:set[int] = self.make_set_of_boundary_nodes(boundary_nodes)
        blocked_set:set[tuple[int, int]] = self.make_set_of_blocked_roads(bloacked_roads)
        # now mark boundary groups with thier destination boundary nodes
        marked:list[int] = [-1] * group_number
        occured_unmarked_grid = set()
        # mark boundary node grids first
        for boundary_node in boundary_nodes:
            marked[node_to_block[boundary_node]] = boundary_node

        heap = [] #(dist, head, node)
        visited = {} # {(head, node) : min_dist}
        

        for node in range(n):
            if node_to_block[node] in occured_unmarked_grid:
                continue
            if marked[node_to_block[node]] == -1:
                
                occured_unmarked_grid.add(node_to_block[node])
                visited[(node, node)] = 0
                heapq.heappush(heap, (0, node, node))

        # now start dijkstra from unmarked grids
        while heap:
            dist, head, node = heapq.heappop(heap)

            if dist > visited[(head, node)]:
                continue
                
            if marked[node_to_block[head]]!=-1:
                continue
            
            if node in boundary_nodes_set:
                marked[node_to_block[head]] = node
                continue
            for neighbour, w in graph[node]:
                # check that this connection should not be in blcoked roads or in path of emergency vehicle
                edge:tuple[int, int] = (min(neighbour, node), max(neighbour, node))
                if (edge in blocked_set) or (edge in roads_in_line):
                    continue

                new_dist = dist + w
                key = (head, neighbour)
                if (key not in visited) or (visited[key] > new_dist):
                    visited[key] = new_dist
                    # check if this is a boundary node
                    heapq.heappush(heap, (new_dist, head, neighbour))


        #important : if marked[group] == -1, means the current group cannot currently be evacuated 
        # where marked[group_number] = target exit point
        return marked
    

        
            





            




        
    
# testing only
# S = ALGO()
# adj = [
#     [[2,3],[1,4],[4,2]], #0
#     [[0,4],[6,2],[10,2],[11,2]], #1
#     [[0,3],[10,4],[3,4],[12,4]], #2
#     [[2,4],[12,4],[5,3]], #3
#     [[0,2],[7,3],[5,4],[8,2]], #4
#     [[3,3],[4,4],[13,2],[14,2]], #5
#     [[1,2],[7,2],[9,2]], #6
#     [[4,3],[6,2],[8,3]], #7
#     [[4,2],[7,3],[9,2],[13,2],[14,2]], #8
#     [[6,2],[8,2],[11,2]], #9
#     [[1,2],[2,4],[11,4],[12,4]], #10
#     [[1,2],[9,2],[10,4]], #11
#     [[2,4],[3,4],[10,4]], #12
#     [[5,2],[8,2],[14,1]], #13
#     [[5,2],[8,2],[13,1]]  #14

# ]
# S.close_root_seperator(adj)
# hospitalss = [
#     {
#         "id": "H1",
#         "node": 4,
#         "ambulances": 2
#     },
#     {
#         "id": "H4",
#         "node": 6,
#         "ambulances": 1
#     },

#     # No ambulances available

    
#     {
#         "id": "H7",
#         "node": 8,
#         "ambulances": 0
#     }
# ]
# blocked_roads_adj = [
#     [1, 10],
#     [2, 10],
#     [4, 5]
# ]
# response = S.find_nearest_hospital(adj,blocked_roads_adj,12, hospitalss)
# for x in response:
#     print(x)