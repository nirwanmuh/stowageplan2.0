import numpy as np
import random

# ======================================================
# AABB Bounding Box (4 titik kendaraan)
# ======================================================
def get_bbox(cx, cy, L, W):
    return (
        cx - L/2, cx + L/2,   # xmin, xmax
        cy - W/2, cy + W/2    # ymin, ymax
    )

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
# No overlap & inside ship
# ======================================================
def valid_chromosome(vehicles, ship_L, ship_W):
    n = len(vehicles)
    for i in range(n):
        xi, yi = vehicles[i]["pos"]
        bi = get_bbox(xi, yi, vehicles[i]["length"], vehicles[i]["width"])

        # boundary check
        if bi[0] < -ship_L/2 or bi[1] > ship_L/2:
            return False
        if bi[2] < -ship_W/2 or bi[3] > ship_W/2:
            return False

        # collision check
        for j in range(i+1, n):
            xj, yj = vehicles[j]["pos"]
            bj = get_bbox(xj, yj, vehicles[j]["length"], vehicles[j]["width"])
            if bbox_overlap(bi, bj):
                return False

    return True

# ======================================================
# Compute CoG
# ======================================================
def compute_cog(vehicles):
    total = sum(v["weight"] for v in vehicles)
    if total == 0:
        return (0,0)
    X = sum(v["pos"][0] * v["weight"] for v in vehicles) / total
    Y = sum(v["pos"][1] * v["weight"] for v in vehicles) / total
    return (X,Y)

# ======================================================
# FITNESS — minimize CoG error + collision penalty
# ======================================================
def fitness(chrom, ship_L, ship_W, target_x, target_y):
    # penalty if overlap
    if not valid_chromosome(chrom, ship_L, ship_W):
        return 10**9

    cx, cy = compute_cog(chrom)
    return abs(cx - target_x) + abs(cy - target_y)

# ======================================================
# RANDOM CHROMOSOME GENERATOR
# ======================================================
def random_chromosome(items, ship_L, ship_W):
    chrom = []
    for v in items:
        x = random.uniform(-ship_L/2, ship_L/2)
        y = random.uniform(-ship_W/2, ship_W/2)
        vcopy = v.copy()
        vcopy["pos"] = (x,y)
        chrom.append(vcopy)
    return chrom

# ======================================================
# CROSSOVER
# ======================================================
def crossover(c1, c2):
    cut = random.randint(1, len(c1)-1)
    child = []
    for i in range(len(c1)):
        if i < cut:
            child.append(c1[i].copy())
        else:
            child.append(c2[i].copy())
    return child

# ======================================================
# MUTATION
# ======================================================
def mutate(chrom, ship_L, ship_W):
    out = []
    for v in chrom:
        vv = v.copy()
        if random.random() < 0.2:
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            x = vv["pos"][0] + dx
            y = vv["pos"][1] + dy

            # clamp boundaries
            x = min(max(x, -ship_L/2), ship_L/2)
            y = min(max(y, -ship_W/2), ship_W/2)

            vv["pos"] = (x,y)
        out.append(vv)
    return out

# ======================================================
# SELECTION (Tournament)
# ======================================================
def select(pop, scores):
    i1, i2 = random.sample(range(len(pop)), 2)
    return pop[i1] if scores[i1] < scores[i2] else pop[i2]

# ======================================================
# GA MAIN ENGINE
# ======================================================
def GA_arrange(items, ship_L, ship_W, cog_x, cog_y,
               pop_size=40, generations=150):

    target_x = cog_x - ship_L/2
    target_y = cog_y - ship_W/2

    # initial population
    pop = [random_chromosome(items, ship_L, ship_W) for _ in range(pop_size)]

    for gen in range(generations):
        scores = [fitness(p, ship_L, ship_W, target_x, target_y) for p in pop]

        new_pop = []

        for _ in range(pop_size):
            parent1 = select(pop, scores)
            parent2 = select(pop, scores)
            child = crossover(parent1, parent2)
            child = mutate(child, ship_L, ship_W)
            new_pop.append(child)

        pop = new_pop

    # choose best final
    scores = [fitness(p, ship_L, ship_W, target_x, target_y) for p in pop]
    best_idx = scores.index(min(scores))
    return pop[best_idx]
