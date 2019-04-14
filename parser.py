from collections import defaultdict

from spacy.lang.lex_attrs import lower

from Response import Response, ResponseType


class Request:
    def __init__(self, original, parsed=""):
        self.original = original
        self.parsed = parsed


class IntroParser(object):

    def handle(self, request):
        text = lower(request.original)
        if text == 'hello':
            response = Response()
            response.type = ResponseType.ASK
            response.value = 'Hello there, Welcome to our office. Do you have an appointment?'
            return response
        else:
            response = Response()
            response.type = ResponseType.TELL
            response.state_change = False
            response.value = 'Sorry I didn\'t get that. Could you repeat?'
            return response


class AppInqParser(object):

    def handle(self, request):
        text = lower(request.original)
        if text == 'yes':
            response = Response()
            response.type = ResponseType.ASK
            response.value = 'What is your full name?'
            return response
        elif text == 'no':
            response = Response()
            response.type = ResponseType.END
            response.value = 'Sorry, I cannot help you with other requests at the moment.'
            return response
        else:
            response = Response()
            response.type = ResponseType.TELL
            response.state_change = False
            response.value = 'Sorry I didn\'t get that. Could you repeat?'
            return response


class VerifyParser(object):

    def handle(self, request):
        text = lower(request.original)
        if text == 'yes':
            response = Response()
            response.type = ResponseType.CONFIRM
            response.value = 'Great, please have a seat in the waiting area. {} We will be with you soon.'
            return response
        elif text == 'no':
            response = Response()
            response.type = ResponseType.END
            response.value = 'Someone will be with you in a second. Please have a seat..'
            return response
        else:
            response = Response()
            response.type = ResponseType.TELL
            response.state_change = False
            response.value = 'Sorry I didn\'t get that. Could you repeat?'
            return response


class NameInqParser(object):

    def __init__(self, parsed_appointments):
        self.parsed_appointments = parsed_appointments
        self.count = 0

    # This method exists as a placeholder for future development.
    # Language specific rules can be applied as a fallback when the statistical model fails.
    def parse_rules(self, request):
        response = Response()
        response.type = ResponseType.ASK
        response.value = "Sorry, we cannot find your appointment. Could you repeat your full name?"
        response.state_change = False
        self.count = self.count + 1
        return response

    def get_appointment_based_on_name(self, entity):
        appointments = defaultdict(list)
        for appointment in self.parsed_appointments:
            no_of_mathes = len(set([e.text for e in entity]) & set(appointment.visitor))
            if no_of_mathes > 0:
                appointments[no_of_mathes].append(appointment)
        return appointments[max(appointments.keys())] if len(appointments) != 0 else []

    def parse_ents(self, request):
        response = Response()

        person_entities = [e for e in request.parsed.ents if e.label_ == 'PERSON']
        entity = person_entities[0]
        appointments = self.get_appointment_based_on_name(entity)

        if len(appointments) == 1:
            response.type = ResponseType.APPOINTMENT
            response.value = appointments[0]
            self.count = 0
        elif len(appointments) > 1:
            response.type = ResponseType.ASK
            response.value = 'We found multiple appointments with that name. Could you repeat your full name?'
            response.state_change = False
            self.count = self.count + 1
        else:
            response.type = ResponseType.ASK
            response.value = "Sorry, we cannot find your appointment. Could you repeat your full name?"
            response.state_change = False
            self.count = self.count + 1
        return response

    def handle(self, request):
        if self.count == 2:
            response = Response()
            response.type = ResponseType.END
            response.value = "Sorry, we cannot find your appointment. Please have a seat and one of our hosts will help you."
            response.state_change = False
            self.count = 0
            return response

        if len(request.parsed.ents) <= 0:
            return self.parse_rules(request)
        else:
            return self.parse_ents(request)
