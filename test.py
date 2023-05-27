from seq import Seq
from table import Table


n = 5
r = range(n)

seq1 = Seq(r, "seq1")
seq2 = Seq(r, "seq2")
seq3 = Seq(r, "seq3")

table = Table.from_seqs([seq1, seq2, seq3])
print(table.union(table))
