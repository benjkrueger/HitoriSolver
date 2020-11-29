import time
from pprint import pprint

from cell import Cell
from hitori_v2 import Hitori, find_all_multiples_circled, find_consecutive_black_outs
import puzzle_file

# example = good
# example2 = not solved
# easy = solved
# easy2 = good

start = time.time()
b = puzzle_file.hitori_20h
a = Hitori(len(b), b)
a.print_table()
a.solve_hitori()
a.print_table()
print(time.time() - start)



"""def make_chains(self):
  dct = {}
  lst = []
  for i, row in enumerate(self.array):
    for j, col in enumerate(row):
      if self.array[i][j].circled:
        neighbors = self.get_surrounding_cells(i, j)
        for n in neighbors:
          if n is not None and n.circled and not n.black:
            self.cell_union(self.array[i][j], n)
        g = dct.get(self.cell_find(i, j))
        if g:
          dct[self.cell_find(i, j)].append((i, j))
        else:
          dct[self.cell_find(i, j)] = [(i, j)]
      elif not self.array[i][j].black and not self.array[i][j].circled:
        lst.append((i, j))
  print(dct, lst)
  return dct, lst"""