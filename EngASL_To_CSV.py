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
"""
def Website_text_convert():
    with open('English_ASLGloss.txt', 'r', encoding="utf8") as f:
        num = 1
        # ERROR HERE, CHECK
        for line2 in f:
            if num % 1 == 0:
                print(line2, end='')
            num+=1

Website_text_convert()
"""