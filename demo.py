from subjectivity import Subjective

@Subjective
class Cat:
    pass

@Subjective
class Dog:
    pass

@Subjective
class Apple:
    pass

@Subjective
class Orange:
    pass

cat = Cat()
dog = Dog()

apple = Apple()
orange = Orange()

print('Comparing cats and dogs')
print('cat > dog : %s' % (cat > dog))

print('Comparing apples and oranges')
print('apple > orange : %s' % (apple > orange))

