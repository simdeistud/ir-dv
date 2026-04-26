from .index import *
from .IR import *
from .utils import *
from .utils.query import parse_boolean_query

ir = BooleanIR(path="C:/Users/simone/PycharmProjects/ir-dv/IR/Exam Project/data/cran.all.1400")
#index.save(path="C:/Users/s248508/PycharmProjects/ir-dv/IR/Exam Project/data/idx.json")
#print(corpus.documents[500])
#print(index.terms["detachment"])
q1 = "results"
q2 = "results are good AND experimental"
q3 = "results OR method"
q4 = "NOT results"
q5 = "results AND (experimental AND method)"

print(parse_boolean_query(q2))

print(ir.retrieve(ir.prepare_query(q2)))