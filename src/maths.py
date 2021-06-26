import math


def calc_point_normals(points, length=12, flip=False):
    def angle(x1, y1, x2, y2):
        numer = (x1 * x2 + y1 * y2)
        denom = math.sqrt((x1 ** 2 + y1 ** 2) * (x2 ** 2 + y2 ** 2))
        return math.acos(numer / denom)

    def cross_sign(x1, y1, x2, y2):
        return x1 * y2 < x2 * y1

    norms = {}
    flip = math.pi if not flip else 0
    l = len(points)
    for i, ref in enumerate(points):
        p1, p2 = points[(i-1) % l], points[(i+1) % l]
        x1, y1 = p1[0] - ref[0], p1[1] - ref[1]
        x2, y2 = p2[0] - ref[0], p2[1] - ref[1]
        t = math.atan2(y2, x2)
        a = angle(x1, y1, x2, y2)
        if cross_sign(x1, y1, x2, y2):
            x = math.cos(a/2+flip+t) * length
            y = math.sin(a/2+flip+t) * length
            if flip:
                norms[i] = (ref[0]+x, ref[1]+y)
        else:
            if not flip:
                x = math.cos(math.pi-a/2+t+flip) * length
                y = math.sin(math.pi-a/2+t+flip) * length
                norms[i] = (ref[0]+x, ref[1]+y)
    return norms


def intersects(s0, s1):
    dx0 = s0[1][0]-s0[0][0]
    dx1 = s1[1][0]-s1[0][0]
    dy0 = s0[1][1]-s0[0][1]
    dy1 = s1[1][1]-s1[0][1]
    p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
    p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
    p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
    p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
    return (p0*p1 <= 0) & (p2*p3 <= 0)


def intersects_circle(l, c, cr):
    x1, y1 = l[0]
    x2, y2 = l[1]
    cx, cy = c
    x1 -= cx
    x2 -= cx
    y1 -= cy
    y2 -= cy
    dx = x2 - x1
    dy = y2 - y1
    dr_squared = dx**2 + dy**2
    D = x1*y2 - x2*y1
    return cr**2 * dr_squared > D**2


def line_intersects_shapes(line1, shapes):
    for shape in shapes:
        for i, s in enumerate(shape.points):
            l = len(shape.points)
            line2 = [s, shape.points[(i+1) % l]]
            if intersects(line1, line2):
                return True
            norm = shape.point_normals.get(i)
            if (
                norm
                and intersects(line1, (s, norm))
                and line1[0] != norm
                and line1[1] != norm
            ):
                return True
    return False
