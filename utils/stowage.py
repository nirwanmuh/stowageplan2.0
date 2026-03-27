import numpy as np
import random

# ======================================================
# AABB Bounding Box
# ======================================================
def get_bbox(cx, cy, L, W):
    xmin = cx - L/2
    xmax = cx + L/2
    ymin = cy - W/2
    ymax = cy + W/2
    return (xmin, xmax, ymin, ymax)

def bbox_overlap(b1, b2):
    x1min, x1max, y1min, y1max = b1
    x2min, x2max, y2min, y2max = b2

    return not (
        x1max <= x2min or
        x1min >= x2max or
        y1max <= y2min or
        y1min >= y2max
    )

# ======================================================
# VALIDATION
# ======================================================
def valid_positions(pos, lengths, widths, ship_L, ship_W):
    N = len(pos)
    for i in range(N):
        xi, yi = pos[i]
        Li, Wi = lengths[i], widths[i]
        b1 = get_bbox(xi, yi, Li, Wi)

        # boundary check
        if b1[0] < -ship_L/2 or b1[1] > ship_L/2: return False
        if b1[2] < -ship_W/2 or b1[3] > ship_W/2: return False

        # collision check
        for j in range(i+1, N):
            xj, yj = pos[j]
            Lj, Wj = lengths[j], widths[j]
            b2 = get_bbox(xj, yj, Lj, Wj)
            if bbox_overlap(b1, b2):
                return False
    return True

# ======================================================
# CoG (pos array)
# ======================================================
def compute_cog_pos(pos, weights):
    total = np.sum(weights)
    if total == 0:
        return (0,0)
    cx = np.sum(pos[:,0] * weights) / total
    cy = np.sum(pos[:,1] * weights) / total
    return cx, cy

# ======================================================
# FITNESS FUNCTION
# ======================================================
def fitness(pos, lengths, widths, weights, ship_L, ship_W, target_x, target_y):

    if not valid_positions(pos, lengths, widths, ship_L, ship_W):
        return 1e12

    cx, cy = compute_cog_pos(pos, weights)
    return abs(cx - target_x) + abs(cy - target_y)

# ======================================================
# RANDOM CHROMOSOME
# ======================================================
def random_chromosome(N, ship_L, ship_W):
    x = np.random.uniform(-ship_L/2, ship_L/2, N)
    y = np.random.uniform(-ship_W/2, ship_W/2, N)
    return np.column_stack((x,y))

# ======================================================
# CROSSOVER
# ======================================================
def crossover(p1, p2):
    N = len(p1)
    cut = random.randint(1, N-1)
    child = np.zeros_like(p1)
    child[:cut] = p1[:cut]
    child[cut:] = p2[cut:]
    return child

# ======================================================
# MUTATION
# ======================================================
def mutate(child, ship_L, ship_W, rate=0.2):
    N = len(child)
    for i in range(N):
        if random.random() < rate:
            child[i,0] += random.uniform(-0.5, 0.5)
            child[i,1] += random.uniform(-0.5, 0.5)

            child[i,0] = min(max(child[i,0], -ship_L/2), ship_L/2)
            child[i,1] = min(max(child[i,1], -ship_W/2), ship_W/2)

    return child

# ======================================================
# SELECTION
# ======================================================
def tournament(pop, scores):
    a, b = random.sample(range(len(pop)), 2)
    return pop[a] if scores[a] < scores[b] else pop[b]

# ======================================================
# GA ENGINE
# ======================================================
def GA_arrange(items, ship_L, ship_W, cog_x_visual, cog_y_visual,
               pop_size=40, generations=150):

    N = len(items)
    if N == 0:
        return []

    lengths = np.array([v["length"] for v in items])
    widths  = np.array([v["width"] for v in items])
    weights = np.array([v["weight"] for v in items])

    target_x = cog_x_visual - ship_L/2
    target_y = cog_y_visual - ship_W/2

    pop = [random_chromosome(N, ship_L, ship_W) for _ in range(pop_size)]

    for gen in range(generations):

        scores = [
            fitness(ch, lengths, widths, weights, ship_L, ship_W, target_x, target_y)
            for ch in pop
        ]

        new_pop = []
        for _ in range(pop_size):
            p1 = tournament(pop, scores)
            p2 = tournament(pop, scores)
            child = crossover(p1, p2)
            child = mutate(child, ship_L, ship_W)
            new_pop.append(child)

        pop = new_pop

    # return best
    scores = [
        fitness(ch, lengths, widths, weights, ship_L, ship_W, target_x, target_y)
        for ch in pop
    ]

    best_idx = int(np.argmin(scores))
    best_pos = pop[best_idx]

    arranged = []
    for i, v in enumerate(items):
        vc = v.copy()
        vc["pos"] = (float(best_pos[i,0]), float(best_pos[i,1]))
        arranged.append(vc)

    return arranged
