from pathlib import Path
from .index import *
from .IR import *
from .utils import *
from .utils.query import parse_boolean_query

cranfield="./data/cran.all.1400"
boolean_saved = "./data/boolean_ir.pkl"
permuterm_saved = "./data/boolean_permuterm_ir.pkl"
kgram_saved = "./data/boolean_kgram_ir.pkl"

def main():
    index_type = input("Insert what type of IR you would like to use.\n [boolean|permuterm|k-gram] : ")
    if index_type == "boolean":
        ir = BooleanIR()
        saved = boolean_saved
    elif index_type == "permuterm":
        ir = BooleanPermutermIR()
        saved = permuterm_saved
    elif index_type == "k-gram":
        ir = BooleanKGRamIR()
        saved = kgram_saved
    else:
        raise ValueError("Invalid IR choice.")
    
    corpus = CranfieldCorpus()
    corpus.build(cranfield)
    
    if Path(saved).exists():
        print("Found IR backup, loading...")
        ir = ir.load(saved)
    else:
        print("First time running the IR, building the index...")
        ir.build(corpus)
        print("Making backup of IR...")
        ir.save(saved)
    
    while True :
        cmd = input("Submit a query or \"QUIT\" to quit : ")
        if cmd == "QUIT":
            break
        docIDs = ir.retrieve(cmd)
        if len(docIDs) == 0:
            print("No matching documents found.")
            continue
        for docID in docIDs:
            print(corpus[int(docID)-1])

main()