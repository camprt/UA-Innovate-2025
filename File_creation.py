from hl7apy.parser import parse_message
from hl7apy.core import Group, Segment
import mysql.connector
from mysql.connector import Error

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

def execute(connection, msg, vals):
    cursor = connection.cursor()
    try:
        cursor.execute(msg, vals)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")

def redacted_msg(msg):
    redacted_msg = msg
    for component in redacted_msg.pid:
        if component.PID_3:
            if component.PID_3.PID_3_1:
                component.PID_3.PID_3_1.value = "*****"
        
        if component.PID_5:
            component.PID_5 = "*****"
        if component.PID_7:
            component.PID_7 = "*****"
        if component.PID_9:
            component.PID_9 = "*****"
        if component.PID_12:
            component.PID_12 = "*****"
        if component.PID_18:
            component.PID_18 = "*****"
        if component.PID_19:
            component.PID_19 = "*****"
    
    for component in redacted_msg.pv1:
        if component.PV1_7:
            component.PV1_7.value = "*****"

    return redacted_msg


#MAIN: read file
redacted_file = open("messages_redacted.txt", "w")
redacted_file.truncate(0)

with open('source_hl7_messages_v2.hl7', 'r') as hl7_input:
    text = hl7_input.read()
    messages = text.split("MSH")
    
    # Read each line in the file
    for line in messages[1:5000]:
        line = "MSH" + line
        msg = parse_message(line.replace("\n", "\r"), find_groups=True, validation_level=2)
        for segment in redacted_msg(msg).children:
            redacted_file.write(segment.value + '\r')
        redacted_file.write('\n')

redacted_file.close()
            