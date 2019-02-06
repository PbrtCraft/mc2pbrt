def laglongToCoord(theta, phi):
    """Convert lagtitude and longitude to xyz coordinate."""
    from math import cos, sin, pi
    theta, phi = theta/180*pi, phi/180*pi
    return sin(theta)*cos(phi), sin(phi), cos(theta)*cos(phi)

def firstPerson(player):
    """First person perspective"""
    theta, phi = map(lambda x: -x, player.rot)
    sx, sy, sz = player.pos
    tx, ty, tz = laglongToCoord(theta, phi)
    nx, ny, nz = laglongToCoord(theta, phi + 90)
    map_eye_y = sy + 1.8 - 1
    return (sx, map_eye_y, sz, sx + tx, map_eye_y + ty, sz + tz, nx, ny, nz)
