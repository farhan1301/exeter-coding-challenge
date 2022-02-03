import csv, sys, time, os, psutil

def initialize_french_dictionary():
    file = open("french_dictionary.csv")
    french_csv_reader = csv.reader(file, delimiter=',')
    for row in french_csv_reader:
        french_dict[row[0]] = [row[1], 0]      # key:english word, value:french word, 0
    file.close()

def translate(input_file):
    output_file = open('t8.shakespeare.translate.txt', 'w')
    eng_word_list = french_dict.keys()
    input_text = open(input_file)
    while True:
        line = input_text.readline()
        if not line:
            break                              # break the loop if the current line read is empty
        new_line = ''
        for word in line.split():
            filtered = filter(str.isalpha, word)
            query = "".join(filtered)          # returns all words that contains only alphabets
            if query in eng_word_list:
                french_value = french_dict[query][0]
                french_dict[query][1] += 1     # for calculating the frequency, later on
                word = word.replace(query, french_value)
            new_line += word + ' '             # adding all the words of the line in new_line along with space
        new_line = new_line.strip()            # stripping start & end spaces
        output_file.write(new_line + '\n')     # over-writing the line with this new line - new_line
    output_file.close()
    return True

def generate_frequency_csv():
    file = open('frequency.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['English', 'French', 'Frequency'])
    for words in french_dict:
        writer.writerow([words, french_dict[words][0], french_dict[words][1]])
    return True

def generate_performance(process_time, memory_info):
    file = open('Performance.txt', 'w')
    file.write(f"Time to process : {process_time} seconds\n")
    file.write(f"Memory used : {memory_info} MB")


if __name__ == '__main__':
    process_start_time = time.time()

    french_dict = {}
    initialize_french_dictionary()
    translate('t8.shakespeare.txt')
    generate_frequency_csv()

    process_complete_time = time.time()

    memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    process_time = process_complete_time - process_start_time

    generate_performance(process_time, memory_used)

