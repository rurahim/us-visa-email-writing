# models/applicant.py
class Applicant:
    def __init__(self, name, visa_type, message, event_date=None):
        self.name = name
        self.visa_type = visa_type
        self.message = message
        self.event_date = event_date
