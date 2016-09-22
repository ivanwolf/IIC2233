def mcd(m, n):  ### Algortimo de euclides para el mcd
    if m % n == 0:
        return n
    else:
        return mcd(n, m % n)


class Rational():
    def __init__(self, num, den):
        self.num = num
        self.den = den

    def __add__(self, other):
        return Rational(self.num * other.den + other.num * self.den, self.den * other.den)

    def __mul__(self, other):
        return Rational(self.num * other.num, self.den * other.den)

    def __truediv__(self, other):
        return Rational(self.num * other.den, self.den * other.num)

    def __sub__(self, other):
        return Rational(self.num * other.den - other.num * self.den, self.den * other.den)

    def __eq__(self, other):
        if self.num * other.den == other.num * self.den:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.num * other.den < other.num * self.den:
            return True
        else:
            return

    def simplificacion(self):
        m = mcd(self.num, self.den)
        return [int(self.num / m), int(self.den / m)]

    def __repr__(self):
        num = self.simplificacion()[0]
        den = self.simplificacion()[1]
        if den == 1:
            return ''.join('Rational({})'.format(str(num)))
        return ''.join('Rational({}/{})'.format(str(num), str(den)))

    def __str__(self):
        num = self.simplificacion()[0]
        den = self.simplificacion()[1]
        if den == 1:
            return ''.join('{}'.format(str(num)))

        return ''.join('{}/{}'.format(str(num), str(den)))


a = Rational(1, 3)
b = Rational(14, 3)
c = Rational(5, 1)

print(a, c, sep=', ')
print([a, c])
