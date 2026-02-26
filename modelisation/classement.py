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
    def __init__(self, rating=1500, rd=350, sigma=0.06):
        self.r = (rating - 1500) / 173.7178  # Échelle Glicko-2
        self.rd = rd / 173.7178
        self.sigma = sigma
        self.historique = [(self.get_rating()[0], self.get_rating()[1])]

    def get_rating(self):
        # Conversion en échelle Glicko classique
        return 173.7178 * self.r + 1500, self.rd * 173.7178

    def g(self, phi):
        return 1 / math.sqrt(1 + 3 * phi**2 / math.pi**2)

    def E(self, mu, mu_j, phi_j):
        return 1 / (1 + math.exp(-self.g(phi_j) * (mu - mu_j)))

    def update(self, adversaires, scores):
        mu, phi, sigma = self.r, self.rd, self.sigma
        v_inv = 0
        delta_num = 0

        for (rj, rdj), score in zip(adversaires, scores):
            mu_j = (rj - 1500) / 173.7178
            phi_j = rdj / 173.7178
            E_ = self.E(mu, mu_j, phi_j)
            g_ = self.g(phi_j)
            v_inv += (g_**2) * E_ * (1 - E_)
            delta_num += g_ * (score - E_)

        if v_inv == 0:
            self.historique.append(self.get_rating())
            return

        v = 1 / v_inv
        delta = v * delta_num

        phi_star = math.sqrt(phi**2 + sigma**2)
        phi_new = 1 / math.sqrt(1 / phi_star**2 + 1 / v)
        mu_new = mu + phi_new**2 * delta_num

        self.r = mu_new
        self.rd = phi_new
        self.historique.append(self.get_rating())
