def clamp(x, a=0., b=1.):
    """Limit value into [a, b]"""
    return max(min(x, b), a)

pt_map = {
    "east"  : (lambda c: (c[0]/2, 0, 0), lambda c: (c[1], c[2]), 1, "quadx"),
    "west"  : (lambda c: (-c[0]/2, 0, 0), lambda c: (c[1], c[2]), -1, "quadx"),
    "up"    : (lambda c: (0, c[1]/2, 0), lambda c: (c[0], c[2]), 1, "quady"),
    "down"  : (lambda c: (0, -c[1]/2, 0), lambda c: (c[0], c[2]), -1, "quady"),
    "north" : (lambda c: (0, 0, c[2]/2), lambda c: (c[1], c[0]), 1, "quadz"),
    "south" : (lambda c: (0, 0, -c[2]/2), lambda c: (c[1], c[0]), -1, "quadz")
}
