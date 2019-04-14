import spacy

from Appointments import Appointments
from NLPEngine import NLP
from Response import ResponseType
from ResponseGenerator import ResponseGenerator
from parser import NameInqParser, Request


class Robot:
    def __init__(self, robot_name, save_path):
        self.robot_name = robot_name
        self.save_path = save_path
        self.appointment = None

    def introduction(self):
        return Request(self.listen("Hi my name is {}. Say hello to begin".format(self.robot_name)))

    def listen(self, question):
        return input(question + "\n")

    def speak(self, output):
        print(output)

    def handle(self, response):
        if response.type == ResponseType.ASK:
            return Request(self.listen(response.value))
        elif response.type == ResponseType.TELL or response.type == ResponseType.END:
            self.speak(response.value)
            return None
        elif response.type == ResponseType.APPOINTMENT:
            self.appointment = response.value
            s = "Can you confirm that you have an appointment with {} ?".format(' '.join(response.value.employee))
            return Request(self.listen(s))
        elif response.type == ResponseType.CONFIRM:
            Appointments.save_appointment(self.save_path, self.appointment)
            self.speak(response.value.format(' '.join(self.appointment.employee)))
            return None


if __name__ == '__main__':
    robot = Robot("Juanito", "checkins.txt")
    nlp = NLP(spacy.load('en_core_web_lg'))
    parsed_appointments = Appointments(nlp, 'appointments.txt')
    generator = ResponseGenerator(nlp, parsed_appointments)
    start = True
    while True:
        if start:
            start = False
            request = robot.introduction()
        response = generator.generate_response(request)
        request = robot.handle(response)
        if not request:
            start = True
