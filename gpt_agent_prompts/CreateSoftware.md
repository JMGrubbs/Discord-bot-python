Instructions:
    1. Responsed with ONLY a valid json object in the form of a string "{object}"
    2. The json object must have a key called "code" that contains the code to be inserted into the file
    3. The json object must have a key called "filename" with a value of a string of a filename
    4. The json object must have a key called "Instructions" with a value of a string of instructions for the user
    5. The python code must print "Hello world"

The JSON object can have any number of key value pairs but must include the 3 keys above. The python code can be any valid python code in the form of a string that can be parsed by json.loads(). The filename can be any valid filename in string format. The instructions can be any valid string.
Example response: "{"code": "print('Hello world')", "filename": "hello.py", "Instructions": "print hello world"}"


I want a python script that returns the current datetime in humanreadble format

I want a python script that prints all the prime numbers under 100


You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.