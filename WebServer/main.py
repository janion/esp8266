import machine
import socket
import re as ure

pins = [machine.Pin(i, machine.Pin.OUT) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

def setPin(pin, value):
  pinObj = getPin(pin)
  if pinObj != None:
    pinObj.value(float(value))
    return "PIN %s set to %s" % (pin, value)
  else:
    return "No pin numbered %s" % pin

def getPin(pinNumber):
  for pin in pins:
    if str(pin.get_id()) == str(pinNumber):
      return pin
  
def parseURL(url):
  #PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
  parameters = {}
  
  path = ure.search("(.*?)(\?|$)", url) 
  
  while True:
    vars = ure.search("(([a-z0-9]+)=([a-z0-8.]*))&?", url)
    if vars:
      parameters[vars.group(2)] = vars.group(3)
      url = url.replace(vars.group(0), '')
    else:
      break

  return path.group(1), parameters

def buildResponse(response):
  # BUILD DE HTTP RESPONSE HEADERS
  return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (len(response), response)
    
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = str(cl.recv(1024))
    #print("REQUEST: ", request)

    obj = ure.search("GET (.*?) HTTP\/1\.1", request)
    #print(obj.group(1))
    
    if not obj:
      cl.send(buildResponse("INVALID REQUEST"))
    else:
      path, parameters = parseURL(obj.group(1))
      if path.startswith("/setPin"):
         pin = parameters.get("pin", None)
         value = parameters.get("value", None)
         print(setPin(pin, value))

      rows = ['<tr><td><a href="/setPin/pin=%d,value=%d">%d</a></td><td>%d</td></tr>' % (p.get_id(), not p.value(), p.get_id(), p.value()) for p in pins]
      response = html % '\n'.join(rows)
      cl.send(response)
    cl.close()
