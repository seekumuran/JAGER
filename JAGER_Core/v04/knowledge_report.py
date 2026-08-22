from .serialization import dumps


class KnowledgeReport:

    def __init__(self, knowledge):
        self.knowledge = knowledge

    def generate(self):
        return [
            entry.to_dict()
            for entry in self.knowledge.all()
        ]

    def json(self):
        return dumps(
            self.generate()
        )
