from .index import *
from .IR import *
from .utils import *
from .utils.query import parse_boolean_query

ir = BooleanIR(path="C:/Users/s248508/PycharmProjects/ir-dv/IR/Exam Project/data/cran.all.1400")
#index.save(path="C:/Users/s248508/PycharmProjects/ir-dv/IR/Exam Project/data/idx.json")
#print(corpus.documents[500])
#print(index.terms["detachment"])
q1 = "results"
q2 = "results are given"
q3 = "results OR method"
q4 = "NOT results"
q5 = "results AND (experimental AND method)"

print(parse_boolean_query(q2))

print(ir.retrieve(ir.prepare_query(q2)))

ir2 = BooleanPermutermIR(path="C:/Users/s248508/PycharmProjects/ir-dv/IR/Exam Project/data/cran.all.1400")
# Document 1051 is the only one that contains "statistically", but does not contain "statistical", so it should appear in the results
# Document 558 is the only one that contains "statistics", but does not contain "statistical", so it should appear in the results
q1 = "statistical"
q2 = "statistics"
q3 = "statistically"
q4 = "statistic*"
print("statistic : " + str(ir2.retrieve(ir2.prepare_query(q1))))
print("statistics : " + str(ir2.retrieve(ir2.prepare_query(q2))))
print("statistically : " + str(ir2.retrieve(ir2.prepare_query(q3))))
print("statistic* : " + str(ir2.retrieve(ir2.prepare_query(q4))))

q1 = "*stream AND downward"
q2 = "*stream of"
print(f"{q1} : " + str(ir2.retrieve(ir2.prepare_query(q1))))
print(f"{q2} : " + str(ir2.retrieve(ir2.prepare_query(q2))))





