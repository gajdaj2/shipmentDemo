


def diff21(n):
    return abs(n-21) if n<=21 else abs(21-n)




#print(diff21(19))  # Output: 2
#print(diff21(10))  # Output: 11
#print(diff21(21))  # Output: 0


def sleep_in(weekday: bool, vacation):
    return not weekday or vacation


def missing(str,n):
    return str[:n]+str[n+1:]

#print(missing("kitten", 1))  # Output: "ktten"


def monk(a_smile,b_smile):
    return True if (a_smile and b_smile)  == True or (a_smile or b_smile) == False else False


def p_ask(talking, hour):
    if (hour <= 20 or hour > 6) and talking:
        return True
    return False



def um_d(a,b):
    if a != b:
        return a + b
    return 2*(a+b)

def front_back(str):
  if len(str)>1:
    return str[len(str)-1]+str[1:len(str)-1]+str[0]
  else: 
      return str


def generate_hashtag(s):
    s = s.strip().lstrip("#")
    words = s.split()
    if not words:
        return False
    if len("#" + "".join(w.capitalize() for w in words)) > 140:
        return False 
    else:
        return "#" + "".join(w.capitalize() for w in words)

#print(generate_hashtag("hello"))
#print(generate_hashtag("'#      Codewars'"))# Output: "#helloH"
#print(generate_hashtag("#Codewarsisnice"))  # Output: False

def sum_strings(x, y):
    return str((int(x)+int(y)))

#print(sum_strings("1", "2"))  # Output: "579"



def pig_it(text):
    words = text.split()
    print(words)
    new_words = ""
    for i in words:
        if i[0].isalpha():
            new_words += i[1:len(i)]+i[0]+'ay '
        else:
            new_words += i + ' '
    return new_words.strip().rstrip()
    
print(pig_it('Pig latin is cool')) # igPay atinlay siay oolcay
pig_it(('Hello world !'))     # elloHay orldway !