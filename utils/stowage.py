import numpy as np
import random


# ======================================================
# BOUNDING BOX
# ======================================================
def get_bbox(cx, cy, L, W):
    return (
        cx - L/2, cx + L/2,
        cy - W/2, cy + W/2
    )


def overlap(b1, b2):
    return not (
        b1[1] <= b2[0] or  # xmax1 <= xmin2
        b1[0] >= b2[1] or  # xmin1 >= xmax2
        b1[3] <= b2[2] or  # ymax1 <= ymin2
        b1[2] >= b2[3]     # ymin1 >= ymax2
    )


# ======================================================
# VALIDATION
# ======================================================
def valid_positions(pos, lens, wids, Ls, Ws):
    N = len(pos)
    for i in range(N):
        cx, cy = pos[i]
        L, W = lens[i], wids[i]
        b1 = get_bbox(cx, cy, L, W)

        # boundary
        if b1[0] < -Ls/2 or b1[1] > Ls/2:
            return False
        if b1[2] < -Ws/2 or b1[3] > Ws/2:
            return False

        # collision
        for j in range(i+1, N):
            cx2, cy2 = pos[j]
            b2 = get_bbox(cx2, cy2, lens[j], wids[j])
            if overlap(b1, b2):
                return False

    return True


# ======================================================
# COG
# ======================================================
def compute_cog_pos(pos, weights):
    total = np.sum(weights)
    if total == 0:
        return (0, 0)
    X = np.sum(pos[:, 0] * weights) / total
    Y = np.sum(pos[:, 1] * weights) / total
    return X, Y


# ======================================================
# FITNESS
# ======================================================
def fitness(pos, lens, wids, wgt, Ls, Ws, tx, ty):

    if not valid_positions(pos, lens, wids, Ls, Ws):
        return 1e12

    cx, cy = compute_cog_pos(pos, wgt)
    return abs(cx - tx) + abs(cy - ty)


# ======================================================
# RANDOM CHROMOSOME
# ======================================================
def random_chromosome(N, Ls, Ws):
    xs = np.random.uniform(-Ls/2, Ls/2, N)
    ys = np.random.uniform(-Ws/2, Ws/2, N)
    return np.column_stack((xs, ys))


# ======================================================
# CROSSOVER
# ======================================================
def crossover(p1, p2):
    N = len(p1)
    cut = random.randint(1, N - 1)
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
            child[i, 0] = min(max(child[i, 0], -Ls/2), Ls/2)
            child[i, 1] = min(max(child[i, 1], -Ws/2), Ws/2)
    return child


# ======================================================
# SELECTION
# ======================================================
def tournament(pop, scores):
    i, j = random.sample(range(len(pop)), 2)
    return pop[i] if scores[i] < scores[j] else pop[j]


# ======================================================
# GENETIC ALGORITHM – MAIN
# ======================================================
def GA_arrange(items, Ls, Ws, cog_x_v, cog_y_v,
               pop_size=40, generations=150):

    N = len(items)
    if N == 0:
        return []

    # extract static data
    lens = np.array([v["length"] for v in items])
    wids = np.array([v["width"] for v in items])
    wgts = np.array([v["weight"] for v in items])
    names = [v["name"] for v in items]

    target_x = cog_x_v - Ls/2
    target_y = cog_y_v - Ws/2

    # initial pop
    pop = [random_chromosome(N, Ls, Ws) for _ in range(pop_size)]

    for gen in range(generations):

        scores = [
            fitness(ch, lens, wids, wgts, Ls, Ws, target_x, target_y)
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
        fitness(ch, lens, wids, wgts, Ls, Ws, target_x, target_y)
        for ch in pop
    ]

    best_idx = int(np.argmin(scores))
    best_pos = pop[best_idx]

    # build final structured items
    arranged = []
    for i in range(N):
        arranged.append({
            "name": names[i],
            "length": float(lens[i]),
            "width":  float(wids[i]),
            "weight": float(wgts[i]),
            "pos":    (float(best_pos[i,0]), float(best_pos[i,1]))
        })

    return arranged
