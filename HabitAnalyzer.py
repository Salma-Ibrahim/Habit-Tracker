from abc import ABC, abstractmethod
from datetime import timedelta, date



#HabitRecord class
class HabitRecord:
    def __init__(self, date, done):
        self.date = date 
        self.done = done

    def is_done(self):
        return self.done

#==================================================================================

#Habit class(Abstract Class)
class Habit(ABC):
    def __init__(self, name):
        self.name = name
        self.records = []

    
    def add_record(self, record):
        #Check if there's a record with the same date
        for i in range(len(self.records)):
            if self.records[i].date == record.date:
                #Overwrite the date
                self.records[i] = record


            
                return
            
        #append new record if there isn't a record with the same date
        self.records.append(record)

    @abstractmethod
    def get_streak(self):
        pass

    def success_rate(self):
        #Success rate = (Done days / Total days)*100


        #Check if records list is empty
        if len(self.records) == 0:
            return 0
        
        #Count done days
        done_days = 0
        for record in self.records:
            if record.is_done():
                done_days += 1

        success_rate = (done_days / len(self.records))*100
        return success_rate
    


#======================================================================

# DailyHabit class
class DailyHabit(Habit):
    def get_streak(self):
        #check if records list is empty
        if len(self.records) == 0:
            return 0
        
        #Sort recoreds by date
        sorted_records = sorted(self.records, key = lambda r: r.date)

        streak = 0
        last_date = None

        #iterate backward start from latest day

        for record in reversed(sorted_records):
            #if records list is empty and no records are done
            if not record.is_done():
                break

            #if records list is empty and the first record is done
            if last_date is None:
                streak = 1
            
            #Records list isn't empty so we check streak condition
            else:
                if last_date - record.date == timedelta(days=1):
                    streak += 1
                #Streak condition isn't satisfied
                else:
                    break
            #updata last_date
            last_date = record.date

        return streak
    

    
#================================================================
    

#HabitAnalyzer class
class HabitAnalyzer:
    def __init__(self, habits):
        self.habits = habits

    def best_habit(self):
        #check if habits are empty
        if not self.habits:
            return None
        
        best = self.habits[0]
        for habit in self.habits[1:]:
            #finding the maximum success rate
            if habit.success_rate() > best.success_rate():
                best = habit

        return best
    
    def worst_habit(self):
        if not self.habits:
            return None
        
        worst = self.habits[0]
        for habit in self.habits[1:]:
            if habit.success_rate() < worst.success_rate():
                worst = habit
        return worst
    
    def highest_commitment_days(self):
        #dictionary 
        #keys -> days & values -> No of habits done in this day
        commitment = {}

        #loop on habits
        for habit in self.habits:
            #loop on records of each habits
            for record in habit.records:
                #selecting days with done status
                if record.is_done():
                    #if this day doesn't have records in the dict add a value for it
                    if record.date not in commitment:
                        commitment[record.date] = 1
                    #if it already has records increment them by 1 
                    else:
                        commitment[record.date] += 1

        return commitment
    
#======================================================================

def main():
    #Defining Habits
    habit1 = DailyHabit("Drinking Water")
    habit2 = DailyHabit("Reading")
    habit3 = DailyHabit("Work out")
    #Defining Records and adding them
    habit1record1 = HabitRecord(date(2026,2,5), True) 
    habit1record2 = HabitRecord(date(2026,2,4), False) 
    habit1record3 = HabitRecord(date(2026,2,3), True) 
    habit1record4 = HabitRecord(date(2026,2,2), True) 
    habit1record5 = HabitRecord(date(2026,2,1), True) 

    habit1.add_record(habit1record1)
    habit1.add_record(habit1record2)
    habit1.add_record(habit1record3)
    habit1.add_record(habit1record4)
    habit1.add_record(habit1record5)

    habit2record1 = HabitRecord(date(2026,2,5), False)
    habit2record2 = HabitRecord(date(2026,2,4), True)
    habit2record3 = HabitRecord(date(2026,2,3), True)
    habit2record4 = HabitRecord(date(2026,2,2), False)
    habit2record5 = HabitRecord(date(2026,2,1), True)

    habit2.add_record(habit2record1)
    habit2.add_record(habit2record2)
    habit2.add_record(habit2record3)
    habit2.add_record(habit2record4)
    habit2.add_record(habit2record5)

    habit3.add_record(HabitRecord(date(2026,2,5), True))
    habit3.add_record(HabitRecord(date(2026,2,4), False))
    habit3.add_record(HabitRecord(date(2026,2,3), True))
    habit3.add_record(HabitRecord(date(2026,2,2), False))
    habit3.add_record(HabitRecord(date(2026,2,1), True))

    # Defining the analyzer
    analyzer = HabitAnalyzer([habit1, habit2, habit3])

    for habit in analyzer.habits:
        print("Habit", habit.name)
        print("Success rate", habit.success_rate(), "%")
        print("Current Streak", habit.get_streak())

    
    best = analyzer.best_habit()
    worst = analyzer.worst_habit()

    print("Best Habit:", best.name if best else "None")
    print("Worst Habit:", worst.name if best else "None")

    
    commitment = analyzer.highest_commitment_days()
    print(f"Highest commitment days: {commitment}")


if __name__ == "__main__":
    main()





