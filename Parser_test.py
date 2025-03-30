import hl7
# import pyodbc

# Example HL7 Message (ADT^A01)
hl7_message = "MSH|^~\&||HOSP_WS|||202502261022||ORU^R01^NURAS|508065.6796364|D|2.1\rEVN|A01|202502260903|||EFD.AJ^JORGENSEN^AMANDA^^^^|202502260903\rPID|1||W000033049|W23038|mairi^ghita^26^^^^L||19900505|F|^^^^^||^^^^^^^^|||||||W00000331191\rPV1|1|I|W.PBTRAIN^W.PB01^026|EM|||\rDRCPOELIVE^DRCPOE^LIVE^^^^MD|DRCPOELIVE^DRCPOE^LIVE^^^^MD|.DNK^KNOW^DOES^NOT^^^|MAS||||UNK|WI|N|DRCPOELIVE^DRCPOE^LIVE^^^^MD|IN||U|||||||||||||||||||HOSP_WS^|NEW HIRE TRAINING DOCUMENTATION|ADM|||202502260903||||||||DRCPOELIVE^DRCPOE^LIVE^^^^MD\rOBX|1||ZBBO32^Heart Rate BPM:||109\rOBX|2||ZBB1^Temperature F:||98.0\rOBX|3||AYYT888^Blood Pressure||74/109\rOBX|4|ABC|SS12345||Discussed lifestyle changes with ghita mairi to manage diabetes."

# Parse the HL7 message
parsed_message = hl7.parse(hl7_message)

# Extract necessary fields (this depends on the structure of your HL7 message)
PID_need = [3, 5, 7, 8, 9, 11, 13, 18, 19]
for i < len(parsed_message.segment('PID'))
    PID.append(parsed_message.segment('PID')[i][0]
    




patient_id = parsed_message.segment('PID')[3][0]  # Patient ID
patient_name = parsed_message.segment('PID')[5][0]  # Patient Name (e.g., Doe^John)
dob = parsed_message.segment('PID')[7][0]  # Date of Birth
gender = parsed_message.segment('PID')[8][0]  # Gender
alias = parsed_message.segment('PID')[9][0] # nickname
address = parsed_message.segment('PID')[11][0]  # Address
phone_number = parsed_message.segment('PID')[13][0]  # Phone Number
account_number = parsed_message.segment('PID')[18][0]
ssn = parsed_message.segment('PID')[19][0]


# # Connect to your SQL database (example using pyodbc for SQL Server)
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql5.freesqldatabase.com;DATABASE=sql5770327;UIDsql5770327;PWD=sPhSlG51bT')
# cursor = conn.cursor()

# # Insert the data into the table
# cursor.execute("""
#     INSERT INTO Patient_Info (MRN, Name, DOB, Gender, Alias, phoneNum, accountNum, ssn)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     """, 
#     12345, patient_id, patient_name, dob, gender, address, phone_number, ethnicity, 'ADT^A01', '2023-03-29 09:00:00', 'GETDATE()'
# )

# # Commit and close
# conn.commit()
# conn.close()
