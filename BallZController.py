# File: Controller.py

import random
import viz
from BallZUtil import *

# Controller class inherits event handling methods from viz.EventClass
class BallZController(viz.EventClass):
	
#----------------------------------------------------------------------
	
	def __init__(self):
	
		
		self.soundRate = 1
		self.sound = viz.addAudio('Rolemusic_-_Keiken_soku.wav') 
		self.sound.loop(viz.ON) 
		self.sound.volume(.5) 
		self.sound.setTime(.3) 
		self.sound.setRate(self.soundRate) 
		self.sound.play() 
		
		# must call constructor of EventClass first!!
		viz.EventClass.__init__(self)
		
		# list to store the balls in the game for tracking
		self.ballList = []
		
		# number of balls in the game
		self.ballNum = 0
		
		# reference to the launcher object
		self.launcher = Launcher(45)
		
		self.launcher.vertices.setScale(1,1,1)
	
		# list to store block in the game
		self.blockList = []
		
		# setting up the timers for the game
		self.callback(viz.TIMER_EVENT,self.onTimer)
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.starttimer(1,.02,viz.FOREVER) 					# timer for ball movement
		self.starttimer(3,viz.FASTEST_EXPIRATION,viz.FOREVER)	# timer for collision detection
		self.starttimer(4,.06, viz.FOREVER) # timer for powerup scaling

		# number of times player has hit space
		self.numSpace = 0
		self.ballPowerUps = 0
		self.ballsCleared = False
		self.level = 0
		
		self.powerUpList = []
		
		self.end = EndLine()

		self.blockInitializer()
			
#----------------------------------------------------------------------

	def collider(self):
		for ball in self.ballList:
			for powerUp in self.powerUpList:
				ballX = ball.getX()
				ballY = ball.getY()
				
				ballVX = ball.getVX()
				ballVY = ball.getVY()
				
				ballLeftSide = ballX - ball.radius
				ballRightSide = ballX + ball.radius
				ballTopSide = ballY + ball.radius
				ballBottomSide = ballY - ball.radius
				
				pX = powerUp.getXY()[0]
				pY = powerUp.getXY()[1]
				
				if ballTopSide >= pY-10 and ballLeftSide <= pX+10 and ballRightSide >= pX-10 and ballBottomSide <= pY+10 and PowerUp.getHit(powerUp) == False:
					powerUp.vertices.remove()
					self.powerUpList.remove(powerUp)
					powerUp.setHit(True)
					self.ballPowerUps += 1
					viz.playSound('powerup.wav')
					
			for block in self.blockList:
				
				ballX = ball.getX()
				ballY = ball.getY()
				
				ballVX = ball.getVX()
				ballVY = ball.getVY()
				
				ballLeftSide = ballX - ball.radius
				ballRightSide = ballX + ball.radius
				ballTopSide = ballY + ball.radius
				ballBottomSide = ballY - ball.radius

				blockX = block.getXY()[0]
				blockY = block.getXY()[1]

				if ballTopSide >= blockY and ballLeftSide <= blockX+20 and ballRightSide >= blockX and ballBottomSide <= blockY+20:
					if (ballTopSide >= blockY and ballTopSide <= blockY+5):
						ballVY = abs(ballVY)
						ballVY *= -1
						block.health -= 60
						block.updateColor(self.blockColorPicker(block.health))
						viz.playsound('laser1.wav')
					elif ballBottomSide <= blockY+20 and ballBottomSide >= blockY+15:
						ballVY = abs(ballVY)
						block.health -= 60
						block.updateColor(self.blockColorPicker(block.health))
						viz.playsound('laser1.wav')
					elif ballLeftSide <= blockX+20 and ballLeftSide >= blockX+15:
						ballVX = abs(ballVX)
						#ballVX *= -1
						block.health -= 60
						block.updateColor(self.blockColorPicker(block.health))
						viz.playsound('laser1.wav')
					elif ballRightSide >= blockX and ballRightSide <= blockX+5:
						ballVX = abs(ballVX)
						ballVX *= -1
						block.health -= 60
						block.updateColor(self.blockColorPicker(block.health))
						viz.playsound('laser1.wav')
						
						
					if block.health <= 0:
						block.vertices.remove()
						self.blockList.remove(block)
					
				ball.setVXVY(ballVX,ballVY)

#----------------------------------------------------------------------

	def blockColorPicker(self, health):
			if health >= 190:
				value = (380 - health) + 65
				color = [1, value/255, .25]
			else:
				value = health + 65
				color = [value/255, 1, .25]
			return color
			
#----------------------------------------------------------------------

	def blockInitializer(self):
		
		
		# setting the level range to determine new block thickness
		if self.level <= 3:
			maxRange = 4
			minHealth = 1
			maxHealth = 150
		elif self.level <= 6:
			maxRange = 5
			minHealth = 50
			maxHealth = 380
		elif self.level <= 9:
			maxRange = 6
			minHealth = 50
			maxHealth = 380
		elif self.level <= 12:
			maxRange = 7
			minHealth = 150
			maxHealth = 380
		elif self.level <= 15:
			maxRange = 8
			minHealth = 300
			maxHealth = 380
		elif self.level <= 18:
			maxRange = 7
			minHealth = 300
			maxHealth = 380
		elif self.level <= 21:
			maxRange = 6
			minHealth = 300
			maxHealth = 380
		else:
			maxRange = 5
			minHealth = 380
			maxHealth = 380
		
		#initializing the new line of blocks
		for i in range (0,200,20):
			
			num = random.randint(0,12)
			self.sound.setRate
			health = random.uniform(minHealth,maxHealth)
			
			color = self.blockColorPicker(health)

			if num >= 0 and num <= maxRange:
				newBlock = Block(20,color,-100+i,80,health)
				self.blockList.append(newBlock)
			elif num == 12:
				newPowerUp = PowerUp(0,0)
				newPowerUp.setXY(-100+i,100)
				self.powerUpList.append(newPowerUp)
				

		if len(self.blockList) == 0:
			newBlock = Block(20,self.blockColorPicker(100),0,0,100)
			newBlock.setXY(-100 + i, 80)
			self.blockList.append(newBlock)
			
#----------------------------------------------------------------------
			
	def blockManager(self):
		self.level += 1
		warned = False
		
		if self.level == 10:
			self.soundRate += .1
			self.sound.setRate(self.soundRate)
		elif self.level == 20:
			self.soundRate += .1
			self.sound.setRate(self.soundRate)
		
		for block in self.blockList:
			block.setXY(block.getXY()[0],block.getXY()[1]-20)
			if block.getXY()[1] <= -100:
				viz.quit()
			if block.getXY()[1] <= -80 and not warned:
				viz.playsound('warning.wav')
				warned = True


		for powerUp in self.powerUpList:
			powerUp.setXY(powerUp.getXY()[0],powerUp.getXY()[1]-20)

#----------------------------------------------------------------------

	def onKeyDown(self,key):
		if key == " " and self.ballNum <= 0:
			self.starttimer(2,.2,self.ballPowerUps)
		if key == viz.KEY_UP:
			for b in self.ballList:
				vx = b.getVX()
				vy = b.getVY()
				vx = vx + (vx * 0.05)
				vy = vy + (vy * 0.05)
				b.setVXVY(vx,vy)
		if key == viz.KEY_DOWN:
			for b in self.ballList:
				vx = b.getVX()
				vy = b.getVY()
				vx = vx - (vx * 0.05)
				vy = vy - (vy * 0.05)
				b.setVXVY(vx,vy)
		if key == viz.KEY_LEFT and self.ballNum <= 0:
			self.launcher.incrementAngle(2)

		if key == viz.KEY_RIGHT and self.ballNum <= 0:
			self.launcher.incrementAngle(-2)


				
#----------------------------------------------------------------------	
		
	def onTimer(self,num):
		if num == 4:
			for powerUp in self.powerUpList:
				powerUp.setAxis()
		if num == 3 and self.ballNum > 0:
			self.collider()
		if num == 2:
			print self.launcher.getBarrelAngle()
			self.ball = Ball(self.launcher.getBarrel()[0],self.launcher.getBarrel()[1],self.launcher.getBarrelAngle())
			self.ballList.append(self.ball)
			self.ballNum += 1
		
		if num == 1:
			if self.ballNum > 0:
				
				for b in self.ballList:

					x = b.getX()
					y = b.getY()
				
				
					vx = b.getVX()
					vy = b.getVY()
					
					x += vx
					y += vy
					
					b.setXY(x,y)

					if (x + b.radius) >= 100:
						vx = abs(vx)
						vx *= -1
						viz.playsound('laser2.wav')
					if (x - b.radius) <= -100:
						vx = abs(vx)
						viz.playsound('laser2.wav')
					if (y + b.radius) >= 100:
						vy = abs(vy)
						vy *= -1
						viz.playsound('laser2.wav')
					if (y-b.radius <= -110): # remove from game
						self.ballList.remove(b)
						self.ballNum -= 1
						
						# new level ahoy
						if self.ballNum == 0:
							self.ballsCleared = True
						
						if self.ballsCleared == True:
							self.blockManager()
							self.blockInitializer()
							self.ballsCleared = False;
					b.setVXVY(vx,vy)

#----------------------------------------------------------------------
