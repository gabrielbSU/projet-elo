import math

class SystemeElo:
    def __init__(self, rating_init=1500, k=32):
        self.historique = [rating_init]
        self.K = k

    @property
    def rating(self):
        return self.historique[-1]

    def update(self, opponent_rating, score):
        expected = 1 / (1 + 10 ** ((opponent_rating - self.rating) / 400))
        new_rating = self.rating + self.K * (score - expected)
        self.historique.append(new_rating)


class SystemeGlicko:
    def __init__(self, rating_init=1500, rd_init=350):
        self.Q = math.log(10) / 400
        self.historique = [(rating_init, rd_init)]

    def get_rating(self):
        return self.historique[-1]

    def update(self, adversaires, scores):
        r, rd = self.get_rating()
        d2_inv = 0
        delta_sum = 0

        for (ri, rdi), score in zip(adversaires, scores):
            g = 1 / math.sqrt(1 + 3 * self.Q ** 2 * rdi ** 2 / math.pi ** 2)
            E = 1 / (1 + 10 ** (g * (ri - r) / 400))
            d2_inv += (self.Q ** 2) * g ** 2 * E * (1 - E)
            delta_sum += self.Q * g * (score - E)

        if d2_inv == 0:
            new_rd = min(math.sqrt(rd ** 2 + 50 ** 2), 350)
            self.historique.append((r, new_rd))
            return

        d2 = 1 / d2_inv
        new_rd = 1 / math.sqrt(1 / rd ** 2 + 1 / d2)
        new_rating = r + self.Q / (1 / rd ** 2 + 1 / d2) * delta_sum
        self.historique.append((new_rating, new_rd))


class SystemeGlicko2:
    def __init__(self, rating=1500, rd=350, vol=0.06):
        self.mu = (rating - 1500) / 173.7178
        self.phi = rd / 173.7178
        self.sigma = vol
        self.tau = 0.5
        self.historique = [(rating, rd, vol)]

    def get_rating(self):
        r = 173.7178 * self.mu + 1500
        rd = 173.7178 * self.phi
        return (r, rd, self.sigma)

    def _g(self, phi):
        return 1 / math.sqrt(1 + 3 * phi**2 / math.pi**2)

    def _E(self, mu, muj, phij):
        return 1 / (1 + math.exp(-self._g(phij) * (mu - muj)))

    def _f(self, x, delta, phi, v):
        a = math.log(self.sigma**2)
        ex = math.exp(x)
        num = ex * (delta**2 - phi**2 - v - ex)
        denom = 2 * (phi**2 + v + ex)**2
        return (num / denom) - ((x - a) / self.tau**2)

    def update(self, adversaires, scores):
        if not adversaires:
            self.phi = math.sqrt(self.phi**2 + self.sigma**2)
            self.historique.append(self.get_rating())
            return

        mu = self.mu
        phi = self.phi
        sigma = self.sigma

        v_inv = 0
        delta_num = 0
        for (rj, rdj, _), score in zip(adversaires, scores):
            muj = (rj - 1500) / 173.7178
            phij = rdj / 173.7178
            g = self._g(phij)
            E = self._E(mu, muj, phij)
            v_inv += (g**2) * E * (1 - E)
            delta_num += g * (score - E)

        v = 1 / v_inv
        delta = v * delta_num

        a = math.log(sigma**2)
        A = a
        eps = 1e-6
        B = math.log(sigma**2 + 1)

        fA = self._f(A, delta, phi, v)
        fB = self._f(B, delta, phi, v)

        while abs(B - A) > eps:
            C = A + (A - B) * fA / (fB - fA)
            fC = self._f(C, delta, phi, v)
            if fC * fB < 0:
                A, fA = B, fB
            else:
                fA = fA / 2
            B, fB = C, fC

        new_sigma = math.exp(A / 2)
        sigma_prime = new_sigma

        phi_star = math.sqrt(phi**2 + sigma_prime**2)
        phi_prime = 1 / math.sqrt(1 / phi_star**2 + 1 / v)
        mu_prime = mu + phi_prime**2 * delta_num

        self.mu = mu_prime
        self.phi = phi_prime
        self.sigma = sigma_prime

        self.historique.append(self.get_rating())