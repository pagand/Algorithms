import time
def costfun(solution):
    # [x1*x1 , x2*x1, x2*x2, x3*x1, x3*x2, x3*x3]
    cost = 0
    q = [-6, 5, -2, -5, 1, -4]
    sol = [solution[0]*solution[0],solution[1]*solution[0], solution[1]*solution[1],
            solution[2]*solution[0],solution[2]*solution[1], solution[2]*solution[2]]
    for i in range(len(q)):
        cost += sol[i]*q[i]
    return cost


def aspirationcriteria(sol, tabuSolutions):
    sol = "".join(map(str, sol))
    if tabuSolutions:
        if sol in tabuSolutions:
            return False
        else:
            return True
    else:
        return True

class TabuSearch:
    def __init__(self, fun, length, num_iter, list_size, timeout,
                 tabuTenure = 10 ,aspirationCriteria = aspirationcriteria, initialSolution = False, *args):
        '''

        :param fun: calleble funciton to evaluate the current solution
        :param length: integer value that tell the length of the search space
        :param num_iter: integer maximum number of evaluation
        :param list_size: integer maximum tabu list size
        :param timeout: maximum allocated time for optimization
        :param tabuTenure: integer value to tell how long a solution should be in tabu list
        :param aspirationCriteria: accept/reject solution based on tabu list
        :param initialSolution: optional Binary variable if any initilization is provided
        :param args: optioanl parameter for initialization
        '''
        self.length = length
        if initialSolution:
            solution = args
        else:
            solution = [0 for i in range(length)]

        self.currSolution = solution
        self.bestSolution = solution
        self.evaluate = fun
        self.aspirationCriteria = aspirationCriteria
        self.tabuTenure = tabuTenure
        self.num_iter = num_iter
        self.list_size = list_size
        self.timeout = timeout

    def neighboroperator(self, solution):
        neighbor = []
        for i in range(len(solution)):
            tmp = solution.copy()
            tmp[i] = int(not solution[i])
            neighbor.append(tmp)
        return neighbor



    def isTerminationCriteriaMet(self, startTime, currentIter):
        # can add more termination criteria
        currentTime = time.time()
        return (currentTime - startTime) > self.timeout or currentIter > self.num_iter

    def run(self):
        tabuList = {}
        startTime = time.time()
        currentIter = 0

        while not self.isTerminationCriteriaMet(startTime, currentIter):
            # get all of the neighbors
            neighbors = self.neighboroperator(self.currSolution)
            # find all tabuSolutions other than those
            # that fit the aspiration criteria
            tabuSolutions = tabuList.keys()
            # find all neighbors that are not part of the Tabu list
            neighbors = filter(lambda n: self.aspirationCriteria(n, tabuSolutions), neighbors)
            # pick the best neighbor solution
            newSolution = sorted(neighbors, key=lambda n: self.evaluate(n))[0]
            # get the cost between the two solutions
            cost = self.evaluate(self.bestSolution) - self.evaluate(newSolution)
            # if the new solution is better,
            # update the best solution with the new solution
            if cost >= 0:
                self.bestSolution = newSolution
            # update the current solution with the new solution
            self.currSolution = newSolution

            # decrement the Tabu Tenure of all tabu list solutions
            for sol in tabuList:
                tabuList[sol] -= 1
                if tabuList[sol] == 0:
                    del tabuList[sol]
            # add new solution to the Tabu list
            tabuList["".join(map(str, newSolution))] = self.tabuTenure

            # check the size of Tabu list
            if len(tabuList)>self.list_size:
                del tabuList[sorted(tabuList, key=tabuList.get)[0]]

            # add iteration
            currentIter += 1

        # return best solution found
        return self.bestSolution


def main():
    search = TabuSearch(fun=costfun, length=3, num_iter=100, list_size=2, timeout=10)
    print(search.run())

if __name__ == "__main__":
    main()