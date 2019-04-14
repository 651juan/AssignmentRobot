from datetime import datetime


class Appointments:

    def __init__(self, nlp, file_path):
        self.nlp = nlp
        self.appointments = self.load_appointments(file_path)

    def __repr__(self):
        return ",".join([repr(app) for app in self.appointments])

    def __getitem__(self, index):
        return self.appointments[index]

    def load_appointments(self, file_path):
        parsed_appointments = self.extract_appointments(file_path)
        self.nlp.add_name_rules_to_nlp(parsed_appointments)
        return parsed_appointments

    @staticmethod
    def extract_appointments(file_path):
        lines = open(file_path).read().splitlines()
        no_of_appointments = int(lines[0].split(' ')[1])
        parsed_appointments = []
        for x in range(no_of_appointments):
            id = lines[(3 * x) + 1].split(' ')[1]
            visitor = lines[(3 * x) + 2].split(' ')[1:]
            employee = lines[(3 * x) + 3].split(' ')[1:]
            parsed_appointments.append(Appointment(id, visitor, employee))
        return parsed_appointments

    @staticmethod
    def save_appointment(file_path, appointment):
        with open(file_path, "a") as myfile:
            myfile.write(" ".join([appointment.id, datetime.utcnow().isoformat() + 'Z']))


class Appointment:

    def __init__(self, id, visitor, employee):
        self.id = id
        self.visitor = visitor
        self.employee = employee

    def __repr__(self):
        return "{} has an appointment with {}".format(' '.join(self.visitor), ' '.join(self.employee))
