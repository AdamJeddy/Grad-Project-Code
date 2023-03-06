------- Model Tests ---------

### Demo.h5 / Demo2.h5 => 
•	People: [Aamir, Adam, Ayesha]

•	Words: ['NoSign','hello','thanks','please','sorry','you','work','where'] 

•	No. of Vids per word: 40 vids

•	Length of vid: 25 frames

•	Camera position: front cam


------- Parameter Test Cases-----------
### test1 => 3 words, 30 vids, 30 frames (camera position - waist height)
    # avg performance, takes time to recognize, when not doing any sign by default it always detects hello
    
### test2 => 3 words + 1 default, 30 vids, 30 frames  (camera position - shoulder height)
    # Was good for nosign, hello and thank you but iloveyou wasnt good

### test3 => 3 words + 1 default, 40 vids, 30 frames  (camera position - shoulder height)
    # good performance, used in the proof of concept as well

### test4 => Ayesha -> 3 words + 1 default, 30 vids, 30 frames (camera position - shoulder height)
    # 

### test5 => HADI -> 3 words + 1 default, 30 vids, 30 frames (camera position - shoulder height)
    # 

### test5 => 3 words + 1 default, 30 vids, 30 frames  (camera position - shoulder height)
    # 

### test6 => 3 words, 30 vids, 30 frames  (camera position - waist height)

### test7 => Combination of tests 3,4,5 and check with 3 words, 100 vids, 30 frames  (camera position - shoulder height)
    #
### test8 => 3 words + 1 default, 30 vids, 25 frames  (camera position - shoulder height)
    # 
### test9 => 3 words + 1 default, 30 vids, 20 frames  (camera position - shoulder height)
    # Faster recognition of words but it can become very frantic sometimes

For real time mobile vid testing:
### test10 => 3 words + 1 default, 30 vids, 30 frames  (camera position - standing)
### test11 => 3 words + 1 default, 30 vids, 30 frames  (camera position - standing) 
### test12 => 3 words + 1 default, 30 vids, 30 frames  (camera position - sitting)
### test13 => 3 words + 1 default, 30 vids, 30 frames  (camera position -sitting)

###  test14 => ['NoSign','hello', 'thanks', 'iloveyou'], 30 vids, 25 frames  (camera position – front cam)
###  test15 => ['NoSign',’please , ‘yourewelcome, ’sorry’], 30 vids, 25 frames  (camera position – front cam)
###  test16 => ['NoSign',’please , ‘yourewelcome, ’sorry’], 30 vids, 25 frames  (camera position – front cam)
