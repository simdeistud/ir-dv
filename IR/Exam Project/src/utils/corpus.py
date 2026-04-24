from document import Document

class Corpus:
    def __init__(self, path: str):
        self.documents = []
        with open(path) as f:
            self.documents = parse_NTIS(path)


def parse_NTIS(path: str) -> list[Document]:
    documents = []
    doc = {}
    current_tag = None

    tag_map = {
        "I": "docID",
        "T": "title",
        "A": "authors",
        "B": "metadata",
        "W": "text"
    }
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            # New document starts
            if line.startswith(".I"):
                if doc:
                    # finalize previous document
                    for k in doc:
                        doc[k] = doc[k].strip()
                    documents.append(Document(doc["docID"], doc["title"], doc["authors"], doc["metadata"], doc["text"]))
                doc = {"I": line[2:].strip()}
                current_tag = "I"
            # Tag line (e.g. ".T", ".W", ...)
            elif line.startswith(".") and len(line) == 2:
                current_tag = line[1]
                doc[current_tag] = ""
            # Content line
            elif current_tag:
                doc[tag_map[current_tag]] += line + " "

        # append last document
        if doc:
            for k in doc:
                doc[k] = doc[k].strip()
            documents.append(Document(doc["docID"], doc["title"], doc["authors"], doc["metadata"], doc["text"]))

    return documents