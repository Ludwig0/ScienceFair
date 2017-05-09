#This one's for you, Brett <3
#Format of test files: QUESTION|ANSWER

#imports for random functions
import random
#import to find the path to the questions.txt file
import os

class question_set(object):
    def __init__(self):
        # init function
        self.questions = []
        self.answers = []
        self.used_questions = set()

    def construct(self):
        #Try to find the questions.txt file and set as path
        try:
            question_file = os.path.abspath("questions.txt")
        #If no question file, throws an exception
        except:
            print("No question file exists!")

        #Open the file
        file = open("questions.txt", "r")
        for line in file:
            #Splits file into question and answer
            line = line.split("|")
            #Adds questions into one list, answers into another
            self.questions.append(str(line[0]))
            self.answers.append(line[1])

    def getQuestion(self, number):
        #Fetches question and corresponding answers from both lists
        question = self.questions[number]
        answer = self.answers[number]
        #Adds the fetched question into the used_questions list
        #WARNING: MAY BE BUGGY, NEEDS TO BE CHECKED OUT
        self.used_questions.add(number)
        return question, answer

    def getNewQuestion(self):
        #If we have used all questions, returns -1
        if list(self.used_questions) == list(range(0, len(questions))):
            return -1
        else:
            #Gets list of ununsed questions using a list comprehension
            unused_questions = [number for number in range(0, len(self.questions)) if number not in self.used_questions]
            #Randomly picks a question number and returns it
            question_number = random.choice(unused_questions)
            return question_number