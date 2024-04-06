# Write code below 💖
#Loop condition
correctAns=False

#Houses
gryff="Gryffindor"
raven="Ravenclaw"
huffle="Hufflepuff"
slyth="Slytherin"

#Points
gryffPoints=0
ravenPoints=0
hufflePoints=0
slythPoints=0

while not correctAns:
  q1Answer=int(input('''Q1/) Do you like Dawn or Dusk?
      1) Dawn
      2) Dusk
      '''))

  if q1Answer == 1:
    gryffPoints+=1
    ravenPoints+=1
    correctAns=True
  elif q1Answer == 2:
    hufflePoints+=1
    slythPoints+=1
    correctAns=True
  else:
    print("Wrong input.")
#end while

correctAns=False

while not correctAns:
  q2Answer=int(input('''Q2/) When Im dead, I want people to remember me as:
      1) The Good
      2) The Great
      3) The Wise
      4) The Bold
      '''))

  if q1Answer == 1:
    hufflePoints+=2
    correctAns=True
  elif q1Answer == 2:
    slythPoints+=2
    correctAns=True
  elif q1Answer == 3:
    ravenPoints+=2
    correctAns=True
  elif q1Answer == 4:
    gryffPoints+=2
    correctAns=True
  else:
    print("Wrong input.")
#end while

correctAns=False

while not correctAns:
  q3Answer=int(input('''Q3/) Which kind of instrument most pleases your ear?
      1) The violin
      2) The trumpet
      3) The piano
      4) The drum
      '''))

  if q1Answer == 1:
    slythPoints+=4
    correctAns=True
  elif q1Answer == 2:
    hufflePoints+=4
    correctAns=True
  elif q1Answer == 3:
    ravenPoints+=4
    correctAns=True
  elif q1Answer == 4:
    gryffPoints+=4
    correctAns=True
  else:
    print("Wrong input.")
#end while

if gryffPoints>slythPoints and gryffPoints>hufflePoints and gryffPoints>ravenPoints:
  print(gryff)
elif ravenPoints>gryffPoints and ravenPoints>slythPoints and ravenPoints>hufflePoints:
  print(raven)
elif hufflePoints>gryffPoints and hufflePoints>slythPoints and hufflePoints>ravenPoints:
  print(huffle)
elif slythPoints>gryffPoints and slythPoints>hufflePoints and slythPoints>ravenPoints:
  print(slyth)
else:
  print("There are not correct answers.")