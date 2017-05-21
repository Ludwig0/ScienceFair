# This is Jeff's better version

import sys
import random


class Question:
    def __init__(self, question, answer_index, possible_answers):
        self.question = question
        self.answer_index = answer_index
        self.possible_answers = possible_answers


class QuestionSet:
    def __init__(self):
        self.question_list = []
        self.current_index = 0

    def parse_file(self, file_name):
        try:
            file = open(file_name)
            for line in file:
                parts = line.split("|")
                answers = parts[2].split("\\")
                answers[len(answers)-1] = answers[len(answers)-1].rstrip()
                self.question_list.append(Question(parts[0], int(parts[1]), answers))
            file.close()
        except FileNotFoundError as file_error:
            print(sys.exc_info()[0])

    def get_next_question(self):
        self.current_index = random.randint(0, len(self.question_list)) - 1
        if not self.has_next_question():
            return
        return self.question_list.pop(self.current_index)

    def has_next_question(self):
        return len(self.question_list) > 0
