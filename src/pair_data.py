
from enum import Enum

class Types(Enum):
    DATE = 0
    INT = 1
    STRING = 2
    BOOLEAN = 3
    CHOICE = 4

class ReqTypes(Enum):
    REQ = 0
    SOFT_REQ = 1
    NOT_REQ = 2

class DataPoint:

    def __init__(self, _key, _type, _req, _value_types = None):
        self._key = _key
        self._type = _type
        self._req = _req
        if _value_types is not None:
            self._value_types = _value_types
        elif self._type == Types.BOOLEAN:
            self._value_types = ["Yes", "No"]

    def key(self):
        return self._key
    
    def data_type(self):
        return self._type
    
    def req(self):
        return self._req
    
    def value_types(self):
        try:
            return self._value_types
        except AttributeError:
            pass

    def is_req(self):
        return self._req == ReqTypes.REQ


PAIRS = [
    # ----------------------------------------------------------
    # FORM HEADER
    DataPoint(
        "Client Name / HMIS ID",
        Types.INT,
        ReqTypes.NOT_REQ
    ),
    DataPoint(
        "HMIS Consent signed", 
        Types.BOOLEAN, 
        ReqTypes.REQ,
    ),
    DataPoint(
        "Date consented", 
        Types.DATE, 
        ReqTypes.REQ
    ),
    DataPoint(
        "Assessment Location", 
        Types.DATE, 
        ReqTypes.REQ
    ),
    DataPoint(
        "Assessment Type", 
        Types.CHOICE, 
        ReqTypes.REQ,
        ["Phone", "Virtual", "In Person"]    
    ),
    DataPoint(
        "Assessment Level", 
        Types.CHOICE, 
        ReqTypes.REQ,
        ["Crisis needs assessment", "Housing needs assessment"]
    ),
    # ----------------------------------------------------------
    # IDENTIFIABLES
    DataPoint(
        "Social Security Number",
        Types.INT,
        ReqTypes.SOFT_REQ
    ),
    DataPoint(
        "Quality of SSN",
        Types.CHOICE,
        ReqTypes.SOFT_REQ,
        [
            "Full SSN reported",
            "Approximate or partial SSN reported",
            "Client doesn't know",
            "Client refused",
            "Data not collected"
        ]
    ),
    # NAME
    DataPoint(
        "Last Name",
        Types.STRING,
        ReqTypes.SOFT_REQ
    ),
    DataPoint(
        "Middle Name",
        Types.STRING,
        ReqTypes.NOT_REQ
    ),
    DataPoint(
        "Suffix",
        Types.STRING,
        ReqTypes.NOT_REQ
    ),
    DataPoint(
        "Maiden Name",
        Types.STRING,
        ReqTypes.NOT_REQ
    ),
    DataPoint(
        "First Name",
        Types.STRING,
        ReqTypes.SOFT_REQ
    ),
    DataPoint(
        "Alias",
        Types.STRING,
        ReqTypes.NOT_REQ
    ),
    DataPoint(
        "Quality of Name",
        Types.CHOICE,
        ReqTypes.SOFT_REQ,
        [
            "Full name reported",
            "Partial, street name, or code name reported",
            "Client doesn't know",
            "Client refused",
            "Data not collected"
        ]
    ),
    # Date of birth
    DataPoint(
        "Date of Birth",
        Types.DATE,
        ReqTypes.SOFT_REQ
    ),
    DataPoint(
        "DOB - Score",
        Types.INT,
        ReqTypes.NOT_REQ
    ),
    DataPoint(
        "Quality of DOB",
        Types.CHOICE,
        ReqTypes.SOFT_REQ,
        [
            "Full DOB reported",
            "Approximate or partial DOB reported",
            "Client doesn't know",
            "Client refused",
            "Data not collected"
        ]
    ),
    # Gender and pronouns
    DataPoint(
        "Gender",
        Types.CHOICE,
        ReqTypes.REQ,
        [
            "Female",
            "Male",
            "Trans Female",
            "Trans Male",
            "Gender Non-Conforming",
            "Client doesn't know",
            "Client refused",
            "Data not collected"
        ]
    ),
    DataPoint(
        "Pronouns",
        Types.STRING,
        ReqTypes.NOT_REQ,
        [
            "she/her/hers",
            "he/him/his",
            "they/them/theirs",
            "etc."  # special case
        ]
    ),
    DataPoint(
        "Ethnicity",
        Types.CHOICE,
        ReqTypes.REQ,
        [
            "Non-Hispanic/Non-Latino",
            "Hispanic/Latino",
            "Client doesn't know",
            "Client refused",
            "Data not collected"
        ]
    ),
    DataPoint(
        "Race",
        Types.CHOICE,
        ReqTypes.REQ,
        [
            "White",
            "Black or African-American",
            "Asian",
            "American Indian or Alaskan Native",
            "Native Hawaiian or other Pacific Islander",
            "Client doesn't know",
            "Client refused",
            "Data not collected"
        ]
    ),
    DataPoint(
        "Primary Language",
        Types.CHOICE,
        ReqTypes.NOT_REQ,
        [
            "English",
            "Spanish",
            "French",
            "Italian",
            "German",
            "Greek",
            "Polish",
            "Portugese",
            "Russian",
            "Swedish",
            "American Sign Language",
            "Other",  # SPECIAL CASE
            "Client doesn't know",
            "Client refused"
        ]
    )
]