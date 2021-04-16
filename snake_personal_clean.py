import argparse, pygame, time, sys, random, threading, os


succ, oopsies = pygame.init() # catch errors on initialization
pygame.display.set_caption('Snake') # set pygame window name to "Snake"
height, width, FPS, clock = 800,800,144,pygame.time.Clock() # set height, width, FPS, and clock
window = pygame.display.set_mode((height,width)) # initialize window
block_size_x = 4 * (height / 100)
block_size_y = 4 * (width / 100)

############################          CRITICAL FUNCTIONS START          ############################

def transformImage(image): # transforms a large image into one that fits into a single grid square
	return pygame.transform.scale(image, (int(block_size_x), int(block_size_y)))

def transformImageAdv(image,x,y): # transforms a large image into one that fits into a custom dimention
	return pygame.transform.scale(image,(x,y))

def colorsNamespace(): # defines colors in a custom namespace
	white = (255,255,255)
	black = (0, 0, 0)

	return argparse.Namespace(**locals())
colors = colorsNamespace()

global tick,stop
stop = False
plzdont = False
tick = 0 
def backgroundthread(r,g,b,bkwards): # background thread that handles the background RGB color shifts
	for _ in range(2):
		if bkwards == False: # if the colors aren't going in reverse
			window.fill([r,g,b]) # color the background to R,G,B set from the last loop
			currentBkColor = [r,g,b] # set the color for the next loop
			if r == 250 and g == 250: # add to the RGB shift
				b+=10
			elif r == 250 and g < 250:
				g+=10
			elif r < 250:
				r+=10
		if r == 250 and g == 250 and b == 250 or bkwards == True: # remove from the RGB shift
																  # if already hit the cap
			bkwards = True

			if r == 0 and g == 0:
				b-=10
			elif r == 0 and g > 0:
				g-=10
			elif r > 0:
				r-=10
			if r == 0 and g == 0 and b == 0:
				bkwards = False
			window.fill([r,g,b])
			currentBkColor = [r,g,b]
	return [r,g,b,bkwards] # return current modified values back

def thread_function(name): # threading functions for backgroudthread
	global r,g,b,bkwards,tick
	localtick = tick
	while True:
		if stop:
			break
		if plzdont:
			pass
		elif localtick != tick:
			bgv = backgroundthread(r,g,b,bkwards)
			r,g,b = bgv[0],bgv[1],bgv[2]
			bkwards = bgv[3]
			localtick = tick

x = threading.Thread(target=thread_function, args=(1,))
x.start()
def startNewGame():

############################          CRITICAL FUNCTIONS END          ############################

############################          VARIABLES START          ############################

	global direction,isgameover,clockspeed,cont,tick,r,g,b,bkwards,apple_loc,pappleloc,millten,apples,image # defines global variables
	r,g,b = 0,0,0 # background color
	stop = False # if true, game stops, used for loops later on.
	apples = 0 # amount of apples eaten
	snakePosFirstx = 10 # X position of the snake when starting the game
	snakePosFirsty = 10 # Y position of the snake when starting the game
	currentBkColor = [0,0,0] # current background color
	bkwards = False # backward stepping for RGB background - set automatically
	gl = transformImageAdv(pygame.image.load(os.getcwd() + "/bkg.png"),height,width) # background
	gl1 = transformImageAdv(pygame.image.load(os.getcwd() + "/gl1.png"),height,width) # background with a glitch effect
	gl2 = transformImageAdv(pygame.image.load(os.getcwd() + "/gl2.png"),height,width) # background with a glitch effect
	gl3 = transformImageAdv(pygame.image.load(os.getcwd() + "/gl3.png"),height,width) # background with a glitch effect
	gl4 = transformImageAdv(pygame.image.load(os.getcwd() + "/gl4.png"),height,width) # background with a glitch effect
	gl5 = transformImageAdv(pygame.image.load(os.getcwd() + "/gl5.png"),height,width) # background with a glitch effect
	image = transformImage(pygame.image.load(os.getcwd() + "/apple.png")) # apple image
	papple = transformImage(pygame.image.load(os.getcwd() + "/papple.png")) # poison apple image
	eat = pygame.mixer.Sound('eat.mp3') # eating apple sound effect
	endmusic = pygame.mixer.Sound('gameover.mp3') # game over music
	music = pygame.mixer.Sound('music.mp3') # playing game music
	apple_loc = [random.randint(0,20),random.randint(0,20)] # current apple location on grid
	pappleloc = [random.randint(0,20),random.randint(0,20)] # current poison apple location on grid
	consumables = ["apple","papple"] # list of grid items that can be consumed
	borderx = 21 # max amount of grid squares until the border is hit on the X axis
	bordery = 21 # max amount of grid squares until the border is hit on the Y axis
	snakeCount = 9 # starting amount of snake body parts 
	tick = 1 # time measurement
	millten = int(time.time()) + 20 # current time + 20 to detect when the time limit is reached
	millis = 0 # defining for later use
	direction = "up" # current direction the snake is moving in
	timelol = 20 # current amount of seconds left
	snakeBP = [] # list of snake body parts on the grid (will be set later)
	cont = True # continue or stop the game
	clockspeed= 0 # time delay per clock cycle (set to 50 after 5 apples)
	window.fill(colors.black) # sets a black background for now
	stop = True # defines stop for the loop below

############################          VARIABLES END          ############################
	
	print(str(oopsies) + " errors on initialization.")

	while stop: # start menu loop
		pygame.time.wait(100)
		x = random.randint(0,15) # glitch effect
		if x == 1:
			window.blit(gl1, (0, 0))
		elif x == 2:
			window.blit(gl2, (0, 0))
		elif x == 3:
			window.blit(gl3, (0, 0))

		elif x == 4:
			window.blit(gl4, (0, 0))

		elif x == 5:
			window.blit(gl5, (0, 0))
		else:
			window.blit(gl, (0, 0))
		pygame.display.flip()
		for event in pygame.event.get(): # wait for any key press or 
										 # mouse click before moving on to game
			if event.type == pygame.QUIT:
				stop = True
				pygame.quit()
				sys.exit()
				raise SystemExit
			elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
				print("a")
				stop = False
				break

############################          FUNCTIONS START          ############################

	def createTwoDSpace(x,y): # creates a x by x list of items to store grid items on
		return [[0] * x for _ in range(y)]
	
	def setMetatable(x,y,val): # sets the metatable value at a grid position
		grid[x][y][2] = val

	def getMetatable(x,y): # gets the metatable value at a grid position
		try:
			return grid[x][y][2]
		except:
			print("UH OH")

	def drawOnGrid(x,y,value): # draws a square at (x,y) on the grid, in black.
		drawOnGridAdv(x,y,value,colors.black)

	def drawOnGridAdv(x,y,value,c): # draws a square at (x,y) on the grid, in black.
		if checkBorder(x,y):
			rect = pygame.Rect(x*(block_size_x+5), y*(block_size_y+5), block_size_x, block_size_y)
			pygame.draw.rect(window, c, rect)
			setMetatable(x,y,value)

	def drawOnGridUltraAdv(x,y,value,c,xs,ys,xt,yt): # draws a square with a custom color value, size, and position on the grid
		if checkBorder(x,y):
			rect = pygame.Rect(x*(block_size_x+5)+4, y*(block_size_y+5)+4, block_size_x-8, block_size_y-8)
			pygame.draw.rect(window, c, rect)
			setMetatable(x,y,value)


	def resetGrid(): # resets the grid and draws the apple and poison apple
		global apple_loc
		global snakePosFirstx
		global snakePosFirsty
		global pappleloc
		for item in range(len(grid)):
			for i in range(len(grid[item])):
				drawOnGridAdv(item,i,"empty",currentBkColor)
		setMetatable(apple_loc[0],apple_loc[1],"apple")
		setMetatable(pappleloc[0],pappleloc[1],"papple")
		window.blit(image, (apple_loc[0]*(block_size_x+5), apple_loc[1]*(block_size_y+5)))
		window.blit(papple, (pappleloc[0]*(block_size_x+5), pappleloc[1]*(block_size_y+5)))

	def searchFirst(xd): # searches for the first item on the grid 
						 # that matches the given metatable value
		for item in range(len(grid)):
			for x in range(len(grid[item])):
				if getMetatable(item,x) == xd:
					return [item,x]
		return False  

	def searchBulk(xd): # searches for every item on the grid that
						# matches the given metatable value
		rets = []
		for item in range(len(grid)):
			for x in range(len(grid[item])):
				if xd in getMetatable(item,x):
					rets.append([item,x])
		if len(rets) > 1:
			return rets
		return False

	def checkBorder(x,y): # checks if an x,y coordinate is outside of the grid
		return x <= borderx and y <= bordery

	def getRandomColor(): # returns a random color
		return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

	def initSnake(x,y): # initializes the snake's head at x,y in a random color
		drawOnGridAdv(x,y,"snakehead",getRandomColor())

	def refreshSnake(): # refreshes the snake on the grid
		xdd = 1
		for _ in range(snakeCount):
			x = searchFirst("snakehead")
			x,y = x[0],x[1]
			if not x:
				print("FATAL: Snake head not found???")
			if checkBorder(x,y):
				drawOnGridAdv(x,y+xdd,"snakebody"+str(xdd),getRandomColor())
				xdd+=1

	def resetApplePos(): # resets the apple's position on the grid
		global image,apple_loc,snakeCount,apples,millten,apple_loc,pappleloc
		setMetatable(apple_loc[0],apple_loc[1],"empty")
		#image.pop()
		while True:
			pappleloc = [random.randint(0,20),random.randint(0,20)]
			if getMetatable(pappleloc[0],pappleloc[1]) == "empty":
				break
		while True:
			apple_loc = [random.randint(0,20),random.randint(0,20)]
			if getMetatable(apple_loc[0],apple_loc[1]) == "empty":
				break
		window.blit(image, (apple_loc[0]*(block_size_x+5), apple_loc[1]*(block_size_y+5)))
		window.blit(image, (pappleloc[0]*(block_size_x+5), pappleloc[1]*(block_size_y+5)))
		apples+=1
		millten = int(time.time()) + 20

	def gameover(): # pulls up the game over screen
		global cont

		if cont == False:
			endmusic.stop()
			startNewGame()
		else:
			print("GAME OVER CALLED")
			stop = False
			cont = False
			music.stop()
			endmusic.play(-1)
			image = transformImageAdv(pygame.image.load(os.getcwd() + "/go.png"),height,width)
			gl1 = transformImageAdv(pygame.image.load(os.getcwd() + "/go1.png"),height,width)
			gl2 = transformImageAdv(pygame.image.load(os.getcwd() + "/go2.png"),height,width)
			gl3 = transformImageAdv(pygame.image.load(os.getcwd() + "/go3.png"),height,width)
			gl4 = transformImageAdv(pygame.image.load(os.getcwd() + "/go4.png"),height,width)
			gl5 = transformImageAdv(pygame.image.load(os.getcwd() + "/go5.png"),height,width)
			window.blit(image, (0, 0))
			pygame.display.flip()

			stop = True
			while stop:
				pygame.time.wait(100)
				x = random.randint(0,15)
				if x == 1:
					window.blit(gl1, (0, 0))
				elif x == 2:
					window.blit(gl2, (0, 0))
				elif x == 3:
					window.blit(gl3, (0, 0))

				elif x == 4:
					window.blit(gl4, (0, 0))

				elif x == 5:
					window.blit(gl5, (0, 0))

				else:
					window.blit(image, (0, 0))
				pygame.display.flip()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						stop = True
						try:
							x.join()
						except:
							print("no thread running - safe")
						pygame.quit()
						sys.exit()
						raise SystemExit
					elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONUP]:
						print("a")
						stop = False
						cont = False
						break

	def moveSnakeHead(): # moves the snake's head, then body parts, then displays the labels on the grid
		global tick, apples, time, millten, millis, direction, clockspeed
		x = searchFirst("snakehead")
		body = searchBulk("snakebody")
		if direction == "up":
			bordx = 0
			bordy = 1
		elif direction == "right":
			bordx = 1
			bordy = 0
		elif direction == "down":
			bordx = 0
			bordy = -1
		else:
			bordx = -1
			bordy = 0

		if x:

			metadata = getMetatable(x[0]+bordx, x[1]-bordy)
			if metadata == "snakebody":
				print("snake body going in on itself")
				if direction == "up":
					direction = "down"
				elif direction == "down":
					direction = "up"
				elif direction == "right":
					direction = "left"
				elif direction == "left":
					direction = "right"
				return False
			if metadata != "empty" and metadata not in consumables:
				gameover()
				return True
			elif metadata in consumables:
				eat.play()

				if metadata == "apple":
					resetApplePos()
					snakeBP.insert(0,[snakePosFirstx,snakePosFirsty+1])
				else:
					newsbp = []
					try:
						del snakeBP[0]
						del snakeBP[0]
						apples-=2
					except:
						gameover()
						return True
					print(snakeBP)
					resetApplePos()


			lol = getMetatable(snakeBP[0][0],snakeBP[0][1])
			tick+=1
			pygame.time.wait(80)
			del snakeBP[0]
			snakeBP.append([x[0],x[1]])
			resetGrid()
			if lol == "snakebody":
				drawOnGridAdv(snakeBP[0][0],snakeBP[0][1],"empty",colors.white)
			initSnake(x[0]+bordx,x[1]-bordy)
			#drawOnGridAdv(x[0],x[1],"snakebody",colors.black)
			for i in range(1,len(snakeBP)):
				drawOnGridAdv(snakeBP[i][0],snakeBP[i][1],"snakebody",colors.white)

			if (millten-int(time.time())) < 0:
				return True
			myfont = pygame.font.SysFont("Arial", 30)
			# apply it to text on a label
			if clockspeed < 10:
				label = myfont.render("Apples: " + str(apples) + ". Time: " + str((millten-int(time.time()))), 1, (255,0,0))
			else:
				label = myfont.render("Apples: " + str(apples) + ". Time: " + str((millten-int(time.time()))) + ". You ate too many apples, you're slow!", 1, (255,0,0))
			
			# put the label object on the screen at point x=100, y=100
			window.blit(label, (5, 5))
			millist = int(round(time.time() * 2000))
			return False
			


############################          FUNCTIONS END          ############################



	music.play(-1) # play game music

	grid = createTwoDSpace(22,22) # initialize the backend grid

	obs = [] # temporarily hold the obstacles
	obstacles = [] # hold permenant obstacles
	for i in range(3): # make three obstacles
		obs.append([random.randint(2,20),random.randint(2,20)])
	for item in obs: # add blocks around each obstacle
		obstacles.append(item)
		obstacles.append([item[0]+random.randint(0,1),item[0]+random.randint(0,1)])



	for y in range(22): # create a grid 22x22 wide, then fill each with squares with the metatable value of "empty"
	    for x in range(22):
	        rect = pygame.Rect(x*(block_size_x+5), y*(block_size_y+5), block_size_x, block_size_y)
	        grid[x][y] = [x*block_size_x+5,y*block_size_y+5, "empty"]
	        pygame.draw.rect(window, colors.black, rect)


	initSnake(snakePosFirstx,snakePosFirsty) # initialize the snake head
	for i in range(1,snakeCount): # initialize the snake body
		drawOnGridAdv(snakePosFirstx,snakePosFirsty+i,"snakebody",colors.white)
		snakeBP.insert(0,[snakePosFirstx,snakePosFirsty+i])



	while cont: # main game loop
		clock.tick(clockspeed)
		pygame.time.wait(clockspeed)
		if apples >= 5: # decrease speed if eaten 5 apples or more
			clockspeed = 25
		else:
			clockspeed = 0
		#try:
		if moveSnakeHead(): # if something went wrong with moving the snake, end the game
			print("GAME OVER")
			pygame.time.wait(200)
			gameover()
			stop = True
			break
		#except:
		#	gameover()
		for item in obstacles: # draw every obstacle using custom colors, sizes, and positions
			drawOnGridUltraAdv(item[0],item[1],"obstacle",[r,g,b],5,5,4,4)

		pygame.display.update() # update the screen
		millist = int(round(time.time() * 1000)) # update the current time
		millis = millist
		for event in pygame.event.get(): # check for pygame events
			if event.type == pygame.QUIT: # if client window is closed, exit
				stop = True
				pygame.quit()
				sys.exit()
				raise SystemExit
			elif event.type == pygame.KEYDOWN: # check for key inputs
				if event.key == pygame.K_w: # move snake up if key is W
					direction = "up"
				elif event.key == pygame.K_s: # move snake down if key is S
					direction = "down" 
				elif event.key == pygame.K_a: # move snake left if key is A
					direction = "left"
				elif event.key == pygame.K_d: # move snake right if key is D
					direction = "right" 


startNewGame() # start a new game