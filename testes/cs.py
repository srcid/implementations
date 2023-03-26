from pathlib import Path
from time import time_ns
from typing import *

from ortools.init import pywrapinit
from ortools.linear_solver import pywraplp


def gen_substring_set(s: str) -> Set[str]:
  res: Set[str] = set()

  for i in range(len(s)+1):
    for j in range(i+1,len(s)+1):
      res.add(s[i:j])

  return res


def gen_substring_pos(s: str, T: Set[str]) -> Dict[str, List[Tuple[int,int]]]:
  res: Dict[str, List[Tuple[int,int]]] = {}

  for i in range(len(s)+1):
    for j in range(i+1,len(s)+1):
      if s[i:j] in T:
        if s[i:j] in res:
          res[s[i:j]].append((i,j))
        else:
          res[s[i:j]] = [(i,j)]

  return res

def main():
  folder_path = (Path("..") / "instancesMCSP" / "random")
  res_file = Path('resultados_cs.csv').open('w')
  
  for i in range(1,2):
    dataset_path = folder_path / f"Dataset_Group0{i}"
    for solver_str in ["SCIP", "CBC", "GUROBI", "CPLEX"]:
      for instance in dataset_path.glob("*.dat"):
        with instance.open('r') as file:
          lines = file.readlines()
          S1 = lines[4].strip()
          S2 = lines[5].strip()
          
          N = len(S1)
          SUBS_OF_S1 = gen_substring_set(S1)
          SUBS_OF_S2 = gen_substring_set(S2)
          T = set.intersection(SUBS_OF_S1, SUBS_OF_S2)
          Q = [gen_substring_pos(S1, T), gen_substring_pos(S2, T)]
          
          file.close()
          
          for _ in range(31):
            BEGIN_TIME_IN_NS = time_ns()
            solver = pywraplp.Solver.CreateSolver(solver_str)
            if solver is None:
              return
          
            # initializing the variables
            y = {}
            for t_idx, t in enumerate(T):
              for q_idx,q in enumerate(Q):
                for k in q[t]:
                  y[t_idx,q_idx,k[0],k[1]] = solver.BoolVar(f'y[{q_idx},{t_idx},{k[0]},{k[1]}]')
            #print('Number of variables =', solver.NumVariables())
            
            # first constraint
            for t_idx, t in enumerate(T):
              partitions_of_S1 = [ y[t_idx, 0, k[0], k[1]] for k in Q[0][t] ]
              partitions_of_S2 = [ y[t_idx, 1, k[0], k[1]] for k in Q[1][t] ]

              solver.Add(solver.Sum(partitions_of_S1) == solver.Sum(partitions_of_S2))
            
            # second contraint            
            for j in range(N):
              substrings_at_pos_j_of_S1 = []
              for t_idx, t in enumerate(T):
                for k in Q[0][t]: 
                  if k[0] <= j < k[1]: # k[1] == k[0] + size(t)
                    substrings_at_pos_j_of_S1.append(y[t_idx,0,k[0],k[1]])
  
              solver.Add(solver.Sum(substrings_at_pos_j_of_S1) == 1)
            
            # third constraint
            for j in range(N):
              substrings_at_pos_j_of_S2 = []
              for t_idx, t in enumerate(T):
                for k in Q[1][t]:
                  if k[0] <= j < k[1]: # k[1] == k[0] + size(t)
                    substrings_at_pos_j_of_S2.append(y[t_idx,1,k[0],k[1]])

              solver.Add(solver.Sum(substrings_at_pos_j_of_S2) == 1)
             
            # objective functions
            objective_terms = []
            for t_idx, t in enumerate(T):
              for k in Q[0][t]:
                objective_terms.append(y[t_idx, 0, k[0], k[1]])

            solver.Minimize(solver.Sum(objective_terms))
            
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