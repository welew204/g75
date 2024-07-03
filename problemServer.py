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
    def __init__(self, problems):
        self.problems = problems
        self.tracker = defaultdict(int)
        self.completionCalendar = defaultdict(self.ddNester)
        self.redoInterval = 5
        self.serialize()

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

    def deserialize(self):
        """
        Should be used *before* any state-checking or -changing operation to ensure working w/ freshest data.
        """
        with open("problemLogs/problemSetLog.pickle", "rb") as incoming:
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
            for date, completions in cDates.items():
                for [time, usedSolution] in completions:
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
        while cDate <= eDate:
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
    ps = ProblemSet(currCoreProblems)
    ps.completeProblem(310, "4:30", "04-18-24")
    ps.completeProblem(310, "3:30", "04-23-24")
    ps.completeProblem(79, "5:00", "04-23-24")
    ps.completeProblem(310, "3:00", "04-24-24")
    ps.completeProblem(79, "4:40", "04-24-24")
    ps.completeProblem(621, "11:00", "04-24-24")
    ps.completeProblem(310, "5:30", "04-25-24")
    ps.completeProblem(79, "5:30", "04-25-24")
    ps.completeProblem(621, "10:00", "04-25-24")
    ps.completeProblem(310, "2:10", "04-26-24")
    ps.completeProblem(79, "4:00", "04-26-24")
    ps.completeProblem(621, "5:35", "04-26-24")
    ps.completeProblem(310, "2:55", "04-29-24")
    ps.completeProblem(79, "5:00", "04-29-24")
    ps.completeProblem(621, "7:30", "04-29-24")
    ps.completeProblem(310, "2:15", "04-30-24")
    ps.completeProblem(79, "3:15", "04-30-24")
    ps.completeProblem(621, "3:20", "04-30-24")
    ps.completeProblem(1, "2:10", "04-30-24")
    ps.completeProblem(310, "2:45", "05-01-24")
    ps.completeProblem(79, "3:15", "05-01-24")
    ps.completeProblem(621, "3:30", "05-01-24")
    ps.completeProblem(15, "5:45", "05-01-24")
    ps.completeProblem(79, "3:45", "05-02-24")
    ps.completeProblem(15, "3:45", "05-02-24")
    ps.completeProblem(310, "2:05", "05-02-24")
    ps.completeProblem(621, "2:50", "05-02-24")
    # added Coin Change problem today
    ps.completeProblem(79, "3:30", "05-07-24")
    ps.completeProblem(310, "2:25", "05-07-24")
    ps.completeProblem(15, "5:25", "05-07-24")
    ps.completeProblem(621, "5:31", "05-07-24")
    ps.completeProblem(322, "7:00", "05-07-24")
    ps.completeProblem(15, "5:45", "05-08-24")
    ps.completeProblem(310, "2:20", "05-08-24")
    ps.completeProblem(621, "7:09", "05-08-24")
    ps.completeProblem(1, "10:00", "05-08-24", True)
    ps.completeProblem(79, "3:45", "05-08-24")
    ps.completeProblem(322, "10:00", "05-08-24", True)
    ps.completeProblem(621, "2:30", "05-09-24")
    ps.completeProblem(322, "7:45", "05-09-24", True)
    ps.completeProblem(15, "15:00", "05-09-24", True)
    ps.completeProblem(79, "3:05", "05-09-24")
    ps.completeProblem(310, "3:00", "05-09-24")
    ps.completeProblem(1, "2:00", "05-09-24")
    ps.completeProblem(1, "1:10", "05-10-24")
    ps.completeProblem(621, "2:25", "05-10-24")
    ps.completeProblem(310, "2:45", "05-10-24")
    ps.completeProblem(322, "1:50", "05-10-24")
    ps.completeProblem(15, "2:20", "05-10-24")
    ps.completeProblem(79, "3:10", "05-10-24")
    ps.completeProblem(1, "1:20", "05-13-24")
    ps.completeProblem(310, "2:10", "05-13-24")
    ps.completeProblem(79, "3:15", "05-13-24")
    ps.completeProblem(15, "2:10", "05-13-24")
    ps.completeProblem(322, "2:00", "05-13-24")
    ps.completeProblem(621, "2:30", "05-13-24")
    # added pre/inorder traversal problem today
    ps.completeProblem(105, "15:00", "05-14-24", True)
    ps.completeProblem(15, "15:00", "05-14-24")
    ps.completeProblem(322, "1:55", "05-14-24")
    ps.completeProblem(105, "2:09", "05-14-24")
    ps.completeProblem(79, "2:50", "05-14-24")
    ps.completeProblem(1, "1:10", "05-14-24")
    ps.completeProblem(105, "4:20", "05-15-24")
    ps.completeProblem(310, "2:15", "05-15-24")
    ps.completeProblem(621, "2:50", "05-15-24")
    ps.completeProblem(322, "1:58", "05-15-24")
    ps.completeProblem(621, "2:10", "05-16-24")
    ps.completeProblem(15, "2:10", "05-16-24")
    ps.completeProblem(1, "0:48", "05-16-24")
    ps.completeProblem(105, "2:10", "05-16-24")
    ps.completeProblem(322, "1:25", "05-16-24")
    ps.completeProblem(105, "1:54", "05-17-24")
    ps.completeProblem(621, "4:00", "05-17-24")
    ps.completeProblem(15, "2:30", "05-17-24")
    ps.completeProblem(310, "2:30", "05-17-24")
    ps.completeProblem(79, "3:00", "05-17-24")
    # added water container problem today
    ps.completeProblem(105, "1:45", "05-20-24")
    ps.completeProblem(621, "3:00", "05-20-24")
    ps.completeProblem(322, "1:20", "05-20-24")
    ps.completeProblem(310, "2:13", "05-20-24")
    ps.completeProblem(79, "6:30", "05-20-24")
    ps.completeProblem(11, "15:00", "05-20-24", True)
    ps.completeProblem(79, "2:45", "05-21-24")
    ps.completeProblem(15, "2:15", "05-21-24")
    ps.completeProblem(11, "2:15", "05-21-24")
    ps.completeProblem(310, "1:55", "05-21-24")
    ps.completeProblem(105, "1:55", "05-21-24")
    ps.completeProblem(322, "1:40", "05-24-24")
    ps.completeProblem(79, "2:35", "05-24-24")
    ps.completeProblem(621, "3:10", "05-24-24")
    ps.completeProblem(105, "2:05", "05-24-24")
    ps.completeProblem(15, "2:52", "05-24-24")
    ps.completeProblem(11, "2:35", "05-24-24")
    ps.completeProblem(621, "5:00", "05-25-24")
    ps.completeProblem(11, "2:45", "05-25-24")
    ps.completeProblem(79, "3:26", "05-25-24")
    ps.completeProblem(105, "1:48", "05-25-24")
    ps.completeProblem(310, "2:24", "05-25-24")
    ps.completeProblem(322, "1:37", "05-25-24")
    # did look at solution, but also MOSTLY solved this new one on my own, first!
    ps.completeProblem(17, "15:00", "05-25-24", True)
    ps.completeProblem(310, "2:07", "05-26-24")
    ps.completeProblem(17, "2:37", "05-26-24")
    ps.completeProblem(105, "1:47", "05-26-24")
    ps.completeProblem(79, "2:36", "05-26-24")
    ps.completeProblem(11, "1:25", "05-26-24")
    ps.completeProblem(322, "1:29", "05-26-24")
    ps.completeProblem(53, "15:00", "05-26-24", True)
    ps.completeProblem(15, "2:08", "05-27-24")
    ps.completeProblem(17, "1:57", "05-27-24")
    ps.completeProblem(11, "1:15", "05-27-24")
    ps.completeProblem(53, "5:20", "05-27-24")
    ps.completeProblem(105, "1:46", "05-27-24")
    ps.completeProblem(621, "2:56", "05-27-24")
    ps.completeProblem(322, "2:05", "05-28-24")
    ps.completeProblem(105, "1:25", "05-28-24")
    ps.completeProblem(17, "1:25", "05-28-24")
    ps.completeProblem(11, "1:15", "05-28-24")
    ps.completeProblem(53, "1:20", "05-28-24")
    ps.completeProblem(310, "1:57", "05-28-24")
    ps.completeProblem(57, "20:00", "05-29-24", True)
    ps.completeProblem(105, "1:18", "05-29-24")
    ps.completeProblem(17, "1:26", "05-29-24")
    ps.completeProblem(621, "1:57", "05-29-24")
    ps.completeProblem(11, "1:16", "05-29-24")
    ps.completeProblem(53, "1:07", "05-29-24")
    ps.completeProblem(57, "2:18", "05-29-24")
    ps.completeProblem(57, "3:17", "05-30-24")
    ps.completeProblem(11, "0:59", "05-30-24")
    ps.completeProblem(15, "2:06", "05-30-24")
    ps.completeProblem(17, "1:26", "05-30-24")
    ps.completeProblem(310, "2:01", "05-30-24")
    ps.completeProblem(53, "0:49", "05-30-24")
    ps.completeProblem(542, "20:00", "05-30-24", True)
    ps.completeProblem(11, "1:06", "05-31-24")
    ps.completeProblem(105, "1:20", "05-31-24")
    ps.completeProblem(542, "16:59", "05-31-24", True)
    ps.completeProblem(57, "5:00", "05-31-24")
    ps.completeProblem(53, "0:59", "05-31-24")
    ps.completeProblem(15, "1:40", "05-31-24")
    ps.completeProblem(542, "6:59", "05-31-24")
    ps.completeProblem(57, "4:51", "06-03-24")
    ps.completeProblem(322, "2:23", "06-03-24")
    ps.completeProblem(53, "0:50", "06-03-24")
    ps.completeProblem(15, "1:58", "06-03-24")
    ps.completeProblem(17, "1:46", "06-03-24")
    ps.completeProblem(542, "15:00", "06-03-24", True)
    ps.completeProblem(542, "9:00", "06-06-24")
    ps.completeProblem(57, "5:05", "06-06-24")
    ps.completeProblem(53, "0:43", "06-06-24")
    ps.completeProblem(17, "1:43", "06-06-24")
    ps.completeProblem(11, "1:26", "06-06-24")
    ps.completeProblem(15, "2:59", "06-06-24")
    ps.completeProblem(542, "10:00", "06-17-24", True)
    ps.completeProblem(57, "4:42", "06-17-24")
    ps.completeProblem(17, "1:36", "06-18-24")
    ps.completeProblem(53, "0:43", "06-18-24")
    ps.completeProblem(105, "2:13", "06-18-24")
    ps.completeProblem(621, "5:35", "06-18-24")
    ps.completeProblem(973, "11:00", "06-18-24")
    ps.completeProblem(57, "3:35", "06-19-24")
    ps.completeProblem(17, "1:39", "06-19-24")
    ps.completeProblem(973, "3:29", "06-19-24")
    ps.completeProblem(53, "0:39", "06-19-24")
    ps.completeProblem(542, "8:40", "06-19-24")
    ps.completeProblem(105, "1:48", "06-19-24")
    ps.completeProblem(3, "10:00", "06-19-24")
    # 3: review other solutions to this tomorrow (mine implements 2 pointers)
    ps.completeProblem(105, "1:20", "06-20-24")
    ps.completeProblem(542, "4:30", "06-20-24")
    ps.completeProblem(3, "2:28", "06-20-24")
    ps.completeProblem(17, "1:42", "06-20-24")
    ps.completeProblem(57, "2:48", "06-20-24")
    ps.completeProblem(973, "1:43", "06-20-24")
    ps.completeProblem(15, "3:15", "06-20-24")
    ps.completeProblem(310, "6:29", "06-21-24")
    ps.completeProblem(542, "4:06", "06-21-24")
    ps.completeProblem(3, "7:59", "06-21-24")
    ps.completeProblem(621, "5:04", "06-21-24")
    ps.completeProblem(973, "1:34", "06-21-24")
    ps.completeProblem(17, "1:56", "06-21-24")
    ps.completeProblem(57, "2:31", "06-21-24")
    ps.completeProblem(973, "1:28", "06-25-24")
    ps.completeProblem(3, "4:06", "06-25-24")
    ps.completeProblem(53, "0:38", "06-25-24")
    ps.completeProblem(105, "1:40", "06-25-24")
    # checkout other solve for 105??
    ps.completeProblem(79, "15:00", "06-25-24", True)
    ps.completeProblem(542, "6:30", "06-25-24")
    ps.completeProblem(57, "2:53", "06-25-24")
    ps.completeProblem(973, "1:16", "06-26-24")
    ps.completeProblem(542, "3:53", "06-26-24")
    ps.completeProblem(79, "3:49", "06-26-24")
    ps.completeProblem(310, "3:36", "06-26-24")
    ps.completeProblem(57, "2:07", "06-26-24")
    ps.completeProblem(322, "12:30", "06-26-24")
    ps.completeProblem(3, "2:14", "06-26-24")
    ps.completeProblem(102, "21:06", "06-26-24")
    ps.completeProblem(133, "30:00", "06-27-24", True)
    ps.completeProblem(322, "2:45", "06-27-24")
    ps.completeProblem(310, "2:37", "06-27-24")
    ps.completeProblem(542, "5:54", "06-29-24")
    ps.completeProblem(15, "10:45", "06-29-24")
    ps.completeProblem(102, "14:00", "06-29-24", True)
    ps.completeProblem(79, "3:59", "06-29-24")
    ps.completeProblem(3, "3:36", "06-29-24")
    ps.completeProblem(133, "10:20", "06-29-24", True)
    ps.completeProblem(102, "5:26", "06-29-24")
    ps.completeProblem(133, "2:23", "06-29-24")
    ps.completeProblem(973, "1:30", "07-01-24")
    ps.completeProblem(102, "5:23", "07-01-24")
    ps.completeProblem(15, "3:06", "07-01-24")
    ps.completeProblem(79, "2:59", "07-01-24")
    ps.completeProblem(542, "4:19", "07-01-24")
    ps.completeProblem(3, "3:15", "07-01-24")
    ps.completeProblem(322, "3:18", "07-01-24")
    ps.completeProblem(133, "5:58", "07-01-24")
    ps.completeProblem(150, "4:28", "07-02-24")
    ps.completeProblem(3, "1:59", "07-02-24")
    ps.completeProblem(102, "3:49", "07-02-24")
    ps.completeProblem(133, "1:58", "07-02-24")
    ps.completeProblem(57, "3:23", "07-02-24")
    ps.completeProblem(621, "3:21", "07-02-24")
    ps.completeProblem(17, "2:24", "07-02-24")
    ps.completeProblem(542, "8:10", "07-02-24")


    #print(ps)
    # some kind of deeper assessment
    # each day gen the problem list, then add results to the completionCalendar
    print(ps.genProblemList(numProblems=7, include=[133, 102], exclude=[1, 53]))
    #print(ps.hardestProblems(numProblems=5))
    #print(ps.bestTimes())
    #print(ps.avgTimes())
    #pprint.pprint(ps.dailyAverageOverSpan("05-01-24", "06-06-24"))
    #print(ps.avgForDay("05-25-24"))
    #print({k: v for k, v in ps.tracker.items() if v < 10})
    
