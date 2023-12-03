import os
from queue import PriorityQueue

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Vertice:
    def __init__(self, coordinate, cost):
        self.coordinate = coordinate
        self.cost = cost

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_vertice(self, x, y, cost):
        new_vertice_key = (x, y)
        if new_vertice_key in self.vertices:
            raise ValueError(f'O vertice ({x}, {y}) já foi adicionado')
        
        coordinate = Coordinate(x, y)
        new_vertice = Vertice(coordinate, cost)
        self.vertices[new_vertice_key] = new_vertice

    def get_vertice(self, x, y) -> Vertice:
        vertice = (x, y)
        if vertice not in self.vertices:
            raise ValueError(f'O vertice ({x}, {y}) não existe')
        
        return self.vertices[vertice]
        
    def add_edge(self, from_vertice, to_vertice):
        from_x = from_vertice.coordinate.x
        from_y = from_vertice.coordinate.y

        to_x = to_vertice.coordinate.x
        to_y = to_vertice.coordinate.y

        vertice_key = (from_x, from_y)

        if vertice_key not in self.edges:
            self.edges[vertice_key] = []

        vertices = self.edges[vertice_key]
        if to_vertice not in vertices:
            vertices.append(to_vertice)

    def get_neighbors(self, vertice):
        x = vertice.coordinate.x
        y = vertice.coordinate.y

        vertice_key = (x, y)
        if vertice_key not in self.edges:
            raise ValueError(f'O vertice ({x}, {y}) não possui vizinhos')

        return self.edges[vertice_key]

class InputFile:
    def __init__(self, first_line, second_line, other_lines):
        self.size = self.__get_size__(first_line)
        self.matrix = self.__get_matrix__(other_lines)
        self.start = self.__get_start__(second_line)
        self.end = self.__get_end__()

    def get_graph(self) -> Graph:
        graph = Graph()

        self.__add_vertices__(graph)
        self.__add_edges__(graph)

        return graph

    def __add_vertices__(self, graph):
        line_count = 0

        while line_count < self.size.height:
            column_count = 0

            while column_count < self.size.width:
                graph.add_vertice(column_count, line_count, self.matrix[line_count][column_count])
                column_count += 1
            
            line_count += 1

    def __add_edges__(self, graph):
        line_count = 0

        while line_count < self.size.height:
            column_count = 0

            while column_count < self.size.width:
                vertice = graph.get_vertice(column_count, line_count)

                # top
                if line_count - 1 >= 0 and self.matrix[line_count - 1][column_count] >= 0:
                    top_neighbor = graph.get_vertice(column_count, line_count - 1)
                    graph.add_edge(vertice, top_neighbor)

                # left
                if column_count - 1 >= 0 and self.matrix[line_count][column_count - 1] >= 0:
                    left_neighbor = graph.get_vertice(column_count - 1, line_count)
                    graph.add_edge(vertice, left_neighbor)

                # bottom
                if line_count + 1 < len(self.matrix) and self.matrix[line_count + 1][column_count] >= 0:
                    bottom_neighbor = graph.get_vertice(column_count, line_count + 1)
                    graph.add_edge(vertice, bottom_neighbor)

                # right
                if column_count + 1 < len(self.matrix[0]) and self.matrix[line_count][column_count + 1] >= 0:
                    right_neighbor = graph.get_vertice(column_count + 1, line_count)
                    graph.add_edge(vertice, right_neighbor)

                column_count += 1
            
            line_count += 1

    def __get_size__(self, line):
        if len(line) <= 2:
            raise ValueError('A primeira linha deve possuir pelo menos 3 caracteres')
    
        elements = line.split()
        if len(elements) != 2:
            raise ValueError('A primeira linha deve possuir pelo menos 2 elementos (largura, altura)')
        
        width = int(elements[0])
        height = int(elements[1])

        return Size(width, height)
    
    def __get_matrix__(self, lines):
        width = self.size.width
        height = self.size.height

        if len(lines) != height:
            raise ValueError('A quantidade de linhas do mapa não pode ser diferente da sua altura')
        
        matrix = []
        line_count = 0
        while line_count < height:
            matrix.append([])
            line = lines[line_count]
            elements = line.strip().split()
            if len(elements) != width:
                raise ValueError('A quantidade de colunas do mapa não pode ser diferente da sua largura')
            
            column_count = 0
            while column_count < width:
                cost = int(elements[column_count])
                if cost < -1:
                    raise ValueError('Os valores não podem ser menores que -1')
                
                matrix[line_count].append(cost)
                column_count += 1
            line_count += 1

        return matrix
    
    def __get_start__(self, line) -> Coordinate:
        width = self.size.width
        height = self.size.height

        if len(line) <= 2:
            raise ValueError('A segunda linha deve possuir pelo menos 3 caracteres')
        
        elements = line.strip().split()
        if len(elements) != 2:
            raise ValueError('A segunda linha deve possuir pelo menos 2 elementos (x, y)')
        
        x = int(elements[0])
        y = int(elements[1])

        if x < 0 or y < 0:
            raise ValueError('Os valores da coordenada não podem ser menores que zero')

        if x > width - 1:
            raise ValueError('O eixo x da posição inicial não pode ser maior que a quantidade de colunas')
        
        if y > height - 1:
            raise ValueError('O eixo y da posição inicial não pode ser maior que a quantidade de linhas')
        
        if self.matrix[y][x] < 0:
            raise ValueError('A posição inicial não pode estar em um local inacessível')

        return Coordinate(x, y)
    
    def __get_end__(self):
        while True:
            _input = input('Informe a coordenada de destino: (formato: \'x y\'): ')
            elements = _input.strip().split()

            if len(elements) != 2:
                print('A entrada deve possuir apenas 2 elementos')
                continue

            try:
                vertice = Coordinate(int(elements[0]), int(elements[1]))

                x = vertice.x
                y = vertice.y

                width = self.size.width
                height = self.size.height

                if x < 0 or y < 0:
                    raise ValueError('Os valores da coordenada não podem ser menores que zero')

                if x > width - 1:
                    raise ValueError('O eixo x da posição final não pode ser maior que a quantidade de colunas')
                
                if y > height - 1:
                    raise ValueError('O eixo y da posição final não pode ser maior que a quantidade de linhas')
                
                if self.matrix[y][x] < 0:
                    raise ValueError('A posição final não pode estar em um local inacessível')

                if x < 0 or y < 0:
                    raise ValueError('Os valores da coordenada não podem ser menores que zero')

                return vertice
                
            except ValueError as exception:
                print(exception)

def get_current_directory():
    return os.getcwd()

def get_map_file_path(current_directory):
    return os.path.join(current_directory, 'map.txt')       

def get_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines
    
def heuristic(_from, to):
    from_coordinate = _from.coordinate
    from_x = from_coordinate.x
    from_y = from_coordinate.y

    to_coordinate = to.coordinate
    to_x = to_coordinate.x
    to_y = to_coordinate.y

    return abs(from_x - to_x) + abs(from_y - to_y)

def a_star_search(graph, start_coordinate, end_coordinate):
    start_x = start_coordinate.x
    start_y = start_coordinate.y
    start_key = (start_x, start_y)

    end_x = end_coordinate.x
    end_y = end_coordinate.y
    end_key = (end_x, end_y)

    start_vertice = graph.get_vertice(start_x, start_y)
    end_vertice = graph.get_vertice(end_x, end_y)

    memo = {start_key: {'cost': start_vertice.cost, 'from': None}}

    priority = PriorityQueue()
    priority.put((0, start_key))

    while not priority.empty():
        (_, current_vertice_key) = priority.get()

        if current_vertice_key == end_key:
            break

        current_vertice = graph.get_vertice(current_vertice_key[0], current_vertice_key[1])

        for next_vertice in graph.get_neighbors(current_vertice):
            next_vertice_key = (next_vertice.coordinate.x, next_vertice.coordinate.y)
            new_cost = memo[current_vertice_key]['cost'] + next_vertice.cost + 1
            if next_vertice_key not in memo or new_cost < memo[next_vertice_key]['cost']:
                memo[next_vertice_key] = {'cost': new_cost, 'from': current_vertice_key}
                priority.put((new_cost + heuristic(end_vertice, next_vertice), next_vertice_key))

    return memo

def get_path_and_cost(result, end_coordinate, start_coordinate):
    end_key = (end_coordinate.x, end_coordinate.y)
    start_key = (start_coordinate.x, start_coordinate.y)
    path = [end_key]
    current_path = result[end_key]['from']

    if current_path is None:
        return path

    path.append(current_path)
    while current_path != start_key:
        current_path = result[current_path]['from']
        path.append(current_path)

    path.reverse()
    return (path, result[end_key]['cost'])

def get_best_path(path):
    best_path = dict()

    vertice_count = len(path) - 1

    while vertice_count > 0:
        vertice = path[vertice_count]
        (vertice_x, vertice_y) = vertice
        previous_vertice = path[vertice_count - 1]
        (previous_vertice_x, previous_vertice_y) = previous_vertice
        difference = (vertice_x - previous_vertice_x, vertice_y - previous_vertice_y)
        symbols = {
            (-1, 0): ' < ',
            (1, 0): ' > ',
            (0, 1): ' v ',
            (0, -1): ' ^ '
        }
        value = symbols[difference]
        best_path[previous_vertice] = value
        vertice_count -= 1
    
    return best_path

def print_path(path, inputFile):
    start_coordinate = inputFile.start
    start_key = (start_coordinate.x, start_coordinate.y)
    end_coordinate = inputFile.end
    end_key = (end_coordinate.x, end_coordinate.y)
    size = inputFile.size
    line_count = 0
    best_path = get_best_path(path)
    while line_count < size.height:
        column_count = 0
        line = ''
        while column_count < size.width:
            coordinate = (column_count, line_count)
            cost = inputFile.matrix[line_count][column_count]
            if coordinate == start_key:
                line += ' S '
            elif coordinate == end_key:
                line += ' E '
            elif coordinate in best_path:
                line += best_path[coordinate]
            elif cost < 0:
                line += ' ■ '
            else:
                line += f' {cost:2d} '

            column_count += 1

        print(line + '\n')
        line_count += 1

def print_exit(cost, coordinates):
    exit = f'{cost}'
    count = 0
    while count < len(coordinates):
        coordinate = coordinates[count]
        (x, y) = coordinate
        exit += f'  {x},{y}'
        count += 1
    print(exit)

if __name__ == '__main__':
    current_directory = get_current_directory()
    file_path = get_map_file_path(current_directory)
    file_lines = get_file_lines(file_path)
    if len(file_lines) < 3:
        raise ValueError('A definição do mapa deve possuir pelo menos 3 linhas!')
    
    inputFile = InputFile(file_lines[0], file_lines[1], file_lines[2:])

    start = inputFile.start
    end = inputFile.end

    graph = inputFile.get_graph()
    result = a_star_search(graph, start, end)
    (path, cost) = get_path_and_cost(result, end, start)
    print_path(path, inputFile)
    print_exit(cost, path)
    
def get_path_and_cost(result, end_coordinate, start_coordinate):
    end_key = (end_coordinate.x, end_coordinate.y)
    start_key = (start_coordinate.x, start_coordinate.y)
    path = [end_key]
    current_path = result[end_key]['from']

    if current_path is None:
        return path

    while current_path != start_key:
        path.append(current_path)
        current_path = result[current_path]['from']

    path.append(start_key)
    path.reverse()

    return (path, result[end_key]['cost'])