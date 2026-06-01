# here we will convert grpah from frontend to DSA type graph
# nodes will be marked from 0 to n-1 in sequence
# temporary example
weighted_graph = [
    [[1,1], [5,2], [12,3]],                      # 0
    [[0,1], [2,1], [6,2]],                       # 1
    [[1,1], [3,1], [7,1]],                       # 2
    [[2,1], [4,1], [8,2], [18,4]],              # 3
    [[3,1], [9,2]],                             # 4

    [[0,2], [6,1], [10,2], [17,3]],             # 5
    [[1,2], [5,1], [7,1], [11,2]],              # 6
    [[2,1], [6,1], [8,1], [12,1], [19,3]],      # 7
    [[3,2], [7,1], [9,1], [13,1]],              # 8
    [[4,2], [8,1], [14,2]],                     # 9

    [[5,2], [11,1], [15,1], [22,3]],            # 10
    [[6,2], [10,1], [12,1], [16,2], [28,4]],    # 11
    [[7,1], [11,1], [13,1], [17,1], [0,3]],     # 12
    [[8,1], [12,1], [14,1], [18,2]],            # 13
    [[9,2], [13,1], [19,1], [26,3]],            # 14

    [[10,1], [16,1], [20,2]],                   # 15
    [[11,2], [15,1], [17,1], [21,2]],           # 16
    [[12,1], [16,1], [18,1], [22,1], [5,3]],    # 17
    [[13,2], [17,1], [19,1], [23,1], [3,4]],    # 18
    [[14,1], [18,1], [24,2], [7,3]],            # 19

    [[15,2], [21,1], [25,2]],                   # 20
    [[16,2], [20,1], [22,1], [26,2]],           # 21
    [[17,1], [21,1], [23,1], [27,1], [10,3]],   # 22
    [[18,1], [22,1], [24,1], [28,2]],           # 23
    [[19,2], [23,1], [29,1]],                   # 24

    [[20,2], [26,1]],                           # 25
    [[21,2], [25,1], [27,1], [14,3]],           # 26
    [[22,1], [26,1], [28,1]],                   # 27
    [[23,2], [27,1], [29,1], [11,4]],           # 28
    [[24,1], [28,1]]                            # 29
]
blocked_roads = [
    [17, 18],
    [18, 17],

    [18, 19],
    [19, 18],

    [18, 23],
    [23, 18],

    [13, 18],
    [18, 13]
]
cars = [
    {"id": 1, "node": 2, "destination": 29},
    {"id": 2, "node": 5, "destination": 24},
    {"id": 3, "node": 7, "destination": 20},
    {"id": 4, "node": 8, "destination": 27},
    {"id": 5, "node": 11, "destination": 25},

    {"id": 6, "node": 12, "destination": 28},
    {"id": 7, "node": 13, "destination": 21},
    {"id": 8, "node": 14, "destination": 26},
    {"id": 9, "node": 15, "destination": 24},
    {"id": 10, "node": 16, "destination": 29},

    {"id": 11, "node": 17, "destination": 0},
    {"id": 12, "node": 18, "destination": 5},
    {"id": 13, "node": 19, "destination": 1},
    {"id": 14, "node": 20, "destination": 4},
    {"id": 15, "node": 21, "destination": 8},

    {"id": 16, "node": 22, "destination": 3},
    {"id": 17, "node": 23, "destination": 6},
    {"id": 18, "node": 24, "destination": 10},
    {"id": 19, "node": 25, "destination": 11},
    {"id": 20, "node": 26, "destination": 12},

    {"id": 21, "node": 27, "destination": 7},
    {"id": 22, "node": 28, "destination": 13},
    {"id": 23, "node": 29, "destination": 15},
    {"id": 24, "node": 9, "destination": 22},
    {"id": 25, "node": 6, "destination": 18},
]
# boundary nodes
boundary_nodes = [
    5, 6, 7, 8, 9,
    25, 26, 27, 28, 29
]
# accident location
accident_node = 18



hospitals = [
    {
        "id": "H1",
        "node": 0,
        "ambulances": 2
    },
    {
        "id": "H2",
        "node": 10,
        "ambulances": 3
    },
    {
        "id": "H3",
        "node": 20,
        "ambulances": 2
    },
    {
        "id": "H4",
        "node": 29,
        "ambulances": 1
    },

    # No ambulances available

    {
        "id": "H5",
        "node": 6,
        "ambulances": 0
    },
    {
        "id": "H6",
        "node": 14,
        "ambulances": 0
    },
    {
        "id": "H7",
        "node": 22,
        "ambulances": 0
    }
]

# this is to be used after decomposing graph into groups (grids here)
node_to_grid = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0,

    5: 1, 6: 1, 7: 1, 8: 1, 9: 1,

    10: 2, 11: 2, 12: 2, 13: 2, 14: 2,

    15: 3, 16: 3, 17: 3, 18: 3, 19: 3,

    20: 4, 21: 4, 22: 4, 23: 4, 24: 4,

    25: 5, 26: 5, 27: 5, 28: 5, 29: 5
}