# For float tuple calculate
plus = lambda p, q: tuple(map(float, [p[i]+q[i] for i in range(3)]))
minus = lambda p, q: tuple(map(float, [p[i]-q[i] for i in range(3)]))
mult = lambda p, f: tuple([float(p[i])*f for i in range(3)])

# For int tuple calculate
plus_i = lambda p, q: tuple(map(int, [p[i]+q[i] for i in range(3)]))
