# LLB-BOT
Leathal league blaze (from now on llb) bot using opencv :))
![Wow](https://hc-cdn.hel1.your-objectstorage.com/s/v3/14e9d6d755dd43bfb529bdde71463d45ccca62ec_screenshot_2025-09-29_213133.png)

# How to run
## prerequirments
1. To run this you will need leathal league blaze on steam (20bucks but it's a solid game ;DD)
> If no llb demo: https://youtu.be/SNY3Zct-8NQ
2. Then you will also need a way to run python
## Run
1. Open LLB and make sure not to minimize it (it auto closes if you do that)
2. Run main.py (with your prefered py complier or intrepreter [idk what they are called ://])
3. If you want to bot to play then you have to choose raptor with this specific skin
![Skin_in_question](https://hc-cdn.hel1.your-objectstorage.com/s/v3/6f2c3b605df2509f1a880bac5149201170b1ff1b_screenshot_2025-09-29_213005.png)
4. As well it needs to be with keyboard inputs aka player 1
5. Have fun

# Instructions
## Keyboard
Works even when not tabed in
Q - quits
W - enables / disables bot (sugest beeing tabed in llb)
E - debug prints time
R - resets the border for map (when you end game or start new one)

# Py scripts
main.py - it is just manager for others, if i need another layer i can easily add it :DD (or bot)
util.py - this is where open cv gets input data as well where player is moved
Real_utils.py - My smart idea to create custom vector 2d class XD
LLBlazze.py - holds all classes for game like ball and others as well do calculation on what to do (moves player and calculates ball bounces)

# How does it work?
1. Im using color to detect colors in game (specific tones) it's pretty easy since this game is stylized and colors are pretty carefully chosen
2. Then using that i'm getting players and balls position
3. Then from ball position i'm making border
4. Then i get last balls position and calculate line till border
5. Then i do that few time and that's all :DD
6. For player movement i just compare positions (litralyy players x with balls x)
7. For hitting i get distnace from player and ball (can be changed in LLBlaze.py at the most bottom) - `"Hit" : self.players[0].position.distance_to(self.ball.position) < 200` and just the 200 :DD
![Hit](https://hc-cdn.hel1.your-objectstorage.com/s/v3/a88aaff3a2a2fa5a7a9369cb97e2e5f9585a869c_screenshot_2025-09-29_213103.png)

> Resources also just formyself so i rember them :))
> i have made so many but now i'm doing for gigs and gas XD (to see how much resources i use :DD)
# Docs used
## Py
1. https://medium.com/@sasasulakshi/opencv-object-masking-b3143e310d03
2. https://www.geeksforgeeks.org/computer-vision/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-with-cv-inrange-opencv
3. https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga17ed9f5d79ae97bd4c7cf18403e1689a
> as well 
>   https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71
>   https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga4303f45752694956374734a03c54d5ff
4. https://www.geeksforgeeks.org/python/find-and-draw-contours-using-opencv-python
5. https://answers.opencv.org/question/204175/how-to-get-boundry-and-center-information-of-a-mask
6. https://docs.opencv.org/4.x/d0/d49/tutorial_moments.html
7. https://www.geeksforgeeks.org/python/python-opencv-find-center-of-contour
8. https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html
9. https://realpython.com/python-multiple-constructors/
10. https://www.geeksforgeeks.org/python/python-opencv-cv2-polylines-method/
11. https://www.reddit.com/r/opencv/comments/e1j7dg/question_is_there_a_way_to_calculate_the
12. https://stackoverflow.com/questions/53381360/how-do-i-detect-a-keypress-event-with-pyautogui
13. https://pyautogui.readthedocs.io/en/latest/keyboard.html
14. https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python
15. https://stackoverflow.com/questions/66036844/time-time-or-time-perf-counter-which-is-faster
16. https://realpython.com/python-profiling/
## C
1. https://stackoverflow.com/questions/145270/calling-c-c-from-python
2. https://docs.python.org/3/library/ctypes.html#module-ctypes
3. https://stackoverflow.com/questions/4755303/python-cdll-cant-find-module
> At this point i got so sick and tierd of this that i pulled out visual studio (not vs code XD)
4. https://learn.microsoft.com/en-us/cpp/build/walkthrough-creating-and-using-a-dynamic-link-library-cpp?view=msvc-170
# Tutorials used
1. https://www.youtube.com/watch?v=WymCpVUPWQ4
2. https://www.youtube.com/watch?v=OlEEv7lLbW0