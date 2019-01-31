# For float tuple calculate
plus = lambda p, q: tuple(map(float, [p[i]+q[i] for i in range(3)]))
minus = lambda p, q: tuple(map(float, [p[i]-q[i] for i in range(3)]))
mult = lambda xs, f: tuple(map(float,[x*f for x in xs]))

# For int tuple calculate
plus_i = lambda p, q: tuple(map(int, [p[i]+q[i] for i in range(3)]))
mult_i = lambda xs, i: tuple(map(int, [x*i for x in xs]))
