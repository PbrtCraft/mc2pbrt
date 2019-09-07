from tqdm import tqdm


def singleton(clz):
    instances = {}

    def getinstance(*args, **kwargs):
        if clz not in instances:
            instances[clz] = clz(*args, **kwargs)
        return instances[clz]
    return getinstance


def clamp(x, a=0., b=1.):
    """Limit value into [a, b]"""
    return max(min(x, b), a)


def tqdmpos(valx, valy, valz):
    total = len(valx)*len(valy)*len(valz)

    def ziptuple():
        for x in valx:
            for y in valy:
                for z in valz:
                    yield (x, y, z)

    for pos in tqdm(ziptuple(), total=total, ascii=True):
        yield pos


pt_map = {
    "east": (lambda c: (c[0]/2, 0, 0), lambda c: (c[1], c[2]), 1, "quadx"),
    "west": (lambda c: (-c[0]/2, 0, 0), lambda c: (c[1], c[2]), -1, "quadx"),
    "up": (lambda c: (0, c[1]/2, 0), lambda c: (c[0], c[2]), 1, "quady"),
    "down": (lambda c: (0, -c[1]/2, 0), lambda c: (c[0], c[2]), -1, "quady"),
    "north": (lambda c: (0, 0, c[2]/2), lambda c: (c[1], c[0]), 1, "quadz"),
    "south": (lambda c: (0, 0, -c[2]/2), lambda c: (c[1], c[0]), -1, "quadz")
}
