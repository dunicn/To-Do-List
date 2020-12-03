from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def user_menu():
    while True:
        print()
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        user_input = int(input())
        print()

        if user_input == 1:
            #  today's_tasks
            today = datetime.today()
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            if rows:
                print_tasks(rows)
            else:
                print("Today {} {}".format(today.day, today.strftime("%b")))
                print("Nothing to do!")
        elif user_input == 2:  # Show tasks for the next 7 days
            today = datetime.today()
            for x in range(0, 7):
                curr_day = today.date() + timedelta(x)
                rows = session.query(Table).filter(Table.deadline == curr_day).order_by(Table.deadline).all()
                if rows:
                    print_tasks(rows)
                elif not rows:
                    print()
                    print("{} {} {}:".format(weekday_method(curr_day.weekday()), curr_day.day, curr_day.strftime("%b")))
                    print("Nothing to do!")
        elif user_input == 3:  # Show all tasks
            rows = session.query(Table).order_by(Table.id).all()
            if not rows:
                print("Nothing to do!")
            else:
                print("All tasks:")
                print_all_tasks(rows)
        elif user_input == 4:  # Show missed tasks
            rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
            print("Missed tasks:")
            if not rows:
                print("Nothing is missed!")
            else:
                for row in rows:
                    print("{}. {}. {} {}".format(row.id, row.task, row.deadline.day, row.deadline.strftime("%b")))
        elif user_input == 5:  # Add task
            #  add_task
            users_task = str(input("Enter task: "))
            users_deadline = input("Enter deadline: ")
            users_deadline_date = datetime.strptime(users_deadline, "%Y-%m-%d").date()
            new_row = Table(task=users_task, deadline=users_deadline_date)
            session.add(new_row)
            session.commit()
            print("The task has been added!")
        elif user_input == 6:
            rows = session.query(Table).order_by(Table.deadline).all()
            if not rows:
                print("Nothing to delete!")
            else:
                print("Choose the number of the task you want to delete:")
                print_all_tasks(rows)
                chosen_task = int(input())
                for row in rows:
                    if row.id == chosen_task:
                        session.delete(row)
                        session.commit()
                        print("The task has been deleted!")

        elif user_input == 0:
            print("Bye!")
            exit()


def print_all_tasks(rows):
    for row in rows:
        print("{}. {}. {} {}".format(row.id, row.task, row.deadline.day, row.deadline.strftime("%b")))


def print_tasks(rows):
    today = datetime.today()
    if rows:
        count = 1
        for task in rows:
            if task:
                if task.deadline == today.date():
                    if count == 1:
                        print("{} {} {}:".format(weekday_method(task.deadline.weekday()), task.deadline.day,
                                                 task.deadline.strftime("%b")))
                        # print("Today {} {}:".format(task.deadline.day, task.deadline.strftime("%b")))
                    print('{}. {}'.format(count, task, task))
                    count += 1
                else:
                    if count == 1:
                        print()
                        print("{} {} {}:".format(weekday_method(task.deadline.weekday()), task.deadline.day,
                                                 task.deadline.strftime("%b")))
                    print("{}. {}".format(count, task))

                    count += 1
            else:
                print("{} {} {}:".format(weekday_method(task.deadline.weekday()), task.deadline.day,
                                         task.deadline.strftime("%b")))
                print("Nothing to do!")


def weekday_method(number):
    if number == 0:
        return "Monday"
    elif number == 1:
        return "Tuesday"
    elif number == 2:
        return "Wednesday"
    elif number == 3:
        return "Thursday"
    elif number == 4:
        return "Friday"
    elif number == 5:
        return "Saturday"
    elif number == 6:
        return "Sunday"


user_menu()
