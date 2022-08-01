from numpy import uint8
from Camera import camera
from Chess import chess

import matplotlib.pyplot as plt

import glob

if __name__ == "__main__":
    ch = chess()
    ch.ser.write_timeout = 0

    a = b'a' 
    move = (48).to_bytes(1,"big")
    solenoid = (0).to_bytes(1,"big")

    print("solenoid is: {}".format(solenoid))

    messages = [a, solenoid, move]

    print(messages) 

    print(ch.ser.is_open)

    for i in range(10):

        ch.ser.close()
        ch.ser.open()

        ch.ser.reset_input_buffer()
    
    for message in messages:
        print(message)
        temp = (message)
        print(temp)
        ch.ser.write(temp)

        feedback = ch.ser.read()
        print("Feedback: {}".format(int.from_bytes(feedback, "big")))
        # if (message == 97):
        #     feedback = ch.ser.read()
        #     print("Feedback: {}".format(int.from_bytes(feedback, "big")))
       

    ch.ser.close()
     
    

