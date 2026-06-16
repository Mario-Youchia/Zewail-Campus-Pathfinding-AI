#pillow
#xlwings
#qrcode
#PyQt5

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import xlwings as xw
import subprocess
import time
import project

class StartPositionWindow(QWidget):
	Signal = QtCore.pyqtSignal(str, str)

	def __init__(self):
		super().__init__()
		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.setWindowTitle("")
		self.setFixedSize(160, 140)
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		self.setStyleSheet('background-color:#e1ebe8')
		self.setWindowIcon(QIcon('logo.png'))
		AI_Project1.center(self)

		self.label1 = QLabel("x =", self)
		self.label1.setObjectName("label1")
		self.label1.setStyleSheet("QLabel#label1 { font-size: 14px;} ");
		self.label1.resize(20,20)
		self.label1.move(20, 20)
		
		self.label2 = QLabel("y =", self)
		self.label2.setObjectName("label2")
		self.label2.setStyleSheet("QLabel#label2 { font-size: 14px;} ");
		self.label2.resize(20,20)
		self.label2.move(20, 60)
		
		self.textbox1 = QLineEdit(self)
		self.textbox1.move(45, 20)
		self.textbox1.resize(95,20)
		self.textbox1.setObjectName("textbox1")
		self.textbox1.setStyleSheet("QLineEdit#textbox1 { border: 1px solid green;} ");

		self.textbox2 = QLineEdit(self)
		self.textbox2.move(45, 60)
		self.textbox2.resize(95,20)
		self.textbox2.setObjectName("textbox2")
		self.textbox2.setStyleSheet("QLineEdit#textbox2 { border: 1px solid green;} ");

		self.button1 = QPushButton('Enter', self)
		self.button1.clicked.connect(self.getStartPosition)
		self.button1.resize(120,20)
		self.button1.move(20,100)
		self.button1.setObjectName("button1")
		self.button1.setStyleSheet("QPushButton#button1 { border: 1px solid black; font-size: 14px;} ");

	def getStartPosition(self):
		if self.textbox1.text().isnumeric() and self.textbox2.text().isnumeric():
			if int(self.textbox1.text()) <= 395 and int(self.textbox2.text()) <= 479:
				self.Signal.emit(self.textbox1.text(), self.textbox2.text())
				self.close()
		else:
			print("Enter valid coordinates")

class AI_Project1(QMainWindow):
	app: 'AI_Project1' = None
	def __init__(self):
		super().__init__()
		self._initUI()
	
	def _initUI(self):
		self.setWindowTitle("AI Project 1")
		self.setFixedSize(730, 830)
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		self.center()
		self.setStyleSheet('background-color:#e1ebe8')
		self.setWindowIcon(QIcon('logo.png'))

		self.x = 0
		self.y = 0
		self.w = StartPositionWindow()
		self.w.show()
		self.w.Signal.connect(self.propagateInput)

		self.group_box = QGroupBox('Input', self)
		self.group_box.setObjectName("InputGroupBox")
		self.group_box.resize(470,200)
		self.group_box.move(30,30)
		self.group_box.setStyleSheet("QGroupBox#InputGroupBox { font-size: 16px; font-weight: bold; border: 2px solid black;} ");

		self.label1 = QLabel("Choose how you want to enter the info of the place you want to reach", self)
		self.label1.setObjectName("label1")
		self.label1.setStyleSheet("QLabel#label1 { font-size: 14px;} ");
		self.label1.resize(440,20)
		self.label1.move(40, 60)

		self.radio1 = QRadioButton("Coordinates", self)
		self.radio1.setObjectName("radio1")
		self.radio1.setStyleSheet("QRadioButton#radio1 { font-size: 14px;} ");
		self.radio1.move(100, 80)
		self.radio1.resize(120,35)
		self.radio1.clicked.connect(self.radioBtn1)

		self.radio2 = QRadioButton("Room, Building", self)
		self.radio2.setObjectName("radio2")
		self.radio2.setStyleSheet("QRadioButton#radio2 { font-size: 14px;} ");
		self.radio2.move(250, 80)
		self.radio2.resize(130,35)
		self.radio2.clicked.connect(self.radioBtn2)

		self.group_boxCoordinates = QGroupBox('Coordinates', self)
		self.group_boxCoordinates.setObjectName("group_boxCoordinates")
		self.group_boxCoordinates.resize(160,100)
		self.group_boxCoordinates.move(60,120)
		self.group_boxCoordinates.setStyleSheet("QGroupBox#group_boxCoordinates { font-size: 14px; color: gray; font-weight: bold; border: 1px solid blue;} ");
		
		self.label2 = QLabel("x =", self)
		self.label2.setObjectName("label2")
		self.label2.setStyleSheet("QLabel#label2 { font-size: 14px;} ");
		self.label2.resize(20,20)
		self.label2.move(70, 145)
		
		self.label3 = QLabel("y =", self)
		self.label3.setObjectName("label3")
		self.label3.setStyleSheet("QLabel#label3 { font-size: 14px;} ");
		self.label3.resize(20,20)
		self.label3.move(70, 180)

		self.textbox1 = QLineEdit(self)
		self.textbox1.move(100, 145)
		self.textbox1.setObjectName("textbox1")
		self.textbox1.setStyleSheet("QLineEdit#textbox1 { border: 1px solid green;} ");
		self.textbox1.setDisabled(True)

		self.textbox2 = QLineEdit(self)
		self.textbox2.move(100, 180)
		self.textbox2.setObjectName("textbox2")
		self.textbox2.setStyleSheet("QLineEdit#textbox2 { border: 1px solid green;} ");
		self.textbox2.setDisabled(True)

		self.group_boxBuildingRoom = QGroupBox('Building, Room', self)
		self.group_boxBuildingRoom.setObjectName("group_boxBuildingRoom")
		self.group_boxBuildingRoom.resize(190,100)
		self.group_boxBuildingRoom.move(240,120)
		self.group_boxBuildingRoom.setStyleSheet("QGroupBox#group_boxBuildingRoom { font-size: 14px; color: gray; font-weight: bold; border: 1px solid blue;} ");

		self.label4 = QLabel("Building: ", self)
		self.label4.setObjectName("label4")
		self.label4.setStyleSheet("QLabel#label4 { font-size: 14px;} ");
		self.label4.resize(50,30)
		self.label4.move(250, 145)

		self.label5 = QLabel("Room: ", self)
		self.label5.setObjectName("label5")
		self.label5.setStyleSheet("QLabel#label5 { font-size: 14px;} ");
		self.label5.resize(50,30)
		self.label5.move(250, 180)

		self.comboBox1 = QComboBox(self)
		self.comboBox1.addItem("Building")
		self.comboBox1.activated[str].connect(self.ComboBox1onChanged)  
		self.comboBox1.move(320,145)
		self.comboBox1.resize(100,30)
		self.comboBox1.setObjectName("comboBox1")
		self.comboBox1.setStyleSheet("QComboBox#comboBox1 { font-size: 14px;} ");
		self.comboBox1.setDisabled(True)

		self.comboBox2 = QComboBox(self)
		self.comboBox2.addItem("Room")
		self.comboBox2.activated[str].connect(self.ComboBox2onChanged)  
		self.comboBox2.move(320,180)
		self.comboBox2.resize(100,30)
		self.comboBox2.setObjectName("comboBox2")
		self.comboBox2.setStyleSheet("QComboBox#comboBox2 { font-size: 14px;} ");
		self.comboBox2.setDisabled(True)


		subprocess.Popen(["powershell.exe", "Start-Process \"Rooms.xlsx\""])
		time.sleep(3)
		ws = xw.Book("Rooms.xlsx").sheets['Sheet1']
		
		MaxNumberOfRows = 1048576
		for i in range(MaxNumberOfRows):
			if ws.range('A'+str(i+1)).value is None:
				break
		
		self.Range = "A1:D" + str(i)
		self.ZCInfo = ws.range(self.Range).value
		self.Buildings = []
		for i in range(len(self.ZCInfo)-1):
			if self.ZCInfo[i+1][0] not in self.Buildings:
				self.Buildings.append(self.ZCInfo[i+1][0])
		
		self.comboBox1.addItems(self.Buildings)

		self.button1 = QPushButton('GO!', self)
		self.button1.clicked.connect(self.Go)
		self.button1.resize(50,30)
		self.button1.move(442, 190)
		self.button1.setObjectName("button1")
		self.button1.setStyleSheet("QPushButton#button1 { border: 1px solid black; font-size: 14px;} ");

		self.group_box2 = QGroupBox('Output', self)
		self.group_box2.setObjectName("OutputGroupBox")
		self.group_box2.resize(150,200)
		self.group_box2.move(550,30)
		self.group_box2.setStyleSheet("QGroupBox#OutputGroupBox { font-size: 16px; font-weight: bold; border: 2px solid black;} ");

		self.label6 = QLabel("Route status", self)
		self.label6.setObjectName("label6")
		self.label6.setStyleSheet("QLabel#label6 { font-size: 14px;} ");
		self.label6.resize(120,60)
		self.label6.move(570, 60)
		self.label6.setWordWrap(True)
		self.label6.setText("Select a destination and press GO.")

		self.group_box3 = QGroupBox('Visualization', self)
		self.group_box3.setObjectName("VisualizationGroupBox")
		self.group_box3.resize(670,300)
		self.group_box3.move(30,260)
		self.group_box3.setStyleSheet("QGroupBox#VisualizationGroupBox { font-size: 16px; font-weight: bold; border: 2px solid black;} ");
		
		self.group_box4 = QGroupBox('Route Description', self)
		self.group_box4.setObjectName("RouteGroupBox")
		self.group_box4.resize(670,200)
		self.group_box4.move(30,590)
		self.group_box4.setStyleSheet("QGroupBox#RouteGroupBox { font-size: 16px; font-weight: bold; border: 2px solid black;} ");

		'''self.PlainTextEditRoute = QPlainTextEdit(self)
		self.PlainTextEditRoute.move(45, 615)
		self.PlainTextEditRoute.resize(630,120)
		self.PlainTextEditRoute.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEditRoute.setReadOnly(True)
		self.PlainTextEditRoute.setObjectName("PlainTextEditRoute")
		self.PlainTextEditRoute.setStyleSheet("QPlainTextEdit#PlainTextEditRoute { font-size: 14px;} ");'''

		self.tabs = QTabWidget(self)
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tab3 = QWidget()
		self.tab4 = QWidget()
		self.tab5 = QWidget()
		self.tab6 = QWidget()
		self.tab7 = QWidget()
		self.tabs.resize(630,250)
		self.tabs.move(45, 285)
		self.tabs.addTab(self.tab1,"BFS")
		self.tabs.addTab(self.tab2,"DFS")
		self.tabs.addTab(self.tab3,"IDS")
		self.tabs.addTab(self.tab4,"Greedy best-first")
		self.tabs.addTab(self.tab5,"A*")
		self.tabs.addTab(self.tab6,"Hill Climbing")
		self.tabs.addTab(self.tab7,"Simulated Annealing")
		
		self.tab1.layout = QVBoxLayout(self)
		self.tab2.layout = QVBoxLayout(self)
		self.tab3.layout = QVBoxLayout(self)
		self.tab4.layout = QVBoxLayout(self)
		self.tab5.layout = QVBoxLayout(self)
		self.tab6.layout = QVBoxLayout(self)
		self.tab7.layout = QVBoxLayout(self)


		self.tab1.layout.setContentsMargins(0, 0, 0, 0)
		self.imageLabel = QLabel(self)
		
		
		self.imageLabel.setObjectName("Map")
		self.imageLabel.setStyleSheet("QLabel#Map { border: 1px solid black; } ");
		self.imageLabel.move(570, 100)
		self.imageScrollArea = QScrollArea()
		self.imageScrollArea.setWidget(self.imageLabel)
		self.tab1.layout.addWidget(self.imageScrollArea)
		self.tab1.setLayout(self.tab1.layout)





		self.PlainTextEdit1 = QPlainTextEdit()
		#self.PlainTextEdit1.move(45, 285)
		self.PlainTextEdit1.resize(630,250)
		self.PlainTextEdit1.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit1.setReadOnly(True)
		self.PlainTextEdit1.setObjectName("PlainTextEdit1")
		self.PlainTextEdit1.setStyleSheet("QPlainTextEdit#PlainTextEdit1 { font-size: 14px;} ");

		self.PlainTextEdit2 = QPlainTextEdit()
		self.PlainTextEdit2.resize(630,250)
		self.PlainTextEdit2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit2.setReadOnly(True)
		self.PlainTextEdit2.setObjectName("PlainTextEdit2")
		self.PlainTextEdit2.setStyleSheet("QPlainTextEdit#PlainTextEdit2 { font-size: 14px;} ");
		
		self.PlainTextEdit3 = QPlainTextEdit()
		self.PlainTextEdit3.resize(630,250)
		self.PlainTextEdit3.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit3.setReadOnly(True)
		self.PlainTextEdit3.setObjectName("PlainTextEdit3")
		self.PlainTextEdit3.setStyleSheet("QPlainTextEdit#PlainTextEdit3 { font-size: 14px;} ");

		self.PlainTextEdit4 = QPlainTextEdit()
		self.PlainTextEdit4.resize(630,250)
		self.PlainTextEdit4.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit4.setReadOnly(True)
		self.PlainTextEdit4.setObjectName("PlainTextEdit4")
		self.PlainTextEdit4.setStyleSheet("QPlainTextEdit#PlainTextEdit4 { font-size: 14px;} ");
		
		self.PlainTextEdit5 = QPlainTextEdit()
		self.PlainTextEdit5.resize(630,250)
		self.PlainTextEdit5.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit5.setReadOnly(True)
		self.PlainTextEdit5.setObjectName("PlainTextEdit5")
		self.PlainTextEdit5.setStyleSheet("QPlainTextEdit#PlainTextEdit5 { font-size: 14px;} ");

		self.PlainTextEdit6 = QPlainTextEdit()
		self.PlainTextEdit6.resize(630,250)
		self.PlainTextEdit6.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit6.setReadOnly(True)
		self.PlainTextEdit6.setObjectName("PlainTextEdit6")
		self.PlainTextEdit6.setStyleSheet("QPlainTextEdit#PlainTextEdit6 { font-size: 14px;} ");

		self.PlainTextEdit7 = QPlainTextEdit()
		self.PlainTextEdit7.resize(630,250)
		self.PlainTextEdit7.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit7.setReadOnly(True)
		self.PlainTextEdit7.setObjectName("PlainTextEdit7")
		self.PlainTextEdit7.setStyleSheet("QPlainTextEdit#PlainTextEdit7 { font-size: 14px;} ");

		self.restart = QShortcut(QKeySequence('Ctrl+R'), self)
		self.restart.activated.connect(self.Restart)

		#self.tab1.layout.addWidget(self.PlainTextEdit1)
		self.tab2.layout.addWidget(self.PlainTextEdit2)
		self.tab3.layout.addWidget(self.PlainTextEdit3)
		self.tab4.layout.addWidget(self.PlainTextEdit4)
		self.tab5.layout.addWidget(self.PlainTextEdit5)
		self.tab6.layout.addWidget(self.PlainTextEdit6)
		self.tab7.layout.addWidget(self.PlainTextEdit7)

		#self.tab1.setLayout(self.tab1.layout)
		self.tab2.setLayout(self.tab2.layout)
		self.tab3.setLayout(self.tab3.layout)
		self.tab4.setLayout(self.tab4.layout)
		self.tab5.setLayout(self.tab5.layout)
		self.tab6.setLayout(self.tab6.layout)
		self.tab7.setLayout(self.tab7.layout)

		self.tabs2 = QTabWidget(self)
		self.tab1_2 = QWidget()
		self.tab2_2 = QWidget()
		self.tab3_2 = QWidget()
		self.tab4_2 = QWidget()
		self.tab5_2 = QWidget()
		self.tab6_2 = QWidget()
		self.tab7_2 = QWidget()
		self.tabs2.resize(630,150)
		self.tabs2.move(45, 615)
		self.tabs2.addTab(self.tab1_2,"BFS")
		self.tabs2.addTab(self.tab2_2,"DFS")
		self.tabs2.addTab(self.tab3_2,"IDS")
		self.tabs2.addTab(self.tab4_2,"Greedy best-first")
		self.tabs2.addTab(self.tab5_2,"A*")
		self.tabs2.addTab(self.tab6_2,"Hill Climbing")
		self.tabs2.addTab(self.tab7_2,"Simulated Annealing")

		self.tab1_2.layout = QVBoxLayout(self)
		self.tab2_2.layout = QVBoxLayout(self)
		self.tab3_2.layout = QVBoxLayout(self)
		self.tab4_2.layout = QVBoxLayout(self)
		self.tab5_2.layout = QVBoxLayout(self)
		self.tab6_2.layout = QVBoxLayout(self)
		self.tab7_2.layout = QVBoxLayout(self)

		self.PlainTextEdit1_2 = QPlainTextEdit()
		self.PlainTextEdit1_2.resize(630,200)
		self.PlainTextEdit1_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit1_2.setReadOnly(True)
		self.PlainTextEdit1_2.setObjectName("PlainTextEdit1_2")
		self.PlainTextEdit1_2.setStyleSheet("QPlainTextEdit#PlainTextEdit1_2 { font-size: 14px;} ");


		self.PlainTextEdit2_2 = QPlainTextEdit()
		self.PlainTextEdit2_2.resize(630,200)
		self.PlainTextEdit2_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit2_2.setReadOnly(True)
		self.PlainTextEdit2_2.setObjectName("PlainTextEdit2_2")
		self.PlainTextEdit2_2.setStyleSheet("QPlainTextEdit#PlainTextEdit2_2 { font-size: 14px;} ");

		self.PlainTextEdit3_2 = QPlainTextEdit()
		self.PlainTextEdit3_2.resize(630,200)
		self.PlainTextEdit3_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit3_2.setReadOnly(True)
		self.PlainTextEdit3_2.setObjectName("PlainTextEdit3_2")
		self.PlainTextEdit3_2.setStyleSheet("QPlainTextEdit#PlainTextEdit3_2 { font-size: 14px;} ");

		self.PlainTextEdit4_2 = QPlainTextEdit()
		self.PlainTextEdit4_2.resize(630,200)
		self.PlainTextEdit4_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit4_2.setReadOnly(True)
		self.PlainTextEdit4_2.setObjectName("PlainTextEdit4_2")
		self.PlainTextEdit4_2.setStyleSheet("QPlainTextEdit#PlainTextEdit4_2 { font-size: 14px;} ");

		self.PlainTextEdit5_2 = QPlainTextEdit()
		self.PlainTextEdit5_2.resize(630,200)
		self.PlainTextEdit5_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit5_2.setReadOnly(True)
		self.PlainTextEdit5_2.setObjectName("PlainTextEdit5_2")
		self.PlainTextEdit5_2.setStyleSheet("QPlainTextEdit#PlainTextEdit5_2 { font-size: 14px;} ");

		self.PlainTextEdit6_2 = QPlainTextEdit()
		self.PlainTextEdit6_2.resize(630,200)
		self.PlainTextEdit6_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit6_2.setReadOnly(True)
		self.PlainTextEdit6_2.setObjectName("PlainTextEdit6_2")
		self.PlainTextEdit6_2.setStyleSheet("QPlainTextEdit#PlainTextEdit6_2 { font-size: 14px;} ");

		self.PlainTextEdit7_2 = QPlainTextEdit()
		self.PlainTextEdit7_2.resize(630,200)
		self.PlainTextEdit7_2.setLineWrapMode(QPlainTextEdit.NoWrap)
		self.PlainTextEdit7_2.setReadOnly(True)
		self.PlainTextEdit7_2.setObjectName("PlainTextEdit7_2")
		self.PlainTextEdit7_2.setStyleSheet("QPlainTextEdit#PlainTextEdit7_2 { font-size: 14px;} ");

		self.tab1_2.layout.addWidget(self.PlainTextEdit1_2)
		self.tab2_2.layout.addWidget(self.PlainTextEdit2_2)
		self.tab3_2.layout.addWidget(self.PlainTextEdit3_2)
		self.tab4_2.layout.addWidget(self.PlainTextEdit4_2)
		self.tab5_2.layout.addWidget(self.PlainTextEdit5_2)
		self.tab6_2.layout.addWidget(self.PlainTextEdit6_2)
		self.tab7_2.layout.addWidget(self.PlainTextEdit7_2)

		self.tab1_2.setLayout(self.tab1_2.layout)
		self.tab2_2.setLayout(self.tab2_2.layout)
		self.tab3_2.setLayout(self.tab3_2.layout)
		self.tab4_2.setLayout(self.tab4_2.layout)
		self.tab5_2.setLayout(self.tab5_2.layout)
		self.tab6_2.setLayout(self.tab6_2.layout)
		self.tab7_2.setLayout(self.tab7_2.layout)

		# Keep the room-based route-description output active after the later UI revision.
		self.PlainTextEditRoute = self.PlainTextEdit1_2

		self.show()

	def center(self):
		qr = self.frameGeometry()
		qr.moveCenter(QDesktopWidget().availableGeometry().center())
		self.move(qr.topLeft())

	def Go(self):
		x = 0
		y = 0
		routeDescription = ''
		if self.radio2.isChecked():
			if self.comboBox2 != "Room":
				for i in range(len(self.ZCInfo)-1):
					if self.ZCInfo[i+1][1] == self.comboBox2.currentText() and self.ZCInfo[i+1][0] == self.comboBox1.currentText():
						x = self.ZCInfo[i+1][2]
						y = self.ZCInfo[i+1][3]
						routeDescription = self.ZCInfo[i+1][4]
				self.PlainTextEditRoute.clear()
				Route = []
				Route = routeDescription.split('@')
				for route in Route:
					self.PlainTextEditRoute.appendPlainText(route)
			else:
				print("Choose a room")
		elif self.radio1.isChecked():
			x = self.textbox1.text()
			y = self.textbox2.text()
			if x.isnumeric() and y.isnumeric():
				if int(x) <= 395 and int(y) <= 479:
					start = (self.x,self.y)
					print("-"*100)
					print(start)
					user_input = 1
					dest = (x,y)
					#1- BFS, 2- DFS, 3- IDS, 4- Greedy best-first, 5- A*, 6- Hill Climbing, 7- Simulated Annealing
					alg = 1
					states = []
					states.append(tuple((int(start[0]), int(start[1]))))
					States = project.program(start, user_input, dest, alg)
					print(States)
					'''for state in States:
						states.append(state)
					states.append(tuple((int(dest[0]), int(dest[1]))))
					print(states)

					image = project.cv2.imread('image.png')
					newImage = 0
					for i in range(len(states)-1):
						firstPoint = (states[i][0]*2, states[i][1]*2)
						secondPoint = (states[i+1][0]*2, states[i+1][1]*2)
						if i == 0:
							newImage = project.cv2.circle(image, firstPoint, radius=7, color=(0, 0, 255), thickness = -1)
						elif i == len(states) -1 -1:
							newImage = project.cv2.circle(image, firstPoint, radius=7, color=(0, 255, 0), thickness = -1)
						newImage = project.cv2.line(image, firstPoint, secondPoint, (255,0,0), 2)
					project.cv2.imwrite('test.png', newImage)
					self.pixMap = QPixmap("test.png")
					self.imageLabel.resize(self.pixMap.width(),self.pixMap.height())
					self.imageLabel.setPixmap(self.pixMap)
					'''
			else:
				print("Enter valid coordinates")
		self.radio1.setDisabled(True)
		self.radio2.setDisabled(True)

		self.label6.setText("Route calculated")
		
		self.PlainTextEdit1.clear()
		self.PlainTextEdit2.clear()
		self.PlainTextEdit3.clear()
		self.PlainTextEdit4.clear()
		self.PlainTextEdit5.clear()
		self.PlainTextEdit6.clear()
		self.PlainTextEdit7.clear()
		for i in range(100):
			if i%9 == 0:
				self.PlainTextEdit1.appendPlainText(str(0)*100)
				self.PlainTextEdit2.appendPlainText(str(0)*100)
				self.PlainTextEdit3.appendPlainText(str(0)*100)
				self.PlainTextEdit4.appendPlainText(str(0)*100)
				self.PlainTextEdit5.appendPlainText(str(0)*100)
				self.PlainTextEdit6.appendPlainText(str(0)*100)
				self.PlainTextEdit7.appendPlainText(str(0)*100)
			else:
				self.PlainTextEdit1.appendPlainText(str(9-i%9)*100)
				self.PlainTextEdit2.appendPlainText(str(9-i%9)*100)
				self.PlainTextEdit3.appendPlainText(str(9-i%9)*100)
				self.PlainTextEdit4.appendPlainText(str(9-i%9)*100)
				self.PlainTextEdit5.appendPlainText(str(9-i%9)*100)
				self.PlainTextEdit6.appendPlainText(str(9-i%9)*100)
				self.PlainTextEdit7.appendPlainText(str(9-i%9)*100)
	def propagateInput(self, x, y):
		self.x = x
		self.y = y

	def ComboBox1onChanged(self, text):
		self.comboBox2.clear()
		self.comboBox2.addItem("Room")
		if text != "Building":
			for i in range(len(self.ZCInfo)-1):
				if self.ZCInfo[i+1][0] == text:
					self.comboBox2.addItem(self.ZCInfo[i+1][1])

	def ComboBox2onChanged(self, text):
		print(text)

	def radioBtn1(self):
		if self.radio1.isChecked():
			self.CoordinatesMethod()

	def radioBtn2(self):
		if self.radio2.isChecked():
			self.RoomBuildingMethod()

	def CoordinatesMethod(self):
		self.group_boxCoordinates.setStyleSheet("QGroupBox#group_boxCoordinates { font-size: 14px; color: black; font-weight: bold; border: 1px solid blue;} ");
		self.textbox1.setDisabled(False)
		self.textbox2.setDisabled(False)
		self.group_boxBuildingRoom.setStyleSheet("QGroupBox#group_boxBuildingRoom { font-size: 14px; color: gray; font-weight: bold; border: 1px solid blue;} ");
		self.comboBox1.setDisabled(True)
		self.comboBox2.setDisabled(True)
	
	def RoomBuildingMethod(self):
		self.group_boxCoordinates.setStyleSheet("QGroupBox#group_boxCoordinates { font-size: 14px; color: gray; font-weight: bold; border: 1px solid blue;} ");
		self.textbox1.setDisabled(True)
		self.textbox2.setDisabled(True)
		self.group_boxBuildingRoom.setStyleSheet("QGroupBox#group_boxBuildingRoom { font-size: 14px; color: black; font-weight: bold; border: 1px solid blue;} ");
		self.comboBox1.setDisabled(False)
		self.comboBox2.setDisabled(False)
	
	@staticmethod
	def Restart():
		AI_Project1.app = AI_Project1()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	AI_Project1.Restart()
	sys.exit(app.exec_())