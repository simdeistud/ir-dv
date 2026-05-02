from .index import *
from .IR import *
from .utils import *
from .utils.query import parse_boolean_query

path="C:\\Users\\simone\\source\\repos\\ir-dv\\IR\\Exam Project\\data\\cran.all.1400"
ir1 = BooleanIR()
ir2 = BooleanPermutermIR()
ir3 = BooleanKGRamIR(k=3)
ir1.build(path)
ir2.build(path)
ir3.build(path)
# Document 1051 is the only one that contains "statistically", but does not contain "statistical", so it should appear in the results
# Document 558 is the only one that contains "statistics", but does not contain "statistical", so it should appear in the results
q1 = "statistical"
print(f"Single word query: '{q1}'")
print(f"Boolean   : " + str(ir1.retrieve(q1)))
print(f"Permuterm : " + str(ir2.retrieve(q1)))
print(f"K-gram    : " + str(ir3.retrieve(q1)))
q2 = "results are given"
print(f"Phrase query: '{q2}'")
print(f"Boolean   : " + str(ir1.retrieve(q2)))
print(f"Permuterm : " + str(ir2.retrieve(q2)))
print(f"K-gram    : " + str(ir3.retrieve(q2)))
q3 = "newtonian AND subsequent"
print(f"AND query: '{q3}'")
print(f"Boolean   : " + str(ir1.retrieve(q3)))
print(f"Permuterm : " + str(ir2.retrieve(q3)))
print(f"K-gram    : " + str(ir3.retrieve(q3)))
q4 = "newtonian OR isentropic"
print(f"OR query: '{q4}'")
print(f"Boolean   : " + str(ir1.retrieve(q4)))
print(f"Permuterm : " + str(ir2.retrieve(q4)))
print(f"K-gram    : " + str(ir3.retrieve(q4)))
q5 = "NOT the"
print(f"NOT query: '{q5}'")
print(f"Boolean   : " + str(ir1.retrieve(q5)))
print(f"Permuterm : " + str(ir2.retrieve(q5)))
print(f"K-gram    : " + str(ir3.retrieve(q5)))
q6 = "(newtonian AND subsequent) OR NOT the"
print(query.parse_boolean_query(q6))
print(f"Boolean   : " + str(ir1.retrieve(q6)))
print(f"Permuterm : " + str(ir2.retrieve(q6)))
print(f"K-gram    : " + str(ir3.retrieve(q6)))
q7 = "statistic*"
print(f"Postfix wildcard query: '{q7}'")
print(f"Permuterm : " + str(ir2.retrieve(q7)))
print(f"K-gram    : " + str(ir3.retrieve(q7)))
q8 = "*pstream" # only matches should be upstream, slipstream
print(f"Prefix wildcard query: '{q8}'")
print(f"Permuterm : " + str(ir2.retrieve(q8)))
print(f"K-gram    : " + str(ir3.retrieve(q8)))
q9 = "aero*ic" # only matches should be aerodynamic, aeronautic, aeroelastic
print(f"Middle wildcard query: '{q9}'")
print(f"Permuterm : " + str(ir2.retrieve(q9)))
print(f"K-gram    : " + str(ir3.retrieve(q9)))
q10 = "*necessar*" # only matches should be necessary, necessarily, unnecessary, unnecessarily
print(f"Multiple wildcard query: '{q10}'")
print(f"K-gram    : " + str(ir3.retrieve(q10)))
#print("statistics : " + str(ir3.retrieve(ir3.prepare_query(q2))))
#print("statistically : " + str(ir3.retrieve(ir3.prepare_query(q3))))
#print("statistic* : " + str(ir3.retrieve(ir3.prepare_query(q4))))

#q1 = "*stream AND downward"
#q2 = "*stream of"
#print(f"{q1} : " + str(ir3.retrieve(ir3.prepare_query(q1))))
#print(f"{q2} : " + str(ir3.retrieve(ir3.prepare_query(q2))))


