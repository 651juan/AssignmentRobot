from enum import Enum

from Response import ResponseType
from parser import IntroParser, AppInqParser, NameInqParser, VerifyParser


class States(Enum):
    INTRO = 1
    APPOINTMENT_INQUIRY = 2
    NAME_INQUIRY = 3
    APPOINTMENT_VERIFY = 4


class ResponseGenerator:

    def __init__(self, nlp, parsed_appointments):
        self.nlp = nlp
        self.parsed_appointments = parsed_appointments
        self.states = [States.APPOINTMENT_VERIFY, States.NAME_INQUIRY, States.APPOINTMENT_INQUIRY, States.INTRO]
        self.intro_parser = IntroParser()
        self.app_parser = AppInqParser()
        self.name_parser = NameInqParser(parsed_appointments)
        self.verify_parser = VerifyParser()

    def reset_conversation(self):
        self.states = [States.APPOINTMENT_VERIFY, States.NAME_INQUIRY, States.APPOINTMENT_INQUIRY, States.INTRO]

    def get_parser(self, state):
        if state == States.INTRO:
            return self.intro_parser
        if state == States.APPOINTMENT_INQUIRY:
            return self.app_parser
        if state == States.NAME_INQUIRY:
            return self.name_parser
        if state == States.APPOINTMENT_VERIFY:
            return self.verify_parser

    def generate_response(self, request):
        parser = self.get_parser(self.states[-1])
        request.parsed = self.nlp.run(request.original)
        response = parser.handle(request)
        if response.state_change:
            self.states.pop()
        if response.type == ResponseType.END or len(self.states) == 0:
            self.reset_conversation()
        return response
