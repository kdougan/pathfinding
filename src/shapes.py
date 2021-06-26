import pygame

from .maths import calc_point_normals


class Shape:
    __slots__ = ['points', 'flip', '_point_normals', '_segments']

    def __init__(self, points, pos=(0, 0), flip=False):
        self.points = [(point[0] + pos[0], point[1] + pos[1])
                       for point in points]
        self.flip = flip
        self._point_normals = None
        self._segments = []

    @property
    def point_normals(self):
        if self._point_normals is None:
            self._point_normals = calc_point_normals(
                self.points, flip=self.flip)
        return self._point_normals

    @ property
    def segments(self):
        if not self._segments:
            l = len(self.points)
            for i, point in enumerate(self.points):
                self._segments.append((point, self.points[(i+1) % l]))
        return self._segments

    def draw(self, surf, points=False, normals=False, path_nodes=False):
        pygame.draw.lines(
            surface=surf,
            color=(200, 0, 0),
            closed=True,
            points=[x[0] for x in self.segments]
        )
        if points:
            for i, point in enumerate(self.points):
                pygame.draw.circle(
                    surface=surf,
                    color=(0, 0, 200),
                    center=point,
                    radius=4
                )
        if normals and self.point_normals:
            for i, point in enumerate(self.points):
                if i not in self.point_normals:
                    continue
                pygame.draw.line(
                    surface=surf,
                    color=(0, 200, 200),
                    start_pos=point,
                    end_pos=self.point_normals[i]
                )
        if path_nodes:
            for point in self.point_normals.values():
                pygame.draw.circle(
                    surface=surf,
                    color=(0, 200, 0),
                    center=point,
                    radius=4
                )
