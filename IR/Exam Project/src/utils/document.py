class Document:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
    def __str__(self):
        return self.raw_text
    
class CranfieldDocument(Document):
    def __init__(self, raw_text: str):
        super().__init__(raw_text)
        fields = self._parse(self.raw_text)
        self.docID = fields["I"]
        self.title = fields["T"]
        self.authors = fields["A"]
        self.metadata = fields["B"]
        self.main_text = fields["W"]
        print(self)    

    @staticmethod
    def _parse(raw_text: str) -> dict[str, str]:
        fields: dict[str, str] = {}
        current_tag = None
        for line in raw_text.splitlines():
            line = line.rstrip()
            # Document starts
            if line.startswith(".I"):
                fields["I"] = line[2:].strip()
                current_tag = "I"
            # Tag line (e.g. ".T", ".W", ...)
            elif line.startswith(".") and len(line) == 2:
                current_tag = line[1]
                fields[current_tag] = ""
            # Content line
            elif current_tag:
                fields[current_tag] += f"{line} "
        return fields
    
    def __str__(self):
        return f"docID : {self.docID}\n" + f"title : {self.title}\n" + f"main_text : {self.main_text}\n" + f"authors : {self.authors}\n" + f"metadata : {self.metadata}\n"