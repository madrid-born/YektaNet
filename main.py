Jobs = []
Users = []
Skills = []


def Error(number):
    Errors = ['invalid name',          # 0
              'invalid age interval',  # 1
              'invalid timetype',      # 2
              'invalid salary',        # 3
              'invalid index',         # 4
              'invalid skill',         # 5
              'repeated skill',        # 6
              ]
    print(Errors[number])


class Skill:
    def __init__(self, name):
        self.name = name
        self.view = 0

    def addView(self):
        self.view += 1


def SkillList(list):
    array = []
    for skill in list:
        array.append(skill.name)
    return array


def showList(list):
    def sorting_key(skill):
        return -skill.view, skill.name

    sorted_list = sorted(list, key=sorting_key)
    for skill in sorted_list:
        print(f"({skill.name},{skill.view})", end="")
    print()


class Job:
    def __init__(self, name, minAge, maxAge, condition, salary):
        self.name = name
        self.minAge = minAge
        self.maxAge = maxAge
        self.condition = condition
        self.salary = salary
        self.view = 0
        self.skills = []

    def checkJob(self):
        if not self.name.isalpha():
            Error(0)
            return False
        elif self.minAge > self.maxAge or self.minAge > 200 or self.minAge < 0 or self.maxAge > 200 or self.maxAge < 0:
            Error(1)
            return False
        elif self.condition not in ['FULLTIME', 'PARTTIME', 'PROJECT']:
            Error(2)
            return False
        elif self.salary >= 1000000000 or self.salary < 0 or self.salary % 1000 >= 1:
            Error(3)
            return False
        else:
            return True

    def addSkill(self, skill):
        if skill in SkillList(self.skills):
            Error(6)
            return
        self.skills.append(Skill(skill))
        print("skill added")

    def addView(self):
        self.view += 1

    def show(self):
        print(f"{self.name}-{self.view}-", end='')
        showList(self.skills)


class User:
    def __init__(self, name, age, condition, salary):
        self.name = name
        self.age = age
        self.condition = condition
        self.salary = salary
        self.skills = []
        self.JobList = []

    def checkUser(self):
        if not self.name.isalpha():
            Error(0)
            return False
        elif self.age > 200 or self.age < 0:
            Error(1)
            return False
        elif self.condition not in ['FULLTIME', 'PARTTIME', 'PROJECT']:
            Error(2)
            return False
        elif self.salary >= 1000000000 or self.salary < 0 or self.salary % 1000 >= 1:
            Error(3)
            return False
        else:
            return True

    def addSkill(self, skill):
        if skill in SkillList(self.skills):
            Error(6)
            return
        self.skills.append(Skill(skill))
        print("skill added")

    def show(self):
        print(f"{self.name}-", end='')
        showList(self.skills)

    def calculateScore(self):
        self.jobList = []
        for i in range(len(Jobs)):
            job = Jobs[i]
            score = 0

            if self.age > job.maxAge:
                score += job.maxAge - self.age
            elif self.age < job.minAge:
                score += self.age - job.minAge
            else:
                score += min(self.age - job.minAge, job.maxAge - self.age)

            userSkills = SkillList(self.skills)
            jobSkills = SkillList(job.skills)
            score += (3 * len(set(userSkills).intersection(jobSkills))) - len(set(jobSkills).difference(userSkills))

            if job.condition == self.condition:
                score += 10
            elif self.condition == 'PARTTIME' or job.condition == 'PARTTIME':
                score += 5
            else:
                score += 4

            score += int(1000 / max(abs(self.salary - job.salary), 1))

            self.jobList.append((i+1, (score * 1000) + i + 1))


def AddJob(name, minAge, maxAge, condition, salary):
    job = Job(name, int(minAge), int(maxAge), condition, int(salary))
    if job.checkJob():
        Jobs.append(job)
        print(f"job id is {len(Jobs)}")


def AddUser(name, age, condition, salary):
    user = User(name, int(age), condition, int(salary))
    if user.checkUser():
        Users.append(user)
        print(f"user id is {len(Users)}")


def AddJobSKill(jobId, skill):
    jobId = int(jobId)
    if len(Jobs) < jobId or jobId <= 0:
        Error(4)
        return
    elif skill not in Skills:
        Error(5)
        return
    job = Jobs[jobId-1]
    job.addSkill(skill)


def AddUserSKill(userId, skill):
    userId = int(userId)
    if len(Users) < userId or userId <= 0:
        Error(4)
        return
    elif skill not in Skills:
        Error(5)
        return
    user = Users[userId-1]
    user.addSkill(skill)


def View(userId, jobId):
    userId = int(userId)
    jobId = int(jobId)
    if len(Jobs) < jobId or jobId <= 0 or len(Users) < userId or userId <= 0:
        Error(4)
        return
    user = Users[userId - 1]
    job = Jobs[jobId - 1]
    for userSkill in user.skills:
        list = SkillList(job.skills)
        if userSkill.name in list:
            userSkill.addView()
            job.skills[list.index(userSkill.name)].addView()
    job.addView()
    print(f"tracked")


def JobStatus(jobId):
    jobId = int(jobId)
    if len(Jobs) < jobId or jobId <= 0:
        Error(4)
        return
    job = Jobs[jobId - 1]
    job.show()
    pass


def UseerStatus(userId):
    userId = int(userId)
    if len(Users) < userId or userId <= 0:
        Error(4)
        return
    user = Users[userId - 1]
    user.show()
    pass


def GetJobList(userId):
    userId = int(userId)
    if len(Users) < userId or userId <= 0:
        Error(4)
        return
    user = Users[userId - 1]
    user.calculateScore()
    jobList = sorted(user.jobList, key=lambda x: -x[1])
    for item in jobList:
        print(item, end='')
    print()


def Command(command):
    if command[0] == 'ADD-JOB':
        AddJob(command[1], command[2], command[3], command[4], command[5])
    elif command[0] == 'ADD-USER':
        AddUser(command[1], command[2], command[3], command[4])
    elif command[0] == 'ADD-JOB-SKILL':
        AddJobSKill(command[1], command[2])
    elif command[0] == 'ADD-USER-SKILL':
        AddUserSKill(command[1], command[2])
    elif command[0] == 'VIEW':
        View(command[1], command[2])
    elif command[0] == 'JOB-STATUS':
        JobStatus(command[1])
    elif command[0] == 'USER-STATUS':
        UseerStatus(command[1])
    elif command[0] == 'GET-JOBLIST':
        GetJobList(command[1])


if __name__ == "__main__":
    input()
    line = input()
    for item in line.split(' '):
        Skills.append(item)
    n = int(input())
    for i in range(n):
        Command(input().split(' '))
    print("DONE")
