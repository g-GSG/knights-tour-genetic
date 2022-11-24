import random

class Chromossome:
    genes = []
    fitness = 0

    def __init__(self, genes):
        if (genes):
            self.genes = genes
        else:
            # generate random genes cols * cols ?
            self.genes = [random.randint(1, 8) for i in range(64)]

    def crossover(self, partner):
        new_genes = []

        # pick a mid divider that will determine which gene to take for the current tour 
        mid = random.randint(0, len(self.genes) - 1)

        for i in range(cols*cols - 1):
            if (i > mid):
                new_genes.append(self.genes[i])
            else:
                new_genes.append(partner.genes[i])

    def mutation(self):
        for i in range(len(self.genes)):
            if (random.random() < 0.01):
                self.chromossome.genes[i] = random.randint(1, 9)


class Knight:
    x = 0
    y = 0
    steps = 0

    path = []
    fitness = 0

    findForward = False 

    def __init__(self, x, y, steps, chromossome):
        self.x = x
        self.y = y
        self.steps = steps
        self.path.append([x, y])
        self.findForward =  bool(random.getrandbits(1))
            
        if (chromossome):
            self.chromossome = chromossome
        else:
            # intitialize a new random chromossome
            self.chromossome = chromossome(None)

    def move_forward(direction):
        match direction:
            case 1:
                self.x += 1
                self.y -= 2
            case 2:
                self.x += 2
                self.y -= 1
            case 3:
                self.x += 2
                self.y += 1
            case 4:
                self.x += 1
                self.y += 2
            case 5:
                self.x -= 1
                self.y += 2
            case 6:
                self.x -= 2
                self.y += 1
            case 7:
                self.x -= 2
                self.y -= 1
            case 8:
                self.x -= 1
                self.y -= 2

    def traceback(direction):
        match direction:
            case 1:
                self.x -= 1
                self.y += 2
            case 2:
                self.x -= 2
                self.y += 1
            case 3:
                self.x -= 2
                self.y -= 1
            case 4:
                self.x -= 1
                self.y -= 2
            case 5:
                self.x += 1
                self.y -= 2
            case 6:
                self.x += 2
                self.y -= 1
            case 7:
                self.x += 2
                self.y += 1
            case 8:
                self.x += 1
                self.y += 2

    def move(self):
        legal = false
        limit = 0

        while (not legal and (limit + 1) < 8):
            self.move_forward(self.chromossome.genes[self.steps])

            if ((self.x>=0 and self.x<cols) and (self.y>=0 and self.y<cols)):
                legal = True
                for i in range(len(self.path)):
                    if (self.path[i].x == self.x and self.path[i].y == self.y): # ta estranho [i][0] e [i][1]
                        legal = false
            if (not legal):
                self.traceback(self.chromossome.genes[self.steps])
                if (self.findForward):
                    self.chromossome.genes[self.steps] = (self.chromossome.genes[self.steps] % 8) + 1
                else:
                    self.chromossome.genes[self.steps] = ((self.chromossome.genes[self.steps]+6) % 8) + 1

        self.path.append([self.x, self.y])
        self.steps += 1

    def calculate_fitness(self):
        legal = True
        self.fitness = 0

        for i in range(len(self.path)):
            if (self.path[i].x<0 or self.path[i].x>cols-1 or self.path[i].y<0 or self.path[i].y>cols-1):
                legal = False
            for j in range(i):
                if (self.path[i].x == self.path[j].x and self.path[i].y == self.path[j].y):
                    legal = False

            if (not legal):
                return

            self.fitness += 1

class Population:
    generation = 1
    knights = []
    popsize = 0
    matingpool = []
    
    def __init__(self, popsize):
        self.popsize = popsize
        for i in range(popsize):
            self.knights.append(knight(0, 0, 0, None))

    def run(self):
        for i in range(cols * cols - 1):
            for j in range(self.popsize):
                self.knights[j].move()

    def evaluate(self):
        max_fit = 0
        best_knight = None

        for i in range(self.popsize):
            self.knights[i].calculate_fitness()

            if (self.knights[i].fitness > max_fit):
                max_fit = self.knights[i].fitness
        
        for i in range(self.popsize):
            self.knights[i].fitness /= max_fit

        self.matingpool = []

        for i in range(self.popsize):
            n = self.knights[i].fitness * 100

            for j in range(n):
                self.matingpool.append(self.knights[i])
        
        if(max_fit == cols * cols): # num sei se ta certo
            best_knight = self.knights[i]
            print("Generation: ", self.generation)
            print("Best Knight: ", best_knight.path)
            print("Fitness: ", best_knight.fitness)
            return True
        
        self.generation += 1

    def selection(self):
        new_knights = []

        for i in range(self.popsize):
            parent1 = random.choice(self.matingpool).chromossome
            parent2 = random.choice(self.matingpool).chromossome

            child = parent1.crossover(parent2)

            child.chromossome.mutation()
            # add the new knight to the array
            new_knights.append(knight(0, 0, 0, child)) # child ou child.chromossome ?

        self.knights = new_knights

        
def main(): # ???
    population = Population(50)
    cols = 8