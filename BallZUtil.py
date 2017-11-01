# File: Ball.py

import random
import viz
import math

# Ball class inherits event handling methods from viz.EventClass

	
#======================================================================

class EndLine:
	
	def __init__(self):
		viz.startLayer(viz.LINES)
		viz.vertexColor(1,0,0)
		viz.vertex(-100,-80)
		viz.vertex(100,-80)
		self.vertices = viz.endLayer()
		
#======================================================================

class Ball:

	# Constructor 
	def __init__(self,x,y,a):
		
		
		# Initialize Ball Instance Variables
		# radius 
		self.radius = 5
		# number of sides of regular polygon representing the ball
		self.sides = 50
		
		hyp = 2

		# velocity vector describing its direction and speed
		self.vx = math.cos(a) * hyp * 2
		self.vy = math.sin(a) * hyp * 2
		print self.vx
		
		# center location 
		self.x = x + (self.radius / 2)
		self.y = y + (self.radius / 2)
		
		
		# create layer for a circle, centered at (0,0)
		viz.startLayer(viz.POLYGON)
		#viz.vertexColor(.58,.58,.58)
		
		viz.vertexColor(.2,.2,1)		
		
		for i in range(0, 360, 360/self.sides):
			x = math.cos( math.radians(i) ) * self.radius
			y = math.sin( math.radians(i) ) * self.radius
			viz.vertex(x, y)
			
			
		# saves layer of vertices in instance variable called vertices
		self.vertices = viz.endLayer()
		
		
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def getVX(self):
		return self.vx
		
	def getVY(self):
		return self.vy
		
	def setXY(self,x,y):
		self.x = x
		self.y = y
		m = viz.Matrix()
		m.postTrans(self.x,self.y)
		self.vertices.setMatrix(m)
		
	def setVXVY(self,vx,vy):
		self.vx = vx
		self.vy = vy
		
		
#======================================================================

class PowerUp:
	
	def __init__(self, x,y):
		
		# Initialize Ball Instance Variables
		# radius 
		self.radius = 5
		# number of sides of regular polygon representing the ball
		self.sides = 4
		
		self.collisionLen = 20
		
		self.hit = False;
		
		hyp = 2
		
		self.currAngle = 0;
		
		# center location 
		self.x = x + (self.radius / 2)
		self.y = y + (self.radius / 2)
		
		# create layer for a circle, centered at (0,0)
		viz.startLayer(viz.LINE_LOOP)
		viz.vertexColor(1,1,1)


		for i in range(0, 360, 360/self.sides):
			x = math.cos( math.radians(i) ) * self.radius
			y = math.sin( math.radians(i) ) * self.radius
			viz.vertex(x, y)
			
		# saves layer of vertices in instance variable called vertices
		self.vertices = viz.endLayer()
		
	def setXY(self,x,y):
		m = viz.Matrix()
		self.x = x
		self.y = y
		m.postTrans(self.x+10,self.y-10)
		self.vertices.setMatrix(m)
		
	def getXY(self):
		return [self.x,self.y]
		
	def setAxis(self):
		m = viz.Matrix()
		self.currAngle += 4
		if self.currAngle == 360:
			self.currAngle = 0
		m.postAxisAngle(0,0,1,self.currAngle)
		m.postTrans(self.x+10,self.y-10)
		self.vertices.setMatrix(m)
		
		
	def setHit(self,hit):
		self.hit = hit
		
	def getHit(self):
		return self.hit
	
		
		
#======================================================================
		
class Launcher:
	
	def __init__(self,a):
		
		self.a = a
		
		hyp = 20
		
		self.radianAngle = viz.radians(self.a)
		
		
		self.x = math.cos(self.radianAngle) * hyp
		self.y = math.sin(self.radianAngle) * hyp
		

		viz.startLayer(viz.LINES)
		viz.vertexColor(1,1,1)
		viz.vertex(0,-100)
		viz.vertex(self.x,self.y-100)
		self.vertices = viz.endLayer()
		
	def getBarrel(self):
		self.barrelLoc = [self.x, self.y-100]
		return self.barrelLoc
		
	def getBarrelAngle(self):
		return self.radianAngle
		
		
		
	def incrementAngle(self,addedAngle):

		radianAdd = viz.radians(addedAngle)
		
		self.radianAngle += radianAdd
		print self.radianAngle

		hyp = 20
		
		self.x = math.cos(self.radianAngle) * hyp
		self.y = math.sin(self.radianAngle) * hyp
		
		self.vertices.setVertex(1,self.x,self.y-100)
		
		m = viz.Matrix()
		self.vertices.setMatrix(m)


		
#======================================================================	
		
class Block:
	
	def __init__(self, len, color, x,y, h):
		self.color = color
		self.x = x
		self.y = y
		self.len = len-.5
		self.health = h
		

		viz.startLayer(viz.POLYGON)
		viz.vertexColor(color)
		viz.vertex(0,0)
		viz.vertex(0+self.len,0+0)
		viz.vertex(0+self.len,0+self.len)
		viz.vertex(0+0,0+self.len)
		self.vertices = viz.endLayer()
		self.setXY(x,y)
		
	def setXY(self,x,y):
		m = viz.Matrix()
		self.x = x
		self.y = y
		m.postTrans(self.x,self.y)
		self.vertices.setMatrix(m)
		
	def getXY(self):
		return [self.x,self.y]

	def updateColor(self, color):
		self.vertices.remove()
		viz.startLayer(viz.POLYGON)
		viz.vertexColor(color)
		viz.vertex(0,0)
		viz.vertex(0+self.len,0+0)
		viz.vertex(0+self.len,0+self.len)
		viz.vertex(0+0,0+self.len)
		self.vertices = viz.endLayer()
		self.setXY(self.x,self.y)
#======================================================================