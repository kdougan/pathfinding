import enum
import heapq
import math
import pygame

from itertools import count
from .maths import line_intersects_shapes


class NodeType(enum.Enum):
    OPEN = 1
    CLOSED = 2
    START = 3
    END = 4
    PATH = 5


class PathNode(pygame.math.Vector2):
    __slots__ = ['connected', 'type', 'id', 'dirty']
    _counter = iter(count())

    def __init__(self, point, type=NodeType.OPEN):
        super().__init__(point)
        self.id = next(PathNode._counter)
        self.connected = set()
        self.type = type
        self.dirty = True

    def __repr__(self):
        return str(self.coord)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    @property
    def coord(self):
        return (int(self.x), int(self.y))

    @property
    def color(self):
        return {
            NodeType.OPEN: (41, 157, 143),
            NodeType.CLOSED: (38, 70, 83),
            NodeType.START: (233, 196, 106),
            NodeType.END: (231, 111, 81),
            NodeType.PATH: (244, 162, 97)
        }.get(self.type)

    def calc_connecting_nodes(self, nodes, shapes=[]):
        self.connected = set()
        for node in nodes:
            if self == node:
                continue
            intersects = line_intersects_shapes((self, node), shapes)
            if intersects:
                if self in node.connected:
                    node.connected.remove(self)
            else:
                self.connected.add(node)
                node.connected.add(self)
        self.dirty = False

    def draw(self, surf, connecting=False):
        pygame.draw.circle(
            surface=surf,
            color=(200, 200, 0),
            center=self,
            radius=4
        )
        if connecting:
            for node in self.connected:
                pygame.draw.line(
                    surface=surf,
                    color=(200, 200, 200, .2),
                    start_pos=self,
                    end_pos=node
                )


class PriorityQueue:
    __slots__ = ['elements']

    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority, h):
        heapq.heappush(self.elements, (priority, h, item))

    def get(self):
        return heapq.heappop(self.elements)[2]


def distance_between(a, b):
    return math.sqrt(abs(a.x-b.x)**2 + abs(a.y-b.y)**2)


def find_path(start, end):
    frontier = PriorityQueue()
    frontier.put(start, 0, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start.id] = None
    cost_so_far[start.id] = 0
    i = 1
    while not frontier.empty():
        current_node = frontier.get()
        if current_node == end:
            break
        for next_node in current_node.connected:
            new_cost = cost_so_far[current_node.id] + 1
            if next_node.id not in cost_so_far or new_cost < cost_so_far[next_node.id]:
                cost_so_far[next_node.id] = new_cost
                priority = new_cost + distance_between(next_node, end)
                frontier.put(next_node, priority, i)
                i += 1
                came_from[next_node.id] = current_node
    return reconstruct_path(came_from, start, end)


def reconstruct_path(came_from, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current.id)
        if not current:
            return None
    path.append(start)
    path.reverse()
    return path
