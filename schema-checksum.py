import hashlib
import json
import os

schema = {
  "version": "1.0",
  "fields": [
    {"index": 1, "name": "FirstName"},
    {"index": 2, "name": "LastName"},
    {"index": 3, "name": "DOB"},
    {"index": 4, "name": "HouseNumber"},
    {"index": 5, "name": "StreetAddress"},
    {"index": 6, "name": "Suburb"},
    {"index": 7, "name": "Postcode"},
    {"index": 8, "name": "Phone"},
    {"index": 9, "name": "Email"},
    {"index": 10, "name": "FatherFirstName"},
    {"index": 11, "name": "FatherLastName"},
    {"index": 12, "name": "FatherDOB"},
    {"index": 13, "name": "MotherFirstName"},
    {"index": 14, "name": "MotherLastName"},
    {"index": 15, "name": "MotherDOB"},
    {"index": 16, "name": "Nationality"},
    {"index": 17, "name": "MotherMaidenName"},
    {"index": 18, "name": "PlaceOfBirth"},
    {"index": 19, "name": "GraduatingPrimarySchool"},
    {"index": 20, "name": "GraduatingHighSchool"},
    {"index": 21, "name": "FirstPet"}
  ]
}

schema_json = json.dumps(schema, sort_keys=True)
checksum = hashlib.sha256(schema_json.encode()).hexdigest()
print(f"Schema Checksum: {checksum}")

# Save the schema to a file
schema_file = os.path.join(os.path.dirname(__file__), 'identa-schema.json')
with open(schema_file, 'w') as
