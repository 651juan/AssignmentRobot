from spacy.pipeline import EntityRuler


class NLP:
    def __init__(self, model):
        self.instance = model

    def __repr__(self):
        return repr(self.instance)

    def add_name_rules_to_nlp(self, parsed_appointments):
        ruler = EntityRuler(self.instance)
        patterns = []
        for appointment in parsed_appointments:
            pattern = {}
            visitor = appointment.visitor
            pattern['label'] = "PER"
            pattern['pattern'] = []
            for part in visitor:
                pattern['pattern'].append({"lower": part})
            patterns.append(pattern)
        ruler.add_patterns(patterns)
        self.instance.add_pipe(ruler)

    def run(self, arg):
        return self.instance(arg)
