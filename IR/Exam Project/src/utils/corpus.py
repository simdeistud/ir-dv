from .document import Document

class Corpus:
    def __init__(self, type: str,  path: str):
        self.documents = []
        with open(path) as f:
            self.documents = parse_NTIS(path) if type == "NTIS" else parse_NTIS(path)


def parse_NTIS(path: str) -> list[Document]:
    documents = []
    doc = {}
    current_tag = None

    with open(path) as f:
        for line in f:
            line = line.rstrip()
            # New document starts
            if line.startswith(".I"):
                print(f"adding document to corpus [{line[2:].strip()}]")
                if doc:
                    # finalize previous document
                    for k in doc:
                        doc[k] = doc[k].strip()
                    documents.append(Document(doc["I"], doc["T"], doc["A"], doc["B"], doc["W"]))
                doc = {"I": line[2:].strip()}
                current_tag = "I"
            # Tag line (e.g. ".T", ".W", ...)
            elif line.startswith(".") and len(line) == 2:
                current_tag = line[1]
                doc[current_tag] = ""
            # Content line
            elif current_tag:
                doc[current_tag] += line + " "

        # append last document
        if doc:
            for k in doc:
                doc[k] = doc[k].strip()
            documents.append(Document(doc["I"], doc["T"], doc["A"], doc["B"], doc["W"]))

    return documents