import pygame

from .paths import PathNode
from .paths import distance_between
from .paths import find_path
from .shapes import Shape


class Game:
    def __init__(self):
        successes, failures = pygame.init()
        print('init: {0} successes and {1} failures'.format(
            successes, failures))

        pygame.display.set_caption('minimal program')

        self.screen = pygame.display.set_mode(
            (1280, 720), pygame.DOUBLEBUF, 16)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)

        self.running = True

        self.shapes = []
        self.path_nodes = []

    def show_fps(self):
        return self.font.render(
            str(int(self.clock.get_fps())),
            1, pygame.Color('coral'))

    def run(self):

        self.add_shape(
            Shape(points=[(0, 0),
                          (1260, 0),
                          (1260, 700),
                          (0, 700)],
                  pos=(10, 10),
                  flip=True)
        )
        for pos in [(120, 100), (300, 120), (420, 200), (600, 400), (100, 500)]:
            self.add_shape(
                Shape(points=[(0, 0),
                              (100, 0),
                              (100, 100),
                              (0, 100)],
                      pos=pos)
            )
        self.player = Player(5, 5, 10, 10)
        self.path_nodes.append(self.player.path_node)

        self.enemy = Player(1200, 650, 10, 10)
        self.path_nodes.append(self.enemy.path_node)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.enemy.target = None if self.enemy.target else self.player

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                self.player.vel.x -= 5
            if pressed[pygame.K_d]:
                self.player.vel.x += 5
            if pressed[pygame.K_w]:
                self.player.vel.y -= 5
            if pressed[pygame.K_s]:
                self.player.vel.y += 5

            self.calc_connecting_nodes()
            self.update()
            self.render()
            self.clock.tick(60)

    def add_shape(self, shape):
        self.shapes.append(shape)
        for point in shape.point_normals.values():
            self.path_nodes.append(PathNode(point))

    def calc_connecting_nodes(self):
        for node in [n for n in self.path_nodes if n.dirty]:
            node.calc_connecting_nodes(self.path_nodes, self.shapes)

    def update(self):
        self.player.update()
        self.enemy.update()

    def render(self):
        self.screen.fill((20, 20, 20))

        for shape in self.shapes:
            shape.draw(self.screen)

        for node in self.path_nodes:
            node.draw(self.screen)

        if self.enemy.path:
            for node in self.enemy.path:
                pygame.draw.lines(
                    self.screen, (200, 200, 200, .2), False, self.enemy.path)

        self.enemy.draw(self.screen)
        self.player.draw(self.screen)

        self.screen.blit(self.show_fps(), (0, 0))
        pygame.display.flip()


class Player:
    def __init__(self, x, y, w, h):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.size = (w, h)
        self.path_node = PathNode((x, y))
        self.target = None
        self.path = None
        self.max_vel = 2

    @property
    def rect(self):
        return pygame.Rect(self.pos, self.size)

    def update(self):
        self.path = None
        if self.target:
            path = find_path(self.path_node, self.target.path_node)
            if path and len(path) > 1:
                self.path = path
                node = path[1]
                ease = (node == self.target.path_node and
                        distance_between(self.path_node, node) < 100)
                self.move_toward(node, ease)

        if self.vel.x == 0 and self.vel.y == 0:
            return

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.path_node.x = self.pos.x
        self.path_node.y = self.pos.y
        self.path_node.dirty = True
        self.vel.x, self.vel.y = 0, 0

    def move_toward(self, point, ease=True):
        dx, dy = point.x - self.pos.x, point.y - self.pos.y
        if ease:
            dx, dy = dx / 25, dy / 25
        if max(abs(dx), abs(dy) > self.max_vel):
            diff_x = (abs(dx) - self.max_vel) / abs(dx)
            diff_y = (abs(dy) - self.max_vel) / abs(dy)
            scale = diff_x if diff_x > diff_y else diff_y
            dx, dy = dx * (1 - scale), dy * (1 - scale)
        self.vel.x = dx
        self.vel.y = dy

    def draw(self, surf):
        pygame.draw.rect(
            surface=surf,
            color=(200, 0, 200),
            rect=self.rect
        )
