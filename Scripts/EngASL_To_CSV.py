def Book_text_convert():
    with open('PDF_ASL_Gloss_Extract.txt', 'r') as f:
        num = 0
        for line in f:
            line = line.replace(',', '').replace('.','').replace('Sign: ', '').replace('English: ', '')
            num += 1
            with open('ASL_English.csv', 'a') as f2:
                if num % 2 == 1:
                    f2.write(line.replace('\n', ''))
                    f2.write(',')
                else:
                    f2.write(line)

def Website_text_convert():
    with open('temp copy.txt', 'r', encoding="utf8") as f:
        num = 0
        string_holder = ""
        string_list = []
        for line2 in f:
            if num % 2 == 0:
                string_holder = line2.replace('\n', '').replace(',','') + ','
            else:
                string_holder += line2.replace('\n', '').replace(',','').replace('I', 'ME')
                string_list.append(string_holder)
                string_holder = ""
            num+=1
        # save string_list to csv
        with open('New_ASL_English.csv', 'w') as f2:
            for i in string_list:
                f2.write(i)
                f2.write('\n')

Website_text_convert()