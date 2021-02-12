import os 
import sys
import string

#create bijection
numb_to_alphabet = list(string.ascii_lowercase)
alphabet_to_numb =  dict(zip(string.ascii_lowercase, range(0,26)))

def main():

  folder_string = sys.argv[1]
  os.chdir(folder_string)
  longest_password_prefix = ''
  traces = os.listdir(os.getcwd())

  for trace in traces:

    password, completeness = get_password(trace)
    if longest_password_prefix in password:
      longest_password_prefix = password
    if completeness == 'complete':
      return password, completeness
  
  password = longest_password_prefix
  return password, completeness

    
def get_password(trace):
  
  guess = trace.split(".txt")[0]
  char_pointer = 0 
  diff_char_size = 0 
  password = ""
  completeness = "partial"
  
  reached_size_check = False
  smaller_or_equal = False
  equal = False
  
  cond_mov_addr = '0x4011d0'
  correct_char_addr = '0x401211' 			#addr necessary to be visited for k++ to happen
  POW_func_addr = '0x401217'     			#addr necessary to be visited for wrong char
  diff_char_for_counter = '0x40127e'  #addr that is visited each time the for loop counting the difference between the chars is used
  end_for_loop_addr = '0x401288'
  equal_size_addr = '0x4012a0'
  
  #format of the lines we look at here: E/R/W:addr:C/D[:opcode:disassembly] 
  with open(trace, 'r') as f:
    line = f.readline()
    while line:
      line = line.split(":")
      if line[1] == cond_mov_addr and line[0]=='E':
        line = f.readline()
        if line:
          line = line.split(":")
          if line[0] == 'R': #its a read hence the eax is rewritten by the input size hence the input size is smaller or equal to password size
            smaller_or_equal = True
      
      #if we guessed the correct character then address is present 
      if line[1] == correct_char_addr and line[0] == 'E':
        #password[char_pointer] = guess[char_pointer]
        password += guess[char_pointer]
        char_pointer += 1

      #if the character we guessed is wrong we go here to extract that char 
      if line[1] == POW_func_addr and line[0] == 'E':
        diff_char_size = 0

        #while we haven't reached the end_for_loop instruction keep parsing
        while line[1] != end_for_loop_addr:
          if line[1] == diff_char_for_counter and line[0] == 'E':
            diff_char_size += 1
          line = f.readline()
          line = line.split(":")
        #here we want to calculate the actual character        
        number = (alphabet_to_numb[guess[char_pointer]] + diff_char_size) % 26
        password += numb_to_alphabet[number]

        #print("{0}. password char numb {1} is char: {2} ------ guess char numb {3} is char: {4} ------ the difference is: {5}".format(char_pointer, number, numb_to_alphabet[number], alphabet_to_numb[guess[char_pointer]], guess[char_pointer], diff_char_size))
        char_pointer += 1
      
      #this is only done if password and guess are of equal size
      if line[1] == equal_size_addr:
        equal = True 

      line = f.readline()
  
  #if the guess is the same length or more the password we gots it
  if (smaller_or_equal and equal) or not smaller_or_equal:
    completeness = 'complete'
  return password, completeness
  

if __name__ == "__main__":
    password, completeness = main()
    print("{0} {1}".format(password, completeness))
