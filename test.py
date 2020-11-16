#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    username ="na1212-0"
    pwd ="2525"
   # print("part_un:"+ username[2:])
    part_un =parseint( username[2:])
    pwd_reverse = reverse(pwd)
    pwd = parseint(pwd_reverse)
    lent = str(len(username)).strip()
    addend = part_un + pwd
    pwd = pwd + addend

    qr_pwd = str(pwd).strip() 
    
#    print(part_un)
 #   print(pwd)
    qr_code = lent+username+qr_pwd
    decode(qr_code)


	

	



def decode(qr_code):
  print("qr_code: "+qr_code )
   
  #qr_code ="8da1010-09652"
  x = parseint(qr_code,2)
  if x > 9:
    lent = 2
  else:
    lent = 1
  part_un = qr_code[lent+2:lent+6]
  part_pwd = qr_code[lent+x:]

  print(f"x:{x}, lent:{lent}, part_un:{part_un}, part_pwd:{part_pwd}") 
  #get pass
  save_pwd = "2525"
  pwd = parseint(reverse(save_pwd))
  
  subtrahend = parseint(part_un) + pwd
  print(f"subtrahend:{subtrahend}, pwd:{pwd}")
  pwd = parseint(part_pwd) - subtrahend
  pwd = reverse(str(pwd))
  if len(pwd) <=3:
     pwd =pwd+"0"
  print(f"pwd:: {pwd}")
  print("password:"+ pwd)
  print("username:"+qr_code[lent:x+lent])
	 
	
    
     #
def reverse(s): 
  str = "" 
  for i in s: 
    str = i + str
  return str
def parseint(string,lenght=10):

    result = '0'
    ctr = 0
    for x in string:
        if x.isdigit():
           result+=x
           ctr = ctr + 1
        else:
            return int(result)

        if ctr >= lenght:
               return int(result)
    return int(result)

if __name__ == '__main__':
    main()
