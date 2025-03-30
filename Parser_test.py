from hl7apy.parser import parse_message
from hl7apy.core import Group, Segment, Field
import mysql.connector
from mysql.connector import Error
import data_generator.random_names as random_names

#Establish database connection
importedDB = None
try:
    importedDB = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5770327",
        password="sPhSlG51bT",
        database="sql5770327"
    )
    
    print("MySQL Database connection successful")
except Error as err:
        print(f"Error: '{err}'")

def xor(data, key):
    # Make sure the key is a single character (e.g., a letter or number)
    key = ord(key)  # Convert the key to its ASCII value (int)
    
    # XOR each character with the key and return the result
    result = ''.join(chr(ord(char) ^ key) for char in data)
    
    return result

def execute(connection, msg, vals):
    cursor = connection.cursor()
    try:
        cursor.execute(msg, vals)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")

#MAIN: read file
with open('source_hl7_messages_v2.hl7', 'r') as hl7_input:
    text = hl7_input.read()
    messages = text.split("MSH")
    
    # Read each line in the file
    for line in messages[4644:]:
        line = "MSH" + line
        msg = parse_message(line.replace("\n", "\r"), find_groups=True, validation_level=2)

        date = msg.msh.MSH_7.value
        pid = msg.pid
        MRN = pid.PID_3.PID_3_1.value
        encryptedMRN = xor(MRN, 'x')
        date = pid.PID_7.PID_7_1.value[:4]
        if date == '':
            date = '2001'
        fake_person = random_names.generate_person(encryptedMRN, pid.PID_8.value, pid.PID_11.PID_11_4.value, int(date))

        #if MRN exists, add msg to tex`
        #SELECT COUNT(*) as count FROM Program WHERE department_id = 1;
        askMRN = "SELECT * FROM `Patient_Info` WHERE MRN = %s;"
        cursor = importedDB.cursor()
        record = ""
        try:
            cursor.execute(askMRN, (encryptedMRN,))
            record = cursor.fetchone()
            importedDB.commit()
        except Error as err:
            print(f"Error: '{err}'")

        #make new record if new mrn
        if not record:
            #PID_Arr = [mrn,first_name, last_name, _birthday, sex, street_address, _city, _county, state, _phone, email_address, act_no, _ssn]pid.PID_11.PID_11_4.value, pid.PID_7.PID_7_1.value.year)
            
            sql = "INSERT INTO Patient_Info (`MRN`, `lastName`, `DOB`, `gender`, `alias`,  `phoneNum`, `accountNum`, `ssn`, `Message_List`, `Dr_ID`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val = (encryptedMRN, fake_person[2], fake_person[3], pid.PID_8.value, pid.PID_9.value, pid.PID_13.value, pid.PID_18.value, pid.PID_19.value, line, msg.pv1.PV1_7.value)
            execute(importedDB, sql, val)
        #update
        else:
            sql = "UPDATE Patient_Info set `Message_List`=%s where MRN = %s;"
            values = (str(record) + '\n' + str(line), MRN)
            execute(importedDB, sql, values)
        

        #get object back
        askMRN = "SELECT * FROM `Patient_Info` WHERE MRN = %s;"
        cursor = importedDB.cursor()

        try:
            cursor.execute(askMRN, (encryptedMRN,))
            record = cursor.fetchone()
            importedDB.commit()
        except Error as err:
            print(f"Error: '{err}'")

        if record:
            #update PHI
            #updating values
            new_values = []
            new_fields = []
    
            columns = [desc[0] for desc in cursor.description]
            for i, col in enumerate(columns):
                if not record[i] and col == "fullName":
                    new_fields.append("fullName")
                    pid5 = Field("PID_5")
                    pid5.pid_5_1 = fake_person[1] #fname
                    pid5.pid_5_2 = fake_person[2] #lname
                    new_values.append(pid5.value)
                
                if not record[i] and col == "lastName":
                    new_fields.append("lastName")
                    new_values.append(fake_person[2])
                if not record[i] and col =="DOB":
                    new_fields.append("DOB")
                    new_values.append(fake_person[3])
                if not record[i] and col =="gender":
                    new_fields.append("gender")
                    new_values.append(pid.PID_8.value)
                if not record[i] and col =="alias":
                    new_fields.append("alias")
                    new_values.append(pid.PID_9.value)
                if not record[i] and col =="address":
                    new_fields.append("address")
                    pid11 = Field("PID_11")
                    pid11.pid_11_1 = fake_person[5] #street
                    pid11.pid_11_3 = fake_person[6] #city
                    pid11.pid_11_9 = fake_person[7] #count
                    pid11.pid_11_4 = fake_person[8] #state
                    new_values.append(pid11.value)
                if not record[i] and col =="phoneNum":
                    new_fields.append("phoneNum")
                    new_values.append(fake_person[9])
                if not record[i] and col  =="accountNum":
                    new_fields.append("accountNum")
                    new_values.append(fake_person[11])
                if record[i] and col =="ssn":
                    new_fields.append("ssn")
                    new_values.append(fake_person[12])
                if str(record[i]) != msg.pv1.PV1_7.value:
                    new_fields.append("Dr_ID")
                    new_values.append(msg.pv1.PV1_7.value)
    
            #perform updates
            if new_fields:
                set_clause = ", ".join([f"`{field}` = %s" for field in new_fields])
                sql = f"UPDATE `Patient_Info` SET {set_clause} WHERE `MRN` = %s;"
                new_values.append(MRN)
                execute(importedDB, sql, tuple(new_values))
            
    
        #add msg record
        sql = "INSERT INTO Message (MRN, Message_Text, Date) VALUES (%s, %s, %s)"
        val = (encryptedMRN, line, date)
        execute(importedDB, sql, val)


# sql = "Select `Message_Text` from Message order by `Date`;"
# mycursor = importedDB.cursor()
# results = []
# try:
#     mycursor.execute(sql)
#     results = mycursor.fetchall()
# except Error as err:
#         print(f"Error: '{err}'")
    
# with open("messages_sorted.txt", "w") as file:
#     for row in results:
#         file.write("%s\n" % row)
    
# def execute_query(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         connection.commit()
#         print("Query successful")
#     except Error as err:
#         print(f"Error: '{err}'")



    

