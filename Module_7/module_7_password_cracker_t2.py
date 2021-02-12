import os 
import os.path
import sys
import string

alphabet = list(string.ascii_lowercase)

def main():

  max_length = 31
  guess = "" 
  prefix = guess 
  password_size_reached = False
  guess = "a" * max_length 

  path = "/home/sgx/pin-2.14-71313-gcc.4.4.7-linux/source/tools/SGXTrace"
  #trace_program = "../../../pin.sh -t ./obj-intel64/SGXTrace.so -o ~/isl/guess.txt -trace 1 -- /home/sgx/isl/t2/password_checker_2 " + guess + " > /dev/null 2>&1"
  delete_program = "rm ~/isl/guess.txt"
  trace = "/home/sgx/isl/guess.txt"

  k_increment_addr = "0x4011b6"
  equal_size_all_correct_addr = "0x4011dc"
  j_increment_addr = "0x4011bc"

  working_dir = os.getcwd()
  #print("Current working directory: {0}".format(os.getcwd()))
  os.chdir(path)


  #calculate password length
  if os.path.isfile(trace):
    os.system(delete_program) #delete previous version of the trace  
  trace_program = "../../../pin.sh -t ./obj-intel64/SGXTrace.so -o ~/isl/guess.txt -trace 1 -- /home/sgx/isl/t2/password_checker_2 " + guess + " > /dev/null 2>&1"
  os.system(trace_program)
  
  #count k and j increments
  with open(trace, 'r') as f:
    count = 0
    line = f.readline()
    while line:
      line = line.split(":")
      if line[0] == "E" and (line[1] == k_increment_addr or line[1] == j_increment_addr):
        count += 1
      line = f.readline()
  
  #max is not the actual length of the password we want to find
  max_length = count
  password = ["a"] * max_length

  #compute password
  for letter in alphabet:
    char_pointer = 0
    guess = letter * max_length
    if os.path.isfile(trace):
      os.system(delete_program) #delete previous version of the trace  
    trace_program = "../../../pin.sh -t ./obj-intel64/SGXTrace.so -o ~/isl/guess.txt -trace 1 -- /home/sgx/isl/t2/password_checker_2 " + guess + " > /dev/null 2>&1"
    os.system(trace_program)

    with open(trace, 'r') as f:
      line = f.readline()
      while line:
        line = line.split(":")
        #if we increment k we have the correct char at this char_pointer write into password
        if line[0] == "E" and line[1] == k_increment_addr:
          password[char_pointer] = letter
          char_pointer += 1
        if line[0] == "E" and line[1] == j_increment_addr:
          char_pointer += 1
        line = f.readline()

  password_string = ""
  for letter in password:
    password_string += letter
  
  #print(len(password_string))
  return password_string , "complete"

if __name__ == "__main__":
    password, completeness = main()
    print("{0} {1}".format(password, completeness))




