class Student:
    def __init__(self, name:str, marks:list[float]):
        self.name=name
        self.marks=marks
    
    def is_passed(self)->bool: return self.avg()>50.0
    def avg(self)->float: return sum(self.marks)/len(self.marks)


if __name__ == "__main__":
    student_pass = Student('Maciej', [60,51,80,30])
    student_fail = Student('Karol', [30,80,40])

    print(f"{student_pass.is_passed()}\t({student_pass.avg()})") #True    (55.25)
    print(f"{student_fail.is_passed()}\t({student_fail.avg()})") #False   (50.0)