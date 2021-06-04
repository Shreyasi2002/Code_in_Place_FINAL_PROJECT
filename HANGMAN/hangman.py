import random
import tkinter as tkk
from tkinter import *
import pyttsx3
import string
from playsound import playsound

WORDLIST_FILENAME = "words.txt"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 160)


class Hangman:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Game")
        master.geometry("500x500")

        self.wordlist = self.load_words()
        self.secret_word = self.choose_word()

        self.letter = list()
        self.guess = None
        self.guesses_left = 6
        self.warnings_left = 3
        

        self.message = "Welcome to the game Hangman! \n" + "I am thinking of a word that is " + str(
            len(self.secret_word)) + " letters long. "

        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(master, textvariable=self.label_text)


        vcmd = master.register(self.validate)
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.entry.place(height=150)
        self.guess_button = Button(master, text="Guess", command=self.hangman, height=2, width=7)
        self.guess_button.bind("<Return>", self.hangman)
        self.hints_button = Button(master, text="Hints", command=self.give_hints, height=2, width=7)
        self.fun_button = Button(master, text="Make me Laugh", command=self.laugh, height=2, width=7)
        self.reset_button = Button(master, text="Play again", command=self.reset, state=DISABLED, height=2, width=7)

        self.label.grid(row=0, column=0, columnspan=6, sticky=W + E)
        self.entry.grid(row=1, column=0, columnspan=6, sticky=W + E, ipadx=100, ipady=5)
        self.guess_button.grid(row=2, column=0)
        self.reset_button.grid(row=4, column=2)
        self.hints_button.grid(row=2, column=2)
        self.fun_button.grid(row=4, column=0)

        engine.say("Welcome to the game Hangman! ")
        engine.runAndWait()
        engine.say("I am thinking of a word that is " + str(len(self.secret_word)) + " letters long.")
        engine.runAndWait()
        engine.say("You have 3 warnings left.")
        engine.runAndWait()

        engine.say("You have " + str(self.guesses_left) + " guesses left")
        engine.runAndWait()
        engine.say("Please guess a letter: ")
        engine.runAndWait()

    def give_hints(self):
        engine.say("Okay I am giving you little hints ")
        engine.runAndWait()
        self.show_possible_matches(self.get_guessed_word(self.letter))

    def laugh(self):
        playsound("Maniacal Witches Laugh-SoundBible.com-262127569.mp3")
        playsound("hahaha-Peter_De_Lang-1639076107.mp3")

    def validate(self, new_text):
        if not new_text:
            self.guess = None
            return True

        try:
            guess = new_text
            if not str.isdigit(guess):
                self.guess = guess
                return True
            else:
                return False
        except ValueError:
            return False

    def reset(self):
        self.entry.delete(0, END)
        self.secret_word = self.choose_word()
        self.guess = None
        self.guesses_left = 6

        self.message = "Welcome to the game Hangman! \n" + "I am thinking of a word that is " + str(
            len(self.secret_word)) + " letters long."
        self.label_text.set(self.message)

        self.guess_button.configure(state=NORMAL)
        self.reset_button.configure(state=DISABLED)

    def load_words(self):
        """

        Returns a list of valid words. Words are strings of lowercase letters.

        Depending on the size of the word list, this function may
        take a while to finish.

        """
        tkk.Label(self.master, text="Loading word list from file...").grid(columnspan=4, sticky=W + E)
        # inFile: file
        inFile = open(WORDLIST_FILENAME, 'r')
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        self.wordlist = line.split()
        tkk.Label(self.master, text="  "+ str(len(self.wordlist))+ "words loaded.").grid(columnspan=3, sticky=W + E)
        return self.wordlist

    def choose_word(self):
        """
        wordlist (list): list of words (strings)
        
        Returns a word from wordlist at random
        """
        return random.choice(self.wordlist)

    # end of helper code

    # -----------------------------------

    # Load the list of words into the variable wordlist
    # so that it can be accessed from anywhere in the program

    def is_word_guessed(self, letters_guessed):

        """
        secret_word: string, the word the user is guessing; assumes all letters are
          lowercase
        letters_guessed: list (of letters), which letters have been guessed so far;
          assumes that all letters are lowercase
        returns: boolean, True if all the letters of secret_word are in letters_guessed;
          False otherwise
        """
        for i in range(len(self.secret_word)):
            if self.secret_word[i] not in letters_guessed:
                return False
        return True

    def get_index_positions(self, list_of_elems, element):
        """ Returns the indexes of all occurrences of give element in
        the list- listOfElements """
        index_pos_list = []
        index_pos = 0
        while True:
            try:
                # Search for item in list from indexPos to the end of list
                index_pos = list_of_elems.index(element, index_pos)
                # Add the index position in list
                index_pos_list.append(index_pos)
                index_pos += 1
            except ValueError as e:
                break
        return index_pos_list

    def get_guessed_word(self, letters_guessed):
        """
        secret_word: string, the word the user is guessing
        letters_guessed: list (of letters), which letters have been guessed so far
        returns: string, comprised of letters, underscores (_), and spaces that represents
          which letters in secret_word have been guessed so far.
        """
        result = list()
        for i in range(len(self.secret_word)):
            result.append("_ ")
        for c in letters_guessed:
            if c in self.secret_word:
                i = self.get_index_positions(self.secret_word, c)
                for j in range(len(i)):
                    result[i[j]] = c
        result1 = ""
        for ele in result:
            result1 += ele

        return result1

    def get_available_letters(self, letters_guessed):
        """
        letters_guessed: list (of letters), which letters have been guessed so far
        returns: string (of letters), comprised of letters that represents which letters have not
          yet been guessed.
        """
        result = string.ascii_lowercase
        for c in letters_guessed:
            result = result.replace(c, '')

        return result

    def match_with_gaps(self, my_word, other_word):
        """
        my_word: string with _ characters, current guess of secret word
        other_word: string, regular English word
        returns: boolean, True if all the actual letters of my_word match the 
            corresponding letters of other_word, or the letter is the special symbol
            _ , and my_word and other_word are of the same length;
            False otherwise: 
        """
        s = my_word
        for x in range(len(my_word)):
            if my_word[x] == ' ':
                s = s.replace(' ', '')

        if len(s) != len(other_word):
            return False
        else:
            for c in s:
                if c != '_':
                    i = self.get_index_positions(s, c)
                    j = self.get_index_positions(other_word, c)
                    if len(i) != len(j):
                        return False
                    else:
                        for a in range(len(i)):
                            if i[a] != j[a]:
                                return False

        return True

    def show_possible_matches(self, my_word):
        """
        my_word: string with _ characters, current guess of secret word
        returns: nothing, but should print out every word in wordlist that matches my_word
                 Keep in mind that in hangman when a letter is guessed, all the positions
                 at which that letter occurs in the secret word are revealed.
                 Therefore, the hidden letter(_ ) cannot be one of the letters in the word
                 that has already been revealed.

        """
        result = ""
        for i in range(len(self.wordlist)):
            if self.match_with_gaps(my_word, self.wordlist[i]):
                result += (self.wordlist[i] + " ")

        if len(result) == 0:
            tkk.Label(self.master, text="No Matches Found").grid(columnspan=3, sticky=W + E)
        else:
            tkk.Label(self.master,text="Possible word matches are: ").grid(columnspan=3, sticky=W + E)
            tkk.Label(self.master, text=result).grid(columnspan=4, sticky=W + E)

    def hangman(self):
        """
        secret_word: string, the secret word to guess.
        
        Starts up an interactive game of Hangman.
        
        * At the start of the game, let the user know how many 
          letters the secret_word contains and how many guesses s/he starts with.
          
        * The user should start with 6 guesses
        
        * Before each round, you should display to the user how many guesses
          s/he has left and the letters that the user has not yet guessed.
        
        * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
          
        * The user should receive feedback immediately after each guess 
          about whether their guess appears in the computer's word.

        * After each guess, you should display to the user the 
          partially guessed word so far.
          
        * If the guess is the symbol *, print out all words in wordlist that
          matches the current guessed word. 
        
        Follows the other limitations detailed in the problem write-up.
        """

        tkk.Label(self.master, text="You have 3 warnings left.").grid(columnspan=3, sticky=W + E)

        unique = len(set(self.secret_word))
        tkk.Label(self.master, text="-----------------").grid(columnspan=6, sticky=W + E)
        #engine.say("You have " + str(self.guesses_left) + " guesses left")
        #engine.runAndWait()
        #engine.say("Please guess a letter: ")
        #engine.runAndWait()
        tkk.Label(self.master, text="You have " + str(self.guesses_left) + " guesses left").grid(columnspan=3,
                                                                                                    sticky=W + E)
        tkk.Label(self.master, text="Available letters: " + self.get_available_letters(self.letter)).grid(
            columnspan=3, sticky=W + E)
        tkk.Label(self.master, text="Please guess a letter: ").grid(columnspan=3, sticky=W + E)

        if self.guess is None:
            self.message = "Please guess a letter ;)"
            engine.say("Please guess a letter")
            engine.runAndWait()

        elif self.guess in self.letter:
            if self.warnings_left > 0:
                engine.say("Oops! You've already guessed that letter. ")
                engine.runAndWait()
                playsound("Sad_Trombone-Joe_Lamb-665429450.mp3")
                engine.say("You have " + str(self.warnings_left - 1) + " warnings left: ")
                engine.runAndWait()
                tkk.Label(self.master, text="Oops! You've already guessed that letter. You have " + str(self.warnings_left - 1) + " warnings left: " + self.get_guessed_word(self.letter)).grid(columnspan=3, sticky=W + E)

                self.warnings_left -= 1
            else:
                engine.say("Oops! You've already guessed that letter.")
                engine.runAndWait()
                playsound("Sad_Trombone-Joe_Lamb-665429450.mp3")
                engine.say(" You have no warnings left so you lose one guess: ")
                engine.runAndWait()
                tkk.Label(self.master,text="Oops! You've already guessed that letter. You have no warnings left so you lose one guess: " + self.get_guessed_word(self.letter)) .grid(columnspan=3, sticky=W + E)

                self.guesses_left -= 1

        else:
            if str.isalpha(self.guess):
                a = str.lower(self.guess)
                self.letter.append(a)
                if a in self.secret_word:
                    engine.say("Good guess  ")
                    engine.runAndWait()
                    playsound("1_person_cheering-Jett_Rifkin-1851518140.mp3")
                    tkk.Label(self.master,text="Good guess: " + self.get_guessed_word(self.letter)).grid(columnspan=4, sticky=W + E)

                else:
                    engine.say("Oops! That letter is not in my word: ")
                    engine.runAndWait()
                    playsound("Sad_Trombone-Joe_Lamb-665429450.mp3")
                    tkk.Label(self.master,text="Oops! That letter is not in my word: " + self.get_guessed_word(self.letter)) .grid(columnspan=3, sticky=W + E)
                    self.guesses_left -= 1

            else:
                if self.warnings_left > 0:
                    engine.say("Oops! That is not a valid letter. ")
                    engine.runAndWait()
                    playsound("Sad_Trombone-Joe_Lamb-665429450.mp3")
                    engine.say("You have " + str(self.warnings_left - 1) + " warnings left: ")
                    engine.runAndWait()
                    tkk.Label(self.master, text="Oops! That is not a valid letter. You have " + str(self.warnings_left - 1) + " warnings left: " + self.get_guessed_word(self.letter)).grid(columnspan=3, sticky=W + E)
                    self.warnings_left -= 1
                else:
                    engine.say("Oops! That is not a valid letter. ")
                    engine.runAndWait()
                    playsound("Sad_Trombone-Joe_Lamb-665429450.mp3")
                    engine.say("You have no warnings left so you lose one guess: ")
                    engine.runAndWait()
                    tkk.Label(self.master,text="Oops! That is not a valid letter. \nYou have no warnings left so you lose one guess: "+ self.get_guessed_word(self.letter)).grid(columnspan=3, sticky=W + E)
                    self.guesses_left -= 1

        if self.is_word_guessed(self.letter):
            engine.say("Congratulations, you won! Your total score for this game is: " + str(self.guesses_left * unique))
            engine.runAndWait()
            tkk.Label(self.master, text="-----------------").grid(columnspan=6, sticky=W + E)
            self.message = "Congratulations, you won!"
            tkk.Label(self.master, text="CONGRATULATIONS YOU WON!!!🥳🥳🥳").grid(columnspan=10, sticky=W + E)
            self.guess_button.configure(state=DISABLED)
            self.reset_button.configure(state=NORMAL)
            tkk.Label(self.master, text="Your total score for this game is: " + str(self.guesses_left * unique)).grid(columnspan=10, sticky=W + E)
            playsound("SMALL_CROWD_APPLAUSE-Yannick_Lemieux-1268806408.mp3")

        if self.guesses_left <= 0:
            engine.say("Sorry, you ran out of guesses. ")
            engine.runAndWait()
            engine.say("The word was " + self.secret_word)
            engine.runAndWait()
            engine.say("Better luck next time !")
            engine.runAndWait()
            self.message = "Sorry! You failed... Better luck next time"
            self.guess_button.configure(state=DISABLED)
            self.reset_button.configure(state=NORMAL)
            tkk.Label(self.master, text="-----------------").grid(columnspan=6, sticky=W + E)
            tkk.Label(self.master, text="Sorry, you ran out of guesses. The word was " + self.secret_word).grid(columnspan=4, sticky=W + E)

        self.label_text.set(self.message)
        engine.say("You have " + str(self.guesses_left) + " guesses left")
        engine.runAndWait()
        engine.say("Please guess a letter: ")
        engine.runAndWait()


root = Tk()
my_gui = Hangman(root)
root.mainloop()
