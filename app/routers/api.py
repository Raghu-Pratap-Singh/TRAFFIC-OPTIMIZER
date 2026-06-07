from fastapi import APIRouter
from pydantic import BaseModel
from SOLVER.mainAlgo import client
router = APIRouter(prefix="/api", tags=["API"])

class UserRequest(BaseModel):
    graph : list[list[list[int]]]
    accident_node : int
    blocked_roads : list[list[int]]
    hospitals : list[dict[str,str | int]]
    vehicles : list[dict[str,str | int]]
    boundary_nodes : list[int]

# @router.get("/health")
# async def health_check():
#     return {
#         "status": "ok",
#         "message": "FastAPI is running"
#     }


# @router.get("/hello")
# async def hello():
#     return {
#         "message": "Hello from FastAPI"
#     }

@router.post("/calc")
async def calculate(data: UserRequest):
    # print(data)
    # for x in data:
    # print(data.graph)
    # print(type(data))
    # solving here
    tool = client()
    response = tool.solve(data)


    # return processed data mainly, ambulance path to chosen hospital, and destination nodes to grids nodes
    return response