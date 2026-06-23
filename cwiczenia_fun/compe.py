

letters = 'Python'

alphabets = []

for letter in letters:
    alphabets.append(letter)
    
print(alphabets)

alphabet = [letters for letters in letters]

print(alphabet)


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even = [number for number in numbers if number % 2 == 0]
print(even)
