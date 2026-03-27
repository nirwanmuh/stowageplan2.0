import numpy as np
import random


# ======================================================
# VEHICLE BOX (AABB)
# ======================================================
def bbox(cx, cy, L, W):
    return (
        cx - L/2, cx + L/2,
        cy - W/2, cy + W/2
    )


def overlap(b1, b2):
    return not (
        b1[1] <= b2[0] or   # xmax1 <= xmin2
        b1[0] >= b2[1] or   # xmin1 >= xmax2
        b1[3] <= b2[2] or   # ymax1 <= ymin2
        b1[2] >= b2[3]      # ymin1 >= ymax2
    )


# ======================================================
# VALIDATION FOR ENTIRE CHROMOSOME
# ======================================================
def valid_positions(pos, lengths, widths, Ls, Ws):
    N = len(pos)
    for i in range(N):
        x, y = pos[i]
        L, W = lengths[i], widths[i]
        b1 = bbox(x, y, L, W)

        # boundary
        if b1[0] < -Ls/2 or b1[1] > Ls/2:
            return False
        if b1[2] < -Ws/2 or b1[3] > Ws/2:
            return False

        # collision
        for j in range(i + 1, N):
            x2, y2 = pos[j]
            b2 = bbox(x2, y2, lengths[j], widths[j])
            if overlap(b1, b2):
                return False
    return True


# ======================================================
# COMPUTE COG
# ======================================================
def compute_cog_pos(pos, weights):
    total = np.sum(weights)
    if total == 0:
        return (0, 0)
    X = np.sum(pos[:, 0] * weights) / total
    Y = np.sum(pos[:, 1] * weights) / total
    return X, Y


# ======================================================
# FITNESS FUNCTION (minimize CoG error)
# ======================================================
def fitness(pos, lengths, widths, weights, Ls, Ws, tx, ty):
    if not valid_positions(pos, lengths, widths, Ls, Ws):
        return 1e12  # heavy penalty

    cx, cy = compute_cog_pos(pos, weights)
    return abs(cx - tx) + abs(cy - ty)


# ======================================================
# INIT RANDOM CHROMOSOME
# ======================================================
def random_chromosome(N, Ls, Ws):
    x = np.random.uniform(-Ls/2, Ls/2, N)
    y = np.random.uniform(-Ws/2, Ws/2, N)
    return np.vstack([x, y]).T  # shape (N, 2)


# ======================================================
# CROSSOVER
# ======================================================
def crossover(p1, p2):
    N = len(p1)
    cut = random.randint(1, N - 1)  # always valid because N>=2
    child = np.zeros_like(p1)
    child[:cut] = p1[:cut]
    child[cut:] = p2[cut:]
    return child


# ======================================================
# MUTATION
# ======================================================
def mutate(child, Ls, Ws, rate=0.2):
    N = len(child)
    for i in range(N):
        if random.random() < rate:
            child[i, 0] += random.uniform(-0.5, 0.5)
            child[i, 1] += random.uniform(-0.5, 0.5)

            # clamp
            child[i, 0] = max(-Ls/2, min(Ls/2, child[i, 0]))
            child[i, 1] = max(-Ws/2, min(Ws/2, child[i, 1]))

    return child


# ======================================================
# SELECTION
# ======================================================
def tournament(pop, scores):
    a, b = random.sample(range(len(pop)), 2)
    return pop[a] if scores[a] < scores[b] else pop[b]


# ======================================================
# GENETIC ALGORITHM MAIN FUNCTION
# ======================================================
def GA_arrange(items, Ls, Ws, cog_x_visual, cog_y_visual,
               pop_size=40, generations=150):

    N = len(items)
    if N == 0:
        return []

    # extract vehicle attributes
    lengths = np.array([v["length"] for v in items])
    widths = np.array([v["width"] for v in items])
    weights = np.array([v["weight"] for v in items])

    tx = cog_x_visual - Ls/2
    ty = cog_y_visual - Ws/2

    # init population
    pop = [random_chromosome(N, Ls, Ws) for _ in range(pop_size)]

    for gen in range(generations):

        scores = [
            fitness(ch, lengths, widths, weights, Ls, Ws, tx, ty)
            for ch in pop
        ]

        new_pop = []

        for _ in range(pop_size):
            p1 = tournament(pop, scores)
            p2 = tournament(pop, scores)

            child = crossover(p1, p2)
            child = mutate(child, Ls, Ws)

            new_pop.append(child)

        pop = new_pop

    # final best
    scores = [
        fitness(ch, lengths, widths, weights, Ls, Ws, tx, ty)
        for ch in pop
    ]

    best_idx = int(np.argmin(scores))
    best_pos = pop[best_idx]

    # reassign to items
    arranged = []
    for i, v in enumerate(items):
        vc = v.copy()
        vc["pos"] = (best_pos[i, 0], best_pos[i, 1])
        arranged.append(vc)

    return arranged
