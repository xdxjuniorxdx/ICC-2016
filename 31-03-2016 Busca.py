def binario():
  b = 0
  c = n
  d = (b+c)/2

  while c - b >= 1:
    if a[d] == x:
      return d
    else:
      if a[d] < x:
        b = d
      else:
        c = d
      d = (b+c)/2

  return -1

def linear():
  i = 0
  while i < n:
    if a[i] == x:
      return i

    i += 1
    
  return -1

def linearSeq():
  i = 0
  while i < n:
    if a[i] == x:
      return i
    else:
      if a[i] > x:
        return -1
      else:
        i += 1
  
  return -1
