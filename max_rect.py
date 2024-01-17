from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Matrix (BaseModel):
    matrix: List[List[int]]

class Rectangle (BaseModel):
    area: int
    number: int

@app.post("/largest-rectangle", response_model=Rectangle)
def largest_rectangle (matrix: Matrix = Body (...)):
    max_area = 0
    max_number = 0
    
    
    def max_rect (row: List[int]):
        nonlocal max_area, max_number
        stack = []
        i = 0
        while i < len (row):
            if not stack or row [i] >= row [stack [-1]]:
                stack.append (i)
                i += 1
            else:
                top = stack.pop ()
                area = row [top] * (i if not stack else i - stack [-1] - 1)
                if area > max_area:
                    max_area = area
                    max_number = row [top]
        while stack:
            top = stack.pop ()
            area = row [top] * (i if not stack else i - stack [-1] - 1)
            if area > max_area:
                max_area = area
                max_number = row [top]
    for row in matrix.matrix:
        max_rect (row)

    return jsonable_encoder (Rectangle (area=max_area, number=max_number))
