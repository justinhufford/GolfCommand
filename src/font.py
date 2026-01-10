# Font design inspired by Tmplr

A="""
┎┒
┠┨
┸┖
  
"""
B="""
┰┒
┠┨
┸┚
  
"""
C="""
┎┒
┃ 
┖┚
  
"""
D="""
┰┒
┃┃
┸┚
  
"""
E="""
┰┒
┠╴
┸┚
  
"""
F="""
┰┒
┠╴
┸ 
  
"""
G="""
┎┒
┃┰
┖┨
┖┚
"""
H="""
┰┎
┠┨
┚┸
  
"""
I="""
┰
┃
┸
 
"""
J="""
┎┰
 ┃
╻┃
┖┚
"""
K="""
┰ 
┠╱
┸┖
  
"""
L="""
┰ 
┃ 
┸┚
  
"""
M="""
┰┰┰
┃┃┃
┸ ┸
   
"""
N="""
┰┒
┃┃
┸┖
  
"""
O="""
┎┒
┃┃
┖┚
  
"""
P="""
┰┒
┠┚
┸ 
  
"""
Q="""
┎┒
┃┃
┖┸
  
"""
R="""
┰┒
┠┒
┸┖
  
"""
S="""
┎┒
┖┒
┖┚
  
"""
T="""
┎┰┒
 ┃ 
 ┸ 
   
"""
U="""
┒┰
┃┃
┖┸
   
"""
V="""
┒┎
┃┃
┖┚
  
"""
W="""
┒┒┰
┃┃┃
┖┸┚
   
"""
X="""
┒ ┎
 ╳ 
┚ ┖
   
"""
Y="""
┒┒
┃┃
┖┨
┖┚
"""
Z="""
┎─┒
 ╱ 
┖─┚
   
"""
a="""
  
┎┒
┖┸
  
"""
b="""
┒ 
┠┒
┸┚
  
"""
c="""
  
┎╴
┖┚
  
"""
d="""
 ┒
┎┨
┖┸
  
"""
e="""
  
┎┒
┖╴
  
"""
f="""
┎
╂
┃
┚
"""
g="""
  
┎┰
┖┨
┖┚
"""
h="""
┒ 
┠┒
┸┖
  
"""
i="""
▪
╻
┖
 
"""
j="""
▪
┒
┃
┚
"""
k="""
┒ 
┠╱
┚┖
  
"""
l="""
┒
┃
┖
 
"""
m="""
   
┰┰┒
┖┖┖
   
"""
n="""
  
┰┒
┖┖
  
"""
o="""
  
┎┒
┖┚
  
"""
p="""
  
┰┒
┠┚
┚ 
"""
q="""
  
┎┰
┖┨
 ┖
"""
r="""
  
┰┒
╹ 
  
"""
s="""
  
┎╴
╶┚
  
"""
t="""
┒
╂
┖
 
"""
u="""
  
┒┒
┖┸
  
"""
v="""
  
┒┎
┖┚
  
"""
w="""
   
┒┒┰
┖┸┸
   
"""
x="""
  
┒┎
┚┖
  
"""
y="""
  
┒┒
┖┨
┖┚
"""
z="""
  
╶┒
┖╴
  
"""
space="""
  
  
  
  
"""
no1="""
┒
┃
┸
 
"""
no2="""
┎┒
┎┚
┖╴
  
"""
no3="""
┎┒
╶┨
┖┚
  
"""
no4="""
┒ 
┖╂
 ┸
  
"""
no5="""
┎╴
┖┒
┖┚
  
"""
no6="""
┎┒
┠┒
┖┚
  
"""
no7="""
─┒
 ┃
 ┸
  
"""
no8="""
┎┒
┠┨
┖┚
  
"""
no9="""
┎┒
┖┨
┖┚
  
"""
no0="""
┎┒
┃┃
┖┚
  
"""



ampersand="""
 ┎╴
┎┸╂
┖─┸
   
"""
period="""
 
 
▪
 
"""
comma="""
 
 
╻
 
"""

exclamation="""
╻
╹
╹
 
"""
question="""
┎┒
╶┚
╹ 
  
"""
dash="""
  
──
  
  
"""
dollar="""
┎╨┒
┖─┒
┖╥┚
  
"""


ASCII_CATEGORIES = {
    "uppercase": {
        "A": A, "B": B, "C": C, "D": D, "E": E, "F": F, "G": G, "H": H, "I": I,
        "J": J, "K": K, "L": L, "M": M, "N": N, "O": O, "P": P, "Q": Q, "R": R,
        "S": S, "T": T, "U": U, "V": V, "W": W, "X": X, "Y": Y, "Z": Z,
    },
    "lowercase": {
        "a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i,
        "j": j, "k": k, "l": l, "m": m, "n": n, "o": o, "p": p, "q": q, "r": r,
        "s": s, "t": t, "u": u, "v": v, "w": w, "x": x, "y": y, "z": z,
    },
    "numbers": {
        "0": no0, "1": no1, "2": no2, "3": no3, "4": no4,
        "5": no5, "6": no6, "7": no7, "8": no8, "9": no9,
    },
    "symbols": {
        " ": space,
        ".": period, "!": exclamation, "?": question, ",": comma,
        "&": ampersand, "-": dash, "$": dollar
    },
}

ascii_dict = {
    character: glyph
    for group in ASCII_CATEGORIES.values()
    for character, glyph in group.items()
}

UPPERCASE_CHARS = set(ASCII_CATEGORIES["uppercase"].keys())

def space_out_caps_words(title: str) -> str:
    words = title.split()  # simple: collapses extra spaces
    n = len(words)
    out = []

    for i, word in enumerate(words):
        has_lowercase = any(ch.islower() for ch in word)
        has_uppercase_from_category = any(ch in UPPERCASE_CHARS for ch in word)

        # expand only if:
        # - no lowercase letters
        # - AND it includes at least one uppercase letter from your uppercase category
        if word and (not has_lowercase) and has_uppercase_from_category:
            spaced = " ".join(word)

            if n == 1:
                out.append(spaced)
            elif i == 0:
                out.append(spaced + "  ")
            else:
                out.append("  " + spaced + "  ")
        else:
            out.append(word)

    return " ".join(out)





def draw(title):
    title = space_out_caps_words(title)
    title_letters = [char for char in title if char in ascii_dict]
    ascii_letters = [ascii_dict[char] for char in title_letters]
    split_letters = [letter.splitlines() for letter in ascii_letters]
    lines = [''.join(line_parts) for line_parts in zip(*split_letters)]
    return '\n'.join(lines)



if __name__ == "__main__":
    while True:
        title = input("> ")
        art = draw(title)
        print(art)
