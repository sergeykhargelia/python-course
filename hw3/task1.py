from typing import List
import numpy as np

class Matrix:
    def __init__(self, value: List[list]):
        if any(len(value_row) != len(value[0]) for value_row in value):
            raise ValueError("rows of value have different number of elements")

        self.value = value
        if len(value) == 0:
            self.shape = (0, 0)
        else:
            self.shape = (len(value), len(value[0]))
        
    def elementwise_operation(self, other, op_name, op):
        if self.shape != other.shape:
            raise ValueError(f"incompatible shapes in elementwise {op_name}: {self.shape} and {other.shape}")
        
        result = [[None for _ in range(self.shape[1])] for _ in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                result[i][j] = op(self.value[i][j], other.value[i][j])
                
        return Matrix(result)
    
    def __add__(self, other):
        return self.elementwise_operation(other, 'plus', lambda x, y: x + y)

    def __mul__(self, other):
        return self.elementwise_operation(other, 'mul', lambda x, y: x * y)

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"incompatible shapes in matmul: {self.shape} and {other.shape}")
        
        result = [[None for _ in range(self.shape[1])] for _ in range(self.shape[0])]  
        for i in range(self.shape[0]):
            for j in range(other.shape[0]):
                for k in range(self.shape[1]):
                    if result[i][k] == None:
                        result[i][k] = self.value[i][j] * other.value[j][k]
                    else:
                        result[i][k] += self.value[i][j] * other.value[j][k]

        return Matrix(result)
    
    def __str__(self):
        return '[' + '\n'.join(str(self.value[i]) for i in range(self.shape[0])) + ']'                            

def compare_with_numpy(A, B, op):
    my_result = op(Matrix(A), Matrix(B))
    numpy_result = op(np.array(A), np.array(B))

    assert(np.array_equal(my_result.value, numpy_result))

def process(A, B, op_name, op):
    compare_with_numpy(A, B, op)
    output_filename = 'artifacts/3.1/matrix_' + op_name + '.txt'
    with open(output_filename, 'w') as out:
        out.write(str(op(Matrix(A), Matrix(B))))

np.random.seed(0)
A = np.random.randint(0, 10, (10, 10))
B = np.random.randint(0, 10, (10, 10))

process(A, B, 'plus', lambda x, y: x + y)
process(A, B, 'elementwise_mul', lambda x, y: x * y)
process(A, B, 'mul', lambda x, y: x @ y)