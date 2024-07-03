from collections import defaultdict
import datetime as dt
import random
import pickle
import pprint

currCoreProblems = [15, 310, 79, 621]
# not using...
completedTracking = {
    15: 1,
    310: 9,
    79: 8,
    621: 5
}

# only difference here is that this PS accepts a pkl filepath as optional instantiator, 
# but not using bc I'm not sure best way to read/write from a pkl w/out risking blowing it all away
# so instead staying w/ primary problemServer and just listing my completions each day

class ProblemSet:
    """
    Represents a set of problems and their completion status.

    Attributes:
        problems (list): A list of problems in the problem set.
        tracker (defaultdict): A dictionary that tracks the number of times each problem has been completed.
        completionCalendar (defaultdict): A nested dictionary that stores the completion dates and times for each problem.
        redoInterval (int): The number of days after which a problem can be attempted again.

    Methods:
        __init__(problems): Initializes a ProblemSet object with the given list of problems.
        __str__(): Prints the completion calendar of the problem set.
        serialize(): Serializes the problem set data and saves it to a file.
        deserialize(): Deserializes the problem set data from a file.
        addProblem(problem): Adds a new problem to the problem set.
        timeFormatter(time): Formats the given time in minutes and seconds.
        completeProblem(problem, timeTaken, dateCompleted, solutionChecked): Marks a problem as completed with the given details.
        genProblemList(numProblems, include, exclude): Generates a list of problems to work on.
        hardestProblems(numProblems, timeWindow): Returns the hardest problems based on completion times.
        bestTimes(problems): Returns the best completion times for the given problems.
    """
    def __init__(self, picklePath="", problems=[]):
        self.problems = problems
        self.tracker = defaultdict(int)
        self.completionCalendar = defaultdict(self.ddNester)
        self.redoInterval = 5
        if picklePath:
            self.deserialize(picklePath)

    def __str__(self) -> str:
        self.deserialize()
        prettyProblems = {}
        for problem, dates in self.completionCalendar.items():
            res = {}
            for date, completions in dates.items():
                fDate = date.strftime("%m-%d-%y")
                res[fDate] = [[self.timeFormatter(x[0]), x[1]] for x in completions]
            res["Number of Completions"] = len(res.keys())
            prettyProblems[problem] = res
        print("Completion Calendar: ")
        pprint.pprint(prettyProblems)
        return "\n"

    def ddNester(self):
        return defaultdict(set)

    def serialize(self):
        """
        Should be used after any state-changing operation.
        """
        with open("problemLogs/problemSetLog.pickle", "wb") as out:
            allTheGoods = {"problems": self.problems, 
                           "tracker": self.tracker, 
                           "completionCalendar": self.completionCalendar}
            pickle.dump(allTheGoods, out)

    def deserialize(self, filePath="problemLogs/problemSetLog.pickle"):
        """
        Should be used *before* any state-checking or -changing operation to ensure working w/ freshest data.
        """
        with open(filePath, "rb") as incoming:
            returnedGoods = pickle.load(incoming)
            self.problems = returnedGoods["problems"]
            self.tracker = returnedGoods["tracker"]
            self.completionCalendar = returnedGoods["completionCalendar"]

    def addProblem(self, problem):
        """
        Adds a new problem to the problem set.

        Args:
            problem (str): The problem to be added.

        Returns:
            None
        """
        self.deserialize()
        self.problems.append(problem)
        self.serialize()

    def timeFormatter(self, time):
        """
        Formats the given time in minutes and seconds.

        Args:
            time (int): The time in seconds.

        Returns:
            str: The formatted time in the format "mm:ss".
        """
        sec = time % 60
        if sec < 10:
            sec = f"0{sec}"
        return f"{time // 60}:{sec}"
    
    def dateConverter(self, dateString):
        dtObject = dt.datetime.strptime(dateString, "%m-%d-%y")
        return dtObject
    
    def completeProblem(self, problem, timeTaken, dateCompleted=None, solutionChecked=False):
        """
        Marks a problem as completed with the given details.

        Args:
            problem (str): The problem to be marked as completed.
            timeTaken (str): The time taken to complete the problem in the format "mm:ss".
            dateCompleted (str, optional): The date when the problem was completed in the format "mm-dd-yy".
                If not provided, the current date is used.
            solutionChecked (bool, optional): Indicates whether the solution was checked. Default is False.

        Returns:
            None
        """
        self.deserialize()
        timeTakenArray = timeTaken.split(":")
        timeTakenSec = int(timeTakenArray[0]) * 60 + int(timeTakenArray[1])
        if dateCompleted == None:
            completedDT = dt.datetime.now()
        else:
            completedDT = self.dateConverter(dateCompleted)
        self.completionCalendar[problem][completedDT].add((timeTakenSec, solutionChecked))
        self.tracker[problem] += 1
        if problem not in self.problems:
            self.problems.append(problem)
        self.serialize()

    def genProblemList(self, numProblems=5, include=[], exclude=[]):
        """
        Generates a list of problems to work on.

        Args:
            numProblems (int, optional): The number of problems to include in the list. Default is 5.
            include (list, optional): A list of problems to include in the list.
            exclude (list, optional): A list of problems to exclude from the list.

        Returns:
            list: A list of problems to work on.
        """
        self.deserialize()
        res = []
        count = numProblems
        randProblems = [x for x in self.problems if x not in exclude]
        random.shuffle(randProblems)
        remains = []
        if include:
            for problem in include:
                res.append(problem)
                count -= 1
                randProblems.remove(problem)
        for problem in randProblems:
            completedDates = sorted([x for x in self.completionCalendar[problem].keys()])
            # grabbing the completion with the smallest time for a given day (in the case of their being multiple on a day)
            completionResult = min(self.completionCalendar[problem][completedDates[-1]], key=lambda x: x[0])
            # need dbl brackets to unpack the single element set (which has 2 elements inside it)
            [timeToComplete, usedSolution] = completionResult
            if usedSolution:
                res.append(problem)
                count -= 1
            elif self.tracker[problem] < 10:
                # select problem if it's been completed less than 10 times
                res.append(problem)
                count -= 1
            elif completedDates[0] < dt.datetime.now() - dt.timedelta(days=self.redoInterval):
                # select problem if it hasn't been completed in the last 5 days
                res.append(problem)
                count -= 1
            elif timeToComplete < 120:
                # skip problem if most recently it's been completed in under 2 minutes
                # and other conditions don't apply
                pass
            else:
                remains.append(problem)
            if count == 0:
                break
        while count > 0 and remains:
            nxt = remains.pop()
            res.append(nxt)
            count -= 1
        random.shuffle(res)
        return res

    def hardestProblems(self, numProblems=3, timeWindow=15):
        """
        Returns the hardest problems based on completion times.

        Args:
            numProblems (int, optional): The number of hardest problems to return. Default is 3.
            timeWindow (int, optional): The number of days to consider for completion times. Default is 15.

        Returns:
            list: A list of the hardest problems with their completion times and solution status.
        """
        self.deserialize()
        problemTimes = []
        for prob, cDates in self.completionCalendar.items():
            for date, completion in cDates.items():
                [[time, usedSolution]] = completion
                if date > dt.datetime.now() - dt.timedelta(days=timeWindow):
                    res = [prob, time, usedSolution]
                    problemTimes.append(res)
        sortedProblems = sorted(problemTimes, key=lambda x: x[1], reverse=True)
        sortedProblems = [[x[0], self.timeFormatter(x[1]), x[2]] for x in sortedProblems]
        return sortedProblems[:numProblems]

    def bestTimes(self, problems=[]):
        """
        Returns the best completion times for the given problems.

        Args:
            problems (list, optional): A list of problems to consider. If not provided, all problems in the problem set are considered.

        Returns:
            list: A list of tuples containing the problem and its best completion time.
        """
        self.deserialize()
        if not problems:
            problems = self.problems
        res = []
        for problem in problems:
            times = []
            for cDates, completions in self.completionCalendar[problem].items():
                for time, _ in completions:
                    times.append(time)
            if times:
                fastest = min(times)
                res.append((problem, self.timeFormatter(fastest)))
        return res
    
    def avgTimes(self, problems=[]):
        """
        Returns the average completion times for the given problems across all completions.

        Args:
            problems (list, optional): A list of problems to consider. If not provided, all problems in the problem set are considered.

        Returns:
            list: A list of tuples containing the problem and its average completion time.
        """
        self.deserialize()
        if not problems:
            problems = self.problems
        res = []
        for problem in problems:
            times = []
            for cDates, completions in self.completionCalendar[problem].items():
                for time, _ in completions:
                    times.append(time)
            if times:
                # throw out outliers
                if len(times) > 2:
                    times.sort()
                    times = times[1:-1]
                avg = int(sum(times) / len(times))
                res.append((problem, self.timeFormatter(avg)))
            else:
                res.append((problem, "Not enough data yet"))
        return res
    
    def avgForDay(self, dateString):
        date = self.dateConverter(dateString)
        totals = []
        for problem in self.problems:
            if date in self.completionCalendar[problem]:
                completions = self.completionCalendar[problem][date]
                # if there are multiple results, get the average of all
                mean = int(sum([c[0] for c in completions]) / len(completions))
                totals.append(mean)
        if len(totals) > 4:
            # throw out outliers if there are enough vals
            totals = totals[1:-1]
        if len(totals) > 0:
            meanProblemTime = int(sum(totals) / len(totals))
            return self.timeFormatter(meanProblemTime)
        else:
            return "Not any completions on that day."

    def dailyAverageOverSpan(self, startDateString, endDateString):
        sDate = self.dateConverter(startDateString)
        eDate = self.dateConverter(endDateString)
        if sDate >= eDate:
            raise ValueError("Start date must be before end date")
        dateList = []
        cDate = sDate
        while cDate < eDate:
            dateList.append(cDate)
            cDate += dt.timedelta(days=1)
        avgs = {}
        for day in dateList:
            dayString = day.strftime("%m-%d-%y")
            dailyMean = self.avgForDay(dayString)
            if dailyMean == "Not any completions on that day.":
                continue
            avgs[dayString] = dailyMean
        return avgs


if __name__ == "__main__":
    ps = ProblemSet(picklePath="problemLogs/problemSetLog.pickle")
    #ps.completeProblem(1, "10:00", "05-08-24", True)
    


    # add new problem next time! 


    #print(ps)
    # each day gen the problem list, then add results to the completionCalendar
    print(ps.genProblemList(numProblems=6, include=[105, 11], exclude=[1]))
    #print(ps.hardestProblems(numProblems=5))
    #print(ps.bestTimes())
    #print(ps.avgTimes())
    #pprint.pprint(ps.dailyAverageOverSpan("04-01-24", "05-24-24"))
    
