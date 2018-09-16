from graphics import *
from random import randint,choice,choices
import math
import  time


class Node(Circle):  # inherits from circle
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.center = Point(self.x, self.y)
        self.radius = radius
        super().__init__(self.center, self.radius)

        self.setFill(color_rgb(0x39, 0xff, 0x14))
        self.setOutline(color_rgb(0xff, 00, 0x85))
        self.setWidth(2)
        pass


class Layer(object):
    def __init__(self, node_num, x_pos=50):
        self.x_pos = x_pos
        self.node_num = node_num
        self.nodes = []
        Dy = 1000
        dy = Dy / (self.node_num + 2)
        for node in range(node_num):
            self.nodes.append(Node(self.x_pos, dy + dy * node))

    def draw(self, window):
        for node in range(len(self.nodes)):
            self.nodes[node].draw(window)

    def undraw(self):
        for node in range(len(self.nodes)):
            self.nodes[node].undraw()


class Edge(object):
    def __init__(self, node1, node2, resolution=25, curve=3):
        self.active = choice((True,True))
        self.weight = randint(0,4)
        self.colour = choice(("red","green","blue","yellow"))
        self.node1 = node1
        self.node2 = node2
        self.curve = curve
        self.Dx = int(abs(self.node2.center.x - self.node1.center.x))
        self.Dy = abs(self.node2.center.y - self.node1.center.y)
        self.resolution = resolution
        self.x_points = []
        self.y_points = []
        self.get_sigmoid()
        self.lines = []
        # print(self.x_points)
        # print(self.y_points)
        pass

    def get_sigmoid(self):
        if self.resolution % 2 == 0:
            for point in range(1, int(self.resolution / 2) + 1):
                self.x_points.append(point)
                self.x_points.append(point * -1)
            self.x_points.sort()
        else:
            for point in range(1, int(self.resolution / 2) + 1):
                self.x_points.append(point)
                self.x_points.append(point * -1)
            self.x_points.append(0)
            self.x_points.sort()
        # print(self.x_points)  # debug

        for index in range(len(self.x_points)):
            if self.node2.center.y > self.node1.center.y:
                self.y_points.append((self.Dy / (1.0 + math.exp(-1 / self.curve * self.x_points[index]))))
            else:
                self.y_points.append((self.Dy * math.exp(-1 / self.curve * self.x_points[index]) / (
                            1.0 + math.exp(-1 / self.curve * self.x_points[index]))))
            self.x_points[index] += self.x_points[-1]
            self.x_points[index] = (self.x_points[index] / self.resolution) * self.Dx

            # shift
            if self.node2.center.y > self.node1.center.y:
                self.x_points[index] += self.node1.center.x
                self.y_points[index] += self.node1.center.y
            else:
                self.x_points[index] += self.node1.center.x
                self.y_points[index] += self.node2.center.y

        # print(self.y_points)

    def draw(self, window):
        if not self.active:
            return

        for x in range(len(self.x_points) - 1):
            line = Line(Point(self.x_points[x], self.y_points[x]), Point(self.x_points[x + 1], self.y_points[x + 1]))
            line.setWidth(self.weight)
            line.setOutline(self.colour)
            self.lines.append(line)

        for line in self.lines:
            line.draw(window)

    def undraw(self):
        for line in self.lines:
            line.undraw()
        self.lines.clear()


class Net(object):
    def __init__(self, dimensions=(3, 5, 2)):
        self.layers = []
        self.edges = []
        pos = 100
        for x in dimensions:
            self.layers.append(Layer(x, pos))
            pos += 200

        for layer in range(len(self.layers) - 1):
            edges = []
            for node1 in self.layers[layer].nodes:
                for node2 in self.layers[layer + 1].nodes:
                    edges.append(Edge(node1, node2))
            self.edges.append(edges)

    def draw(self, window):
        for edge_list in self.edges:
            for edge in edge_list:
                edge.draw(window)

        for layer in self.layers:
            layer.draw(window)

    def undraw(self):
        for edge_list in self.edges:
            for edge in edge_list:
                edge.undraw()

        for layer in self.layers:
            layer.undraw()

    def loop(self,window):
        self.undraw()
        self.draw(window)
        while True:
            time.sleep(0.05)
            for x in range(len(self.edges)):
                self.layers[x].undraw()
                self.layers[x].draw(window)
                for edge in self.edges[x]:
                    edge.undraw()
                    edge.draw(window)
                self.layers[x].undraw()
                self.layers[x].draw(window)






def main():
    win = GraphWin("graph", 1200, 850)
    win.setCoords(0, 0, win.width, win.height)  # remove to reset co-ord system
    win.setBackground(color_hex("#001"))

    net1 = Net([4, 6, 8, 6, 3, 2])
    net1.loop(win)

    while True:
        net1.draw(win)
        net1.undraw()




main()
