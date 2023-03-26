from pathlib import Path
from time import time_ns
from typing import *

from ortools.init import pywrapinit
from ortools.linear_solver import pywraplp

# scip gurobi cplex xpress

def gen_substring_set(s: str) -> Set[str]:
  res: Set[str] = set()

  for i in range(len(s)):
    for j in range(i+1,len(s)+1):
      res.add(s[i:j])

  return res

def get_ocurrence_indices(S: str, pattern: str):
  res = []
  for i in range(len(S)):
    if S[i:i+len(pattern)] == pattern:
      res.append(i)
  return res

def gen_common_blocks(S1: str, S2: str, T: Set[str]) -> Dict[str, List[Tuple[int,int]]]:
  blocks: Dict[str, List[Tuple[int,int]]] = {}
  
  for t in T:
    pos_of_t_in_S1 = get_ocurrence_indices(S1, t)
    pos_of_t_in_S2 = get_ocurrence_indices(S2, t)
  
    for i in pos_of_t_in_S1:
      for j in pos_of_t_in_S2:
        if t in blocks:
          blocks[t].append((i,j))
        else:
          blocks[t] = [(i,j)]
        
  return blocks

def main():
  folder_path = (Path("..") / "instancesMCSP" / "random")
  res_file = Path('resultados_cb.csv').open('w')
  
  for i in range(1,4):
    dataset_path = folder_path / f"Dataset_Group0{i}"
    for solver_str in ["CPLEX", "GUROBI", "SCIP", "CBC"]:
      for instance in dataset_path.glob("*.dat"):
        with instance.open('r') as file:
          print(f'{solver_str} running {dataset_path.name}')

          lines = file.readlines()
          S1 = lines[4].strip()
          S2 = lines[5].strip()
          
          N = len(S1)
          SUBS_OF_S1 = gen_substring_set(S1)
          SUBS_OF_S2 = gen_substring_set(S2)
          T: Set[str] = set.intersection(SUBS_OF_S1, SUBS_OF_S2)
          B = gen_common_blocks(S1, S2, T)
          
          file.close()
          
          for _ in range(31):
            BEGIN_TIME_IN_NS = time_ns()
            solver = pywraplp.Solver.CreateSolver(solver_str)
            if solver is None:
              return
          
            # initializing the variables
            x = {}
            for t_idx, t in enumerate(T):
              for b in B[t]:
                x[t_idx,b[0],b[1]] = solver.BoolVar(f'x[{t_idx},{b[0]},{b[1]}]')
            #print('Number of variables =', solver.NumVariables())
            
            # first constraint
            for j in range(N):
              blocks_at_pos_j = []
              for t_idx, t in enumerate(T):
                for b in B[t]:
                  if b[0] <= j < (b[0] + len(t)):
                    blocks_at_pos_j.append(x[t_idx, b[0], b[1]])
        
              solver.Add(solver.Sum(blocks_at_pos_j) == 1)
            
            # second contraint
            for j in range(N):
              blocks_at_pos_j = []
              for t_idx, t in enumerate(T):
                for b in B[t]:
                  if b[1] <= j < (b[1] + len(t)):
                    blocks_at_pos_j.append(x[t_idx, b[0], b[1]])
              
              solver.Add(solver.Sum(blocks_at_pos_j) == 1)
              
            # objective functions
            objetive_terms = []
            for t_idx, t in enumerate(T):
              for b in B[t]:
                objetive_terms.append(x[t_idx,b[0],b[1]])

            solver.Minimize(solver.Sum(objetive_terms))
            
            status = solver.Solve()
            
            TIME_SPENT_IN_NS = time_ns() - BEGIN_TIME_IN_NS
            
            if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
              VAL = solver.Objective().Value()
            else:
              VAL = -1
            
            res_file.write(f'{solver_str},{instance.name},{N},{VAL},{TIME_SPENT_IN_NS}' + '\n')
            res_file.flush()
  
  res_file.close()
      
if __name__ == '__main__':
  main()
