"""
This is a stub for COMP16321 Coursework 01.
Do not edit or delete any lines given in this file that are marked with a "(s)".
(you can move them to different lines as long as you do not change the overall structure)

Place your code below the comments marked "#Your code here" and before the pass for that method.

Each method is documented to explain what work is to be placed within it.

NOTE: You can create as many more methods as you need. However, you need to add 
self as a parameter of the new method and  to call it with the prefix self.name 

"""

class Basics:#(s)

    def __init__(self):
        file_name = 'paragraph.txt'
        file = open(file_name, 'r')
        self.text = file.read()
        self.words = self.text.split()
        punct = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '{', '|', '}', '~', '`']

        file = open('dictionary.txt', 'r')
        dict_list = file.read().splitlines()

        offset = 0
        for i in range(len(self.words)):
            j = i - offset
            self.words[j] = ''.join([char for char in self.words[j] if char not in punct and not char.isnumeric()])
            self.words[j] = self.words[j].lower() 
            if self.words[j] not in dict_list:
                self.words.pop(j)
                offset += 1

    # ---Section 1 --- #

    #(Task 1.1)
    def read_file(self):#(s)
        """
            Read the contents of the text file paragraph.txt and return it as a single string.

            Returns: 
                str: The content of the text file as a single string
        """
        #Your code here

        file = open('paragraph.txt', 'r')
        self.text = file.read()
        
        return self.text

        pass#(s)


    # ---Section 2 --- #

    #(Task 2.1)
    def length_of_file(self, file_string):#(s)
        """
            Calculate the length of the text string from Task 1.1

            This method calculates the total number of characters in the provided text string,
            including letters, numbers, symbols, and whitespace, and returns the result as an integer.
        
            Parameters:
                file_string (str): The text string from Task 1.1

            Returns:
                int: The length of the text string, including all characters.
        """
        #Your code here

        return len(self.text)
    
        pass#(s)


    #(Task 2.2)
    def lower_case_count(self, file_string):#(s)
        """
            Calculate the total number of lower case letters (i.e. a-z) in the text string from Task 1.1

            This method calculates the total number of lower case letters in the provided text string and returns the result as an integer
        
            Parameters:
                file_string (str): The text string from Task 1.1

            Returns:
                int: The count of lower case letters.
        """
        #Your code here
        count = 0
        for char in self.text:
            if char.islower():
                count += 1
        return count
        pass#(s)

    #(Task 2.3)
    def upper_case_merge(self, file_string):#(s)
        """
            Find all upper case letters (i.e. A-Z) in the text string from task 1.1 and merge these into a single string

            This method finds all upper case letters and merges them into a singular string of upper case letters. E.g. "thIs Sentence OF a feW wordS" will return "ISOFWS"
        
            Parameters:
                file_string (str): The text string from Task 1.1

            Returns:
                str: The upper case letters as a single string
        """
        #Your code here
        upper = ''

        for char in self.text:
            if char.isupper():
                upper += char
        return upper
        pass#(s)

    #(Task 2.4)
    def digits_sum(self, file_string):#(s)
        """
            Sum all digits in the text string from task 1.1

            Find all digits in the text string and sum them together. Each digit must be treated as an individual digit. E.g. i.e. if there is a 1 then 23 then this will be treated as 1+2+3 and not 1+23 
        
            Parameters:
                file_string (str): The text string from Task 1.1

            Returns:
                int: The sum of all digits in the file
        """
        #Your code here
        count = 0

        for char in self.text:
            if char.isnumeric():
                count += int(char)
        return count
        pass#(s)

    # ---Section 3 --- #

    #(Task 3.1)
    def specific_character(self, file_string, word, letter):#(s)
        """
            Reports the n'th letter in the m'th word of the paragraph as a string. If m'th word is not present in the dictionary file then return False

            For something to constitute a word it must appear in the dictionary.txt file, this comparison is case insensitive. You should remove additional punctuation such as a ' or , when determining if something is a word or not. E.g. "python's" would be read as "pythons" and that should be checked against the dictionary.
        
            Parameters:
                file_string (str): The text string from Task 1.1
                word (int): An integer denoting which word
                letter (int): An integer denoting which letter

            Returns:
                str: The letter in position 'letter' of 'word', if the input is valid
                bool: False if the input is invalid
        """
        #Your code here
        
        try: 
            if word > 0 and letter > 0:
                return self.words[word-1][letter-1]
            else: return False
        except: return False

        pass#(s)

    #(Task 3.2)
    def word_display(self, file_string, length):#(s)
        """
            Returns a list of all words in the text string from task 1.1 which are of size 'length' or longer

            For something to constitute a word it must appear in the dictionary.txt file
        
            Parameters:
                file_string (str): The text string from Task 1.1
                length (int): An integer denoting the length of words to be counted

            Returns:
                arr[str]: A list of all words of size 'length' or longer as individual strings
        """
        #Your code here
        long_words = []
        for word in self.words:
            if len(word) >= length:
                long_words.append(word)

        return long_words

        pass#(s)

    #(Task 3.3)
    def letter_count(self, file_string, letters):#(s)
        """
            Returns a count of all letters (i.e. a-z) irrespective of case, ignoring those specified.

            Specified letters are provided in the letters parameter.
        
            Parameters:
                file_string (str): The text string from Task 1.1
                letters (arr[str]): An array of strings denoting which letters to not count

            Returns:
                int: The count of all letters ignoring those specified 
        """
        #Your code here

        count = 0
        for word in self.text:
            for letter in word:
                if letter.isalpha() and letter not in letters:
                    count += 1

        return count

        pass#(s)

    #(Task 3.4)
    def find_replace(self, file_string, old_substring, new_substring):#(s)
        """
            Find all occurrences of a substring and replace then with the provided new substring

            Directly replace the old substring with the new one with no further changes and return the whole text. If there are no occurrences of the substring then nothing will be replaced.
        
            Parameters:
                file_string (str): The text string from Task 1.1
                old_substring (str): The substring which is to be replaced
                new_substring (str): The substring which is used in the place of the removed substring

            Returns:
                str: The contents of the text as a single string
        """
        #Your code here

        return self.text.replace(old_substring,new_substring)

        pass#(s)

if __name__ == '__main__':#(s)
    #You can place any ad-hoc testing here
    my_instance = Basics()
    test1 = my_instance.read_file()
    test2 = my_instance.length_of_file('what')
    test3 = my_instance.lower_case_count('what')
    test4 = my_instance.upper_case_merge('what')
    test5 = my_instance.digits_sum('what')
    test6 = my_instance.specific_character('what', 16,-2)
    test7 = my_instance.word_display('what', 4)
    test8 = my_instance.letter_count('what', ['a','b','i'])
    test9 = my_instance.find_replace('what', 'Python', 'Snake Language')

    print(test1)
    print(test2)
    print(test3)
    print(test4)
    print(test5)
    print(test6)
    print(test7)
    print(test8)
    print(test9)

    pass#(s)