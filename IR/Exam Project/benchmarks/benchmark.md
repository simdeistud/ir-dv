# Boolean Model implementations benchmarks
In this notebook we will perform some queries testing all the various features implemented by the IRs.


```python

import sys
from pathlib import Path
ROOT = Path.cwd().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

```


```python
from src.index import *
from src.IR import *
from src.utils import *

path="C:\\Users\\simone\\source\\repos\\ir-dv\\IR\\Exam Project\\data\\cran.all.1400"
ir1 = BooleanIR()
ir2 = BooleanPermutermIR()
ir3 = BooleanKGRamIR(k=3)
ir1.build(path)
ir2.build(path)
ir3.build(path)
```

    [nltk_data] Downloading package punkt_tab to
    [nltk_data]     C:\Users\simone\AppData\Roaming\nltk_data...
    [nltk_data]   Package punkt_tab is already up-to-date!
    

    Adding document to index [1]
    Adding document to index [2]
    Adding document to index [3]
    ...
    Adding document to index [1398]
    Adding document to index [1399]
    Adding document to index [1400]
    

## Normal Boolean IR queries
This set of queries aims to test whether the various IRs can retrieve correctly the documents that match a normal boolean query (no wildcards).

### Single term query
A text search reveals that "statistical" only occurs in documents: 99, 110, 218, 729, 839, 1255, and 1286


```python
q1 = "statistical"
print(f"Boolean   : " + str(ir1.retrieve(q1)))
print(f"Permuterm : " + str(ir2.retrieve(q1)))
print(f"K-gram    : " + str(ir3.retrieve(q1)))
```

    Boolean   : [99, 110, 218, 729, 839, 1255, 1286]
    Permuterm : [99, 110, 218, 729, 839, 1255, 1286]
    K-gram    : [99, 110, 218, 729, 839, 1255, 1286]
    

### Single phrase query
A text search reveals that "results are given" only occurs in documents: 98, 369, 413, 475, 477, 514, 545, 558, 606, 610, 619, 632, 671, 751, 755, 776, 844, 891, 963, 1025, 1050, 1145, 1346


```python
q2 = "results are given"
print(f"Boolean   : " + str(ir1.retrieve(q2)))
print(f"Permuterm : " + str(ir2.retrieve(q2)))
print(f"K-gram    : " + str(ir3.retrieve(q2)))
```

    Boolean   : [98, 369, 413, 475, 477, 514, 545, 558, 606, 610, 619, 632, 671, 751, 755, 776, 844, 891, 963, 1025, 1050, 1145, 1346]
    Permuterm : [98, 369, 413, 475, 477, 514, 545, 558, 606, 610, 619, 632, 671, 751, 755, 776, 844, 891, 963, 1025, 1050, 1145, 1346]
    K-gram    : [98, 369, 413, 475, 477, 514, 545, 558, 606, 610, 619, 632, 671, 751, 755, 776, 844, 891, 963, 1025, 1050, 1145, 1346]
    

### Simple AND query
A text search reveals that the only document in which "newtonian" and "subsequent" both occur is 110


```python
q3 = "newtonian AND subsequent"
print(f"Boolean   : " + str(ir1.retrieve(q3)))
print(f"Permuterm : " + str(ir2.retrieve(q3)))
print(f"K-gram    : " + str(ir3.retrieve(q3)))
```

    Boolean   : [110]
    Permuterm : [110]
    K-gram    : [110]
    

### Simple OR query


```python
q4 = "newtonian OR isentropic"
print(f"Boolean   : " + str(ir1.retrieve(q4)))
print(f"Permuterm : " + str(ir2.retrieve(q4)))
print(f"K-gram    : " + str(ir3.retrieve(q4)))
```

    Boolean   : [20, 27, 28, 35, 36, 58, 64, 97, 110, 118, 122, 144, 169, 232, 276, 317, 360, 370, 372, 423, 473, 495, 567, 593, 634, 635, 688, 689, 719, 775, 814, 947, 949, 999, 1000, 1005, 1011, 1037, 1110, 1124, 1157, 1186, 1191, 1205, 1218, 1231, 1238, 1248, 1258, 1274, 1304, 1307, 1310, 1319, 1356]
    Permuterm : [20, 27, 28, 35, 36, 58, 64, 97, 110, 118, 122, 144, 169, 232, 276, 317, 360, 370, 372, 423, 473, 495, 567, 593, 634, 635, 688, 689, 719, 775, 814, 947, 949, 999, 1000, 1005, 1011, 1037, 1110, 1124, 1157, 1186, 1191, 1205, 1218, 1231, 1238, 1248, 1258, 1274, 1304, 1307, 1310, 1319, 1356]
    K-gram    : [20, 27, 28, 35, 36, 58, 64, 97, 110, 118, 122, 144, 169, 232, 276, 317, 360, 370, 372, 423, 473, 495, 567, 593, 634, 635, 688, 689, 719, 775, 814, 947, 949, 999, 1000, 1005, 1011, 1037, 1110, 1124, 1157, 1186, 1191, 1205, 1218, 1231, 1238, 1248, 1258, 1274, 1304, 1307, 1310, 1319, 1356]
    

### Simple NOT query
The only documents that do not contain the term "the" are: 405, 557, 1138


```python
q5 = "NOT the"
print(f"Boolean   : " + str(ir1.retrieve(q5)))
print(f"Permuterm : " + str(ir2.retrieve(q5)))
print(f"K-gram    : " + str(ir3.retrieve(q5)))
```

    Boolean   : [405, 557, 1138]
    Permuterm : [405, 557, 1138]
    K-gram    : [405, 557, 1138]
    

### Complex Boolean query
This query should return a union of queries q3 and q5


```python
q6 = "(newtonian AND subsequent) OR NOT the"
print(f"Boolean   : " + str(ir1.retrieve(q6)))
print(f"Permuterm : " + str(ir2.retrieve(q6)))
print(f"K-gram    : " + str(ir3.retrieve(q6)))
```

    Boolean   : [110, 405, 557, 1138]
    Permuterm : [110, 405, 557, 1138]
    K-gram    : [110, 405, 557, 1138]
    

## Wildcard Boolean IR queries
This set of queries aims to test whether the various IRs can retrieve correctly the documents that match a query which contains wildcards.
Of course, the base Boolean IR doesn't support wildcards, so it is excluded from these tests.

### Prefix wildcard query
In the Cranfield corpus, this query should only find matches for "statistic", "statistics", or "statistically"


```python
q7 = "statistic*"
vanilla = sorted(set(ir1.retrieve("statistic")).union(set(ir1.retrieve("statistical"))).union(set(ir1.retrieve("statistics"))).union(set(ir1.retrieve("statistically"))))
permuterm = ir2.retrieve(q7)
kgram = ir3.retrieve(q7)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [99, 110, 218, 558, 729, 839, 1051, 1255, 1286]
    Permuterm : [99, 110, 218, 558, 729, 839, 1051, 1255, 1286]
    K-gram    : [99, 110, 218, 558, 729, 839, 1051, 1255, 1286]
    

### Postfix wildcard query
In the Cranfield corpus, this query should only find matches for "upstream" and "slipstream"


```python
q8 = "*pstream" # only matches should be upstream, slipstream
vanilla = sorted(set(ir1.retrieve("upstream")).union(set(ir1.retrieve("slipstream"))))
permuterm = ir2.retrieve(q8)
kgram = ir3.retrieve(q8)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [1, 53, 111, 187, 189, 190, 276, 291, 294, 364, 409, 410, 453, 457, 459, 472, 484, 490, 526, 529, 560, 605, 636, 656, 696, 697, 757, 933, 979, 987, 989, 994, 1064, 1089, 1090, 1091, 1092, 1094, 1144, 1164, 1165, 1166, 1202, 1203, 1205, 1240, 1261, 1302, 1364, 1367, 1382, 1383]
    Permuterm : [1, 53, 111, 187, 189, 190, 276, 291, 294, 364, 409, 410, 453, 457, 459, 472, 484, 490, 526, 529, 560, 605, 636, 656, 696, 697, 757, 933, 979, 987, 989, 994, 1064, 1089, 1090, 1091, 1092, 1094, 1144, 1164, 1165, 1166, 1202, 1203, 1205, 1240, 1261, 1302, 1364, 1367, 1382, 1383]
    K-gram    : [1, 53, 111, 187, 189, 190, 276, 291, 294, 364, 409, 410, 453, 457, 459, 472, 484, 490, 526, 529, 560, 605, 636, 656, 696, 697, 757, 933, 979, 987, 989, 994, 1064, 1089, 1090, 1091, 1092, 1094, 1144, 1164, 1165, 1166, 1202, 1203, 1205, 1240, 1261, 1302, 1364, 1367, 1382, 1383]
    

### Middle wildcard query
In the Cranfield corpus, this query should only find matches for "aerodynamic", "aerothermodynamic", "aeronautic", and "aeroelastic"


```python
q9 = "aero*ic"
vanilla = sorted(set(ir1.retrieve("aerodynamic")).union(set(ir1.retrieve("aeronautic"))).union(set(ir1.retrieve("aerothermodynamic"))).union(set(ir1.retrieve("aeroelastic"))))
permuterm = ir2.retrieve(q9)
kgram = ir3.retrieve(q9)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [5, 12, 13, 14, 29, 32, 33, 36, 44, 51, 52, 66, 73, 77, 78, 95, 120, 129, 137, 141, 142, 163, 164, 172, 184, 185, 202, 203, 204, 205, 225, 272, 277, 284, 287, 297, 329, 337, 342, 356, 357, 379, 390, 391, 406, 415, 434, 441, 442, 452, 453, 464, 481, 486, 499, 530, 536, 544, 546, 567, 592, 598, 599, 606, 608, 624, 625, 627, 632, 635, 638, 650, 658, 662, 671, 685, 688, 689, 698, 704, 707, 708, 709, 711, 712, 715, 716, 717, 719, 746, 748, 749, 753, 759, 780, 781, 783, 794, 798, 801, 812, 813, 814, 815, 859, 860, 861, 875, 877, 886, 892, 894, 896, 899, 917, 919, 925, 927, 939, 947, 972, 978, 981, 982, 999, 1005, 1008, 1064, 1066, 1089, 1104, 1112, 1115, 1147, 1156, 1162, 1163, 1164, 1195, 1197, 1209, 1213, 1244, 1246, 1259, 1272, 1274, 1289, 1291, 1305, 1314, 1319, 1320, 1328, 1332, 1333, 1334, 1335, 1336, 1339, 1340, 1342, 1343, 1345, 1347, 1352, 1361, 1379, 1380, 1391]
    Permuterm : [5, 12, 13, 14, 29, 32, 33, 36, 44, 51, 52, 66, 73, 77, 78, 95, 120, 129, 137, 141, 142, 163, 164, 172, 184, 185, 202, 203, 204, 205, 225, 272, 277, 284, 287, 297, 329, 337, 342, 356, 357, 379, 390, 391, 406, 415, 434, 441, 442, 452, 453, 464, 481, 486, 499, 530, 536, 544, 546, 567, 592, 598, 599, 606, 608, 624, 625, 627, 632, 635, 638, 650, 658, 662, 671, 685, 688, 689, 698, 704, 707, 708, 709, 711, 712, 715, 716, 717, 719, 746, 748, 749, 753, 759, 780, 781, 783, 794, 798, 801, 812, 813, 814, 815, 859, 860, 861, 875, 877, 886, 892, 894, 896, 899, 917, 919, 925, 927, 939, 947, 972, 978, 981, 982, 999, 1005, 1008, 1064, 1066, 1089, 1104, 1112, 1115, 1147, 1156, 1162, 1163, 1164, 1195, 1197, 1209, 1213, 1244, 1246, 1259, 1272, 1274, 1289, 1291, 1305, 1314, 1319, 1320, 1328, 1332, 1333, 1334, 1335, 1336, 1339, 1340, 1342, 1343, 1345, 1347, 1352, 1361, 1379, 1380, 1391]
    K-gram    : [5, 12, 13, 14, 29, 32, 33, 36, 44, 51, 52, 66, 73, 77, 78, 95, 120, 129, 137, 141, 142, 163, 164, 172, 184, 185, 202, 203, 204, 205, 225, 272, 277, 284, 287, 297, 329, 337, 342, 356, 357, 379, 390, 391, 406, 415, 434, 441, 442, 452, 453, 464, 481, 486, 499, 530, 536, 544, 546, 567, 592, 598, 599, 606, 608, 624, 625, 627, 632, 635, 638, 650, 658, 662, 671, 685, 688, 689, 698, 704, 707, 708, 709, 711, 712, 715, 716, 717, 719, 746, 748, 749, 753, 759, 780, 781, 783, 794, 798, 801, 812, 813, 814, 815, 859, 860, 861, 875, 877, 886, 892, 894, 896, 899, 917, 919, 925, 927, 939, 947, 972, 978, 981, 982, 999, 1005, 1008, 1064, 1066, 1089, 1104, 1112, 1115, 1147, 1156, 1162, 1163, 1164, 1195, 1197, 1209, 1213, 1244, 1246, 1259, 1272, 1274, 1289, 1291, 1305, 1314, 1319, 1320, 1328, 1332, 1333, 1334, 1335, 1336, 1339, 1340, 1342, 1343, 1345, 1347, 1352, 1361, 1379, 1380, 1391]
    

### Wildcard phrase query
In the Cranfield corpus, this query should only find matches for "aerodynamic and" and "aerodynamics and"


```python
q10 = "aerodynamic* and"
vanilla = sorted(set(ir1.retrieve("aerodynamic and")).union(set(ir1.retrieve("aerodynamics and"))))
permuterm = ir2.retrieve(q10)
kgram = ir3.retrieve(q10)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [44, 634, 1314, 1331, 1347]
    Permuterm : [44, 634, 1314, 1331, 1347]
    K-gram    : [44, 634, 1314, 1331, 1347]
    

### Multiple wildcards query
In the Cranfield corpus, this query should only find matches for "necessary", "necessarily", "unnecessary" and "unnecessarily"


```python
q11 = "*necessar*"
vanilla = sorted(set(ir1.retrieve("necessary")).union(set(ir1.retrieve("necessarily"))).union(set(ir1.retrieve("unnecessary"))).union(set(ir1.retrieve("unnecessarily"))))
permuterm = ir2.retrieve(q11)
kgram = ir3.retrieve(q11)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [2, 17, 42, 44, 49, 82, 94, 147, 158, 179, 184, 188, 196, 202, 212, 214, 216, 217, 220, 231, 249, 315, 329, 341, 349, 355, 356, 368, 406, 412, 417, 470, 480, 518, 529, 551, 552, 640, 645, 652, 665, 710, 721, 739, 777, 796, 800, 874, 893, 904, 927, 946, 986, 1025, 1042, 1117, 1197, 1209, 1216, 1246, 1248, 1251, 1252, 1257, 1280, 1302, 1325, 1342, 1343, 1361, 1387, 1392, 1398]
    Permuterm : [2, 17, 42, 44, 49, 82, 94, 147, 158, 179, 184, 188, 196, 202, 212, 214, 216, 217, 220, 231, 249, 315, 329, 341, 349, 355, 356, 368, 406, 412, 417, 470, 480, 518, 529, 551, 552, 640, 645, 652, 665, 710, 721, 739, 777, 796, 800, 874, 893, 904, 927, 946, 986, 1025, 1042, 1117, 1197, 1209, 1216, 1246, 1248, 1251, 1252, 1257, 1280, 1302, 1325, 1342, 1343, 1361, 1387, 1392, 1398]
    K-gram    : [2, 17, 42, 44, 49, 82, 94, 147, 158, 179, 184, 188, 196, 202, 212, 214, 216, 217, 220, 231, 249, 315, 329, 341, 349, 355, 356, 368, 406, 412, 417, 470, 480, 518, 529, 551, 552, 640, 645, 652, 665, 710, 721, 739, 777, 796, 800, 874, 893, 904, 927, 946, 986, 1025, 1042, 1117, 1197, 1209, 1216, 1246, 1248, 1251, 1252, 1257, 1280, 1302, 1325, 1342, 1343, 1361, 1387, 1392, 1398]
    

### Multiple wildcards phrase query
In the Cranfield corpus, this query should only find matches for "necessary to", "necessarily to", "unnecessary to" and "unnecessarily to"


```python
q12 = "*necessar* to"
vanilla = sorted(set(ir1.retrieve("necessary to")).union(set(ir1.retrieve("necessarily to"))).union(set(ir1.retrieve("unnecessary to"))).union(set(ir1.retrieve("unnecessarily to"))))
permuterm = ir2.retrieve(q12)
kgram = ir3.retrieve(q12)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [2, 17, 42, 94, 212, 249, 315, 341, 349, 355, 368, 412, 470, 480, 518, 552, 652, 710, 721, 739, 927, 946, 1197, 1251, 1280, 1342, 1392, 1398]
    Permuterm : [2, 17, 42, 94, 212, 249, 315, 341, 349, 355, 368, 412, 470, 480, 518, 552, 652, 710, 721, 739, 927, 946, 1197, 1251, 1280, 1342, 1392, 1398]
    K-gram    : [2, 17, 42, 94, 212, 249, 315, 341, 349, 355, 368, 412, 470, 480, 518, 552, 652, 710, 721, 739, 927, 946, 1197, 1251, 1280, 1342, 1392, 1398]
    

### Multiple wildcards phrase Boolean query
In the Cranfield corpus, this query should only find matches for documents 212, 946, and 1342


```python
q13 = "*necessar* to AND total"
vanilla = sorted(set(ir1.retrieve("necessary to AND total")).union(set(ir1.retrieve("necessarily to AND total"))).union(set(ir1.retrieve("unnecessary to AND total"))).union(set(ir1.retrieve("unnecessarily to AND total"))))
permuterm = ir2.retrieve(q13)
kgram = ir3.retrieve(q13)
print(f"Vanilla   : " + str(vanilla))
print(f"Permuterm : " + str(permuterm))
print(f"K-gram    : " + str(kgram))
```

    Vanilla   : [212, 946, 1342]
    Permuterm : [212, 946, 1342]
    K-gram    : [212, 946, 1342]
    
