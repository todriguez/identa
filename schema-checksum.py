import hashlib
import json

schema = {
  "version": "1.0",
  "fields": [
    "FirstName",
    "LastName",
    "DOB",
    "HouseNumber",
    "StreetAddress",
    "Suburb",
    "Postcode",
    "Phone",
    "Email",
    "FatherFirstName",
    "FatherLastName",
    "FatherDOB",
    "MotherFirstName",
    "MotherLastName",
    "MotherDOB",
    "Nationality"
  ]
}

schema_json = json.dumps(schema, sort_keys=True)
checksum = hashlib.sha256(schema_json.encode()).hexdigest()
print(f"Schema Checksum: {checksum}")
