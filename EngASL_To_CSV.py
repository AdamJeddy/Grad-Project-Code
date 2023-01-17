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