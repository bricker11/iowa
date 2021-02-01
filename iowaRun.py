import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from iowa import *

consentContent = "Thank you for your interest in taking part in this research. Before you agree to take part, the person organising " \
                 + "\nthe research must explain the project to you. " \
                 + "\n"\
                 + "\n\tParticipant’s Statement" \
                 + "\n"\
                 + "\n-	I have read the notes written above and the Information Sheet, and understand what the study involves. " \
                 + "\n\tunderstand the nature of data gathered by the use of the program."\
                 + "\n-	I understand that if I decide at any time that I no longer wish to take part in this project, I can quit " \
                 + "\n\tanytime. Moreover, confidentiality and anonymity will be maintained and consent to the processing of"\
                 + "\n\tmy personal information for the purposes of this research study."\
                 + "\n-	I understand that such information will be treated as strictly confidential and handled in accordance with " \
                 + "\n\tthe provisions of the Data Protection Act 1998."\
                 + "\n-	I agree that the research project named above has been explained to me to my satisfaction and I agree to take " \
                 + "\n\tpart in this study."

introduceContent = "There are 4 decks of cards A/B/C/D. "\
                   + "But the positive is reward or a combination of reward "\
                   + "and punishment. The specific arrangement of the rewards "\
                   + "and punishments for playing cards is: Card A gives a reward "\
                   + "of 100 US dollars each time, but there will be 5 times in 10 "\
                   + "consecutive times with a penalty of 35-150 dollars; Card B "\
                   + "gives a reward of 100 US dollars each time, but 10 times in "\
                   + "a row. There was a penalty of US$1250; Card C gave a reward of "\
                   + "US$50 each time, but 5 times out of 10 consecutive times was a "\
                   + "penalty of US$25-75; Card D gave a reward of US$50 each time, but "\
                   + "once in 10 consecutive times A penalty of $250. Before the start of "\
                   + "the task, the subjects did not know the number and frequency of the "\
                   + "rewards and punishments in the cards, but were told to choose 1 of the "\
                   + "4 decks of cards (each deck of cards in order from top to bottom) to "\
                   + "achieve Choose multiple times to win points as much as possible. "\
                   + "Participants started with $2,000."

consentWarnning = 'You can not start without agreement!'

# 每副牌的奖励值和惩罚列表
gainDeckA = 100
costDeckA = \
    [
    0,0,150,0,300,0,200,0,250,350,\
    0,350,0,250,200,0,300,150,0,0,\
    0,300,0,350,0,200,250,150,0,0,\
    350,200,250,0,0,0,150,300,0,0 \
    ]

gainDeckB = 100
costDeckB = \
    [
    0,0,0,0,0,0,0,0,1250,0,\
    0,0,0,1250,0,0,0,0,0,0,\
    1250,0,0,0,0,0,0,0,0,0,\
    0,1250,0,0,0,0,0,0,0,0 \
    ]

gainDeckC = 50
costDeckC = \
    [
    0,0,50,0,50,0,50,0,50,50,\
    0,25,75,0,0,0,25,75,0,50,\
    0,0,0,50,25,50,0,0,75,50,\
    0,0,0,25,25,0,75,0,50,75 \
    ]

gainDeckD = 50
costDeckD = \
    [
    0,0,0,0,0,0,0,0,0,250,\
    0,0,0,0,0,0,0,0,0,250,\
    0,0,0,0,0,0,0,0,250,0,\
    0,0,0,0,250,0,0,0,0,0 \
    ]

# 总轮数，修改轮数需修改此处
# 同时设置好每副牌的惩罚列表（如costDeckA），确保惩罚项数不小于总轮数
# 这里总轮数为10轮，惩罚项为40个，所以满足条件
# 如果需要做100轮，则惩罚矩阵列表还要扩充到100项，确保程序不会出错
expRound = 10

# csv表头
testerInfoTitle = ['Age','Gender','Education level']
recordTitle = ['Round','Deck','DcekCount','Win','Lost','Current Money']

# 自定义的QLable类，增加了鼠标单击信号
class MyQLabel(QLabel):
    button_clicked_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(MyQLabel, self).__init__(parent)
    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


class Iowa(QWidget,Ui_Iowa):
    # 界面初始化
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 先显示第一页
        self.stackedWidget.setCurrentIndex(0)
        self.showGif(self.welcomeGif,'./WelcomePage.gif')

        # 测试结果列表
        self.record = []

        # 连接信号和槽
        self.welcomeNext.clicked.connect(self.welcomeNextOnClicked)

        self.consentNext.clicked.connect(self.consentNextOnClicked)
        self.consentAgree.toggled.connect(self.consentAgreeToggled)

        self.demoNext.clicked.connect(self.demoNextOnclicked)
        self.demoAgeSpin.valueChanged.connect(self.demoAgeSpinValueChanged)
        self.demoGenderCombo.currentIndexChanged.connect(self.demoGenderComboCurrentIndexChanged)
        self.demoEducationCombo.currentIndexChanged.connect(self.demoEducationComboCurrentIndexChanged)

        self.introduceNext.clicked.connect(self.introduceNextOnClicked)

        self.gameContinue.clicked.connect(self.gameContinueOnClicked)

        self.finalMonetNext.clicked.connect(self.finalMoneyNextOnClicked)

        self.debriefQuit.clicked.connect(self.debriefQuitOnClicked)

    # 显示gif动画，这里的url为要显示gif文件路径
    def showGif(self,label,url):
        movie = QMovie(url)
        label.setMovie(movie)
        movie.start()

    # 隐藏gif动画（这里的url随意）
    def hindGif(self,label,url):
        movie = QMovie(url)
        label.setMovie(movie)
        movie.stop()

    # 设置QLabel颜色
    def setColor(self,label,colourName):
        label.setAutoFillBackground(True)
        LabelPalette = label.palette()
        LabelPalette.setColor(QPalette.WindowText, QColor(colourName))
        label.setPalette(LabelPalette)

    # 设置QTextEdit颜色
    def setTextEditColor(self, text, colourName):
        text.setAutoFillBackground(True)
        LabelPalette = text.palette()
        LabelPalette.setColor(QPalette.Text, QColor(colourName))
        text.setPalette(LabelPalette)

    #-------------------------------------------------------- welcomePage ------------------------------------------------------#
    def welcomeNextOnClicked(self):
        self.stackedWidget.setCurrentIndex(1)
        self.consentLabel.setText(consentContent)
        self.setColor(self.consentLabel,'#224b8f')
        self.consentWarn.hide()

    #-------------------------------------------------------- consentPage ------------------------------------------------------#
    # 仅当RadioButton 选择“Yes，I agree” 时，Next键按下切换到下一页，否则显示警告信息
    def consentNextOnClicked(self):
        if self.consentAgree.isChecked():
            self.stackedWidget.setCurrentIndex(2)
            self.demoAgeSpin.setValue(18)

            self.age = self.demoAgeSpin.value()
            self.gender = self.demoGenderCombo.currentText()
            self.education = self.demoEducationCombo.currentText()
            self.demoAgeWarn.setText('')
            self.demoGenderWarn.setText('')
            self.demoEducationWarn.setText('')
        else:
            self.consentWarn.setText(consentWarnning)
            self.setColor(self.consentWarn,'#FF5151')
            self.consentWarn.show()

    def consentAgreeToggled(self):
        self.consentWarn.hide()

    #----------------------------------------------------- demographicsPage ----------------------------------------------------#
    def demoNextOnclicked(self):
        # 受试者信息符合要求，跳转到下一个页面
        if self.age >= 18 and self.gender != 'Please select' and self.education != 'Please select':
            self.stackedWidget.setCurrentIndex(3)
            self.showGif(self.introduceGif,'./IntroPoker.gif')
            self.introduceContent.setText(introduceContent)
            self.introduceContent.setStyleSheet("QTextEdit{background-color:transparent;border-width:0;border-style:outset}")
            self.setTextEditColor(self.introduceContent,'#224b8f')

        # 信息不符合要求时，显示警告消息
        else:
            if self.age < 18:
                self.demoAgeWarn.setText('Age must be older than 18 years old!')
                self.setColor(self.demoAgeWarn,'#ff0000')
                self.demoAgeWarn.show()
            else:
                self.demoAgeWarn.hide()
            if self.gender == 'Please select':
                self.demoGenderWarn.setText('Must select a gender!')
                self.setColor(self.demoGenderWarn, '#ff0000')
                self.demoGenderWarn.show()
            else:
                self.demoGenderWarn.hide()
            if self.education == 'Please select':
                self.demoEducationWarn.setText('Must select a education level!')
                self.setColor(self.demoEducationWarn, '#ff0000')
                self.demoEducationWarn.show()
            else:
                self.demoEducationWarn.hide()

    # 从交互界面获取受试者信息
    def demoAgeSpinValueChanged(self):
        self.age = self.demoAgeSpin.value()

    def demoGenderComboCurrentIndexChanged(self):
        self.gender = self.demoGenderCombo.currentText()

    def demoEducationComboCurrentIndexChanged(self):
        self.education = self.demoEducationCombo.currentText()

    #------------------------------------------------------- introducePage -----------------------------------------------------#
    def introduceNextOnClicked(self):
        # 看完实验介绍后，跳转到下一个页面
        self.stackedWidget.setCurrentIndex(4)
        self.initCard()
        self.initRound()

    # --------------------------------------------------------- gamePage -------------------------------------------------------#
    # 每一轮完成后，需按“continue”键方可进入下一轮
    def gameContinueOnClicked(self):
        # 初始化下一轮
        self.initRound()
        # 恢复纸牌下方文字（“eg.deckA”）
        self.setColor(self.deckAResult, '#0000000')
        self.setColor(self.deckBResult, '#0000000')
        self.setColor(self.deckCResult, '#0000000')
        self.setColor(self.deckDResult, '#0000000')
        self.deckAResult.setText('        DeckA')
        self.deckBResult.setText('        DeckB')
        self.deckCResult.setText('        DeckC')
        self.deckDResult.setText('        DeckD')
        self.deckAResult_2.setText('')
        self.deckBResult_2.setText('')
        self.deckCResult_2.setText('')
        self.deckDResult_2.setText('')
        # 先隐藏输或赢的表情
        self.hindGif(self.gameGif,'./WinMoney.gif')
        self.selectFlag = False
        #如果测试轮数达到设定值，则跳转到下一个页面
        if self.round == expRound:
            self.stackedWidget.setCurrentIndex(5)
            # 设置下一个页面闪烁条定时器，并显示闪烁条
            self.timer = QTimer()
            self.timer.start(800)
            self.timer.timeout.connect(self.barTimer)
            self.showBar()
            # 显示最终金钱
            if self.currentTotal > 0:
                self.finalMoneyValue.setText(' +$' + str(self.currentTotal))
                self.setColor(self.finalMoneyValue,'#1d953f')
                self.showGif(self.finalMonetGif,'finalmoney-win.gif')
            else:
                self.finalMoneyValue.setText(' -$' + str(abs(self.currentTotal)))
                self.setColor(self.finalMoneyValue, '#ff0000')
                self.showGif(self.finalMonetGif, 'finalmoney-lost.gif')

    # 初始化牌堆
    def initCard(self):
        # 总轮数
        self.round = 0
        # 第几次翻某副牌
        self.deckACount = 0
        self.deckBCount = 0
        self.deckCCount = 0
        self.deckDCount = 0
        # 选定标志，防止多选，点击一副牌后，再点其他牌不会再有响应
        self.selectFlag = False
        # 初始化金钱
        self.borrow = 2000
        self.currentTotal = self.borrow
        # 可视化条显示时，像素与金钱的比例因子，可视化条随金钱数伸缩
        # 条带横向像素为700pixel，每1000刻度对应75pixel，故有以下关系
        self.axisfactor = 75/1000

        # 为了实现点击纸牌触发动作，而不是通过radio button，这里使用自定义的QLable，其中加入了鼠标点击的信号
        self.deckA = MyQLabel()
        self.deckA.setObjectName('deckA')
        self.deckB = MyQLabel()
        self.deckB.setObjectName('deckB')
        self.deckC = MyQLabel()
        self.deckC.setObjectName('deckC')
        self.deckD = MyQLabel()
        self.deckD.setObjectName('deckD')

        # 在Qt Designer中布局纸牌位置时，使用了Qt原始QLabel占位并设置了背景图片（可视化，方便布局）
        # 这里需要将原始QLabel的背景图片设为透明背景（null.png），以便在相同位置用自定义的QLable（MyQLabel）覆盖
        layoutA = QHBoxLayout()
        layoutA.addWidget(self.deckA)
        self.deckA_.setPixmap(QPixmap('./null.png'))
        self.deckA_.setLayout(layoutA)
        layoutB = QHBoxLayout()
        layoutB.addWidget(self.deckB)
        self.deckB_.setPixmap(QPixmap('./null.png'))
        self.deckB_.setLayout(layoutB)
        layoutC = QHBoxLayout()
        layoutC.addWidget(self.deckC)
        self.deckC_.setPixmap(QPixmap('./null.png'))
        self.deckC_.setLayout(layoutC)
        layoutD = QHBoxLayout()
        layoutD.addWidget(self.deckD)
        self.deckD_.setPixmap(QPixmap('./null.png'))
        self.deckD_.setLayout(layoutD)
        # 显示当前金钱，设置颜色为绿色，因为初始金钱2000，是正数
        self.currentMoney.setText(str(self.currentTotal))
        self.setColor(self.currentMoney, '#1d953f')
        # 初始化已借款状态条和当前金钱状态条
        self.gameBorrowedBar.resize(self.borrow * self.axisfactor,15)
        self.gameBorrowedBar.setStyleSheet('border-width:0px;background-color:rgb(29, 149, 63);')
        self.gameCashBar.resize(self.currentTotal * self.axisfactor,15)
        self.gameCashBar.setStyleSheet('border-width:0px;background-color:rgb(29, 149, 63);')
        self.gameCashBar.setText('')
        self.gameBorrowedBar.setText('')
        # 设置四张牌的点击信号和槽，多个信号用一个槽函数处理（通过名字区分）
        self.deckA.button_clicked_signal.connect(self.deckOnClicked)
        self.deckB.button_clicked_signal.connect(self.deckOnClicked)
        self.deckC.button_clicked_signal.connect(self.deckOnClicked)
        self.deckD.button_clicked_signal.connect(self.deckOnClicked)

    # 每一轮开始前的初始化
    def initRound(self):
        # 纸牌状态恢复成未选状态
        self.selectFlag = False
        # 纸牌图片恢复成未选图片
        card = QPixmap('./unselected.png')
        self.deckA.setPixmap(card)
        self.deckA.setScaledContents(True)
        self.deckB.setPixmap(card)
        self.deckB.setScaledContents(True)
        self.deckC.setPixmap(card)
        self.deckC.setScaledContents(True)
        self.deckD.setPixmap(card)
        self.deckD.setScaledContents(True)
        # 隐藏“continue”按钮
        self.gameContinue.hide()
        # 更新当前轮数
        self.currentRound.setText(str(self.round + 1) + ' of ' + str(expRound))

    # 纸牌被点击后的处理
    def deckOnClicked(self):
        # 如果已经有纸牌被选过了，再点任意牌都都不会有反应
        if self.selectFlag:
            return
        # 获得点击了哪一张牌
        deck = self.sender()
        # 更新牌的图片为已选图片
        card = QPixmap('./selected.png')
        deck.setPixmap(card)
        # 隐藏“Please select a card”提示，并显示“continue”按钮
        self.selectTip.hide()
        self.gameContinue.show()
        # 轮数加一
        self.round = self.round + 1
        # 本轮数据统计列表，收集：当前轮数，翻了哪一组纸牌，是这一组纸牌的第几张，赢钱数，输钱数，当前总钱数
        roundRecord = []
        roundRecord.append(self.round)
        roundRecord.append(deck.objectName())

        # 如果轮数没到设定值（如10或100），则更新显示当前钱数
        if self.round <= expRound:
            if deck.objectName() == 'deckA':
                # 牌组A被翻次数加一
                self.deckACount = self.deckACount + 1
                # 奖励数
                gain = gainDeckA
                # 惩罚数
                cost = costDeckA[self.deckACount-1]
                # 显示奖励和惩罚，奖励绿色显示，惩罚红色显示
                self.deckAResult.setText('   you win $' + str(gain))
                self.deckAResult_2.setText('   you lost $' + str(cost))
                self.setColor(self.deckAResult,'#1d953f')
                self.setColor(self.deckAResult_2, '#ff0000')
                # 牌已被选，再点任意牌将不会有反应
                self.selectFlag = True
                # 收集牌组A第几次被选择
                roundRecord.append(self.deckACount)
            if deck.objectName() == 'deckB':
                self.deckBCount = self.deckBCount + 1
                gain = gainDeckB
                cost = costDeckB[self.deckBCount - 1]
                self.deckBResult.setText('   you win $' + str(gain))
                self.deckBResult_2.setText('   you lost $' + str(cost))
                self.setColor(self.deckBResult, '#1d953f')
                self.setColor(self.deckBResult_2, '#ff0000')
                self.selectFlag = True
                roundRecord.append(self.deckBCount)
            if deck.objectName() == 'deckC':
                self.deckCCount = self.deckCCount + 1
                gain = gainDeckC
                cost = costDeckC[self.deckCCount - 1]
                self.deckCResult.setText('   you win $' + str(gain))
                self.deckCResult_2.setText('   you lost $' + str(cost))
                self.setColor(self.deckCResult, '#1d953f')
                self.setColor(self.deckCResult_2, '#ff0000')
                self.selectFlag = True
                roundRecord.append(self.deckCCount)
            if deck.objectName() == 'deckD':
                self.deckDCount = self.deckDCount + 1
                gain = gainDeckD
                cost = costDeckD[self.deckDCount - 1]
                self.deckDResult.setText('   you win $' + str(gain))
                self.deckDResult_2.setText('   you lost $' + str(cost))
                self.setColor(self.deckDResult, '#1d953f')
                self.setColor(self.deckDResult_2, '#ff0000')
                self.selectFlag = True
                roundRecord.append(self.deckDCount)

            # 计算当前金钱数并显示
            self.currentTotal = self.currentTotal + gain - cost
            self.currentMoney.setText(str(self.currentTotal))
            # 收集奖励惩罚等信息
            roundRecord.append(gain)
            roundRecord.append(cost)
            roundRecord.append(self.currentTotal)
            # 每一轮的数据写入总记录，最终结果为一轮一行
            self.record.append(roundRecord)
            # 1.更加当前钱数的正负设置字体颜色
            # 2.更新状态条
            if self.currentTotal > 0:
                self.setColor(self.currentMoney,'#1d953f')
                barWidth = self.currentTotal * self.axisfactor
                # 状态条是一个QLabel，通过调整QLabel的宽度来实现状态条伸缩
                self.gameCashBar.resize(barWidth,15)
                # 通过设置QLable的背景颜色先表示正负
                self.gameCashBar.setStyleSheet('border-width:0px;background-color:rgb(29, 149, 63);')
            else:
                self.setColor(self.currentMoney,'#ff0000')
                barWidth = abs(self.currentTotal) * self.axisfactor
                self.gameCashBar.resize(barWidth, 15)
                self.gameCashBar.move(550-barWidth,82)
                self.gameCashBar.setStyleSheet('border-width:0px;background-color:rgb(255, 0, 0);')
            # 根据有无惩罚显示不同表情
            if cost == 0:
                self.showGif(self.gameGif, './WinMoney.gif')
            else:
                self.showGif(self.gameGif, './LostMoney.gif')

    #-------------------------------------------------------- finalMoneyPage -----------------------------------------------------#
    def finalMoneyNextOnClicked(self):
        # 切换到最后一页
        self.stackedWidget.setCurrentIndex(6)
        # 在最后一个简要显示一个每一轮的结果记录，这里采用Text Edit控件来显示，当记录较多时可以滑动滑块来浏览
        string = 'Round' + '  ' + 'Deck' + '  ' + 'DcekCount' + '  ' + 'Win' + '  ' + 'Lost' + '  ' + 'Current Money' + '\n'
        # 拼接结果字符串
        for i in range(len(self.record)):
            string = string + 'round' + str(self.record[i][0]) + '  ' + self.record[i][1] + '  ' + str(self.record[i][2]) \
                     + '  ' + str(self.record[i][3]) + '  ' + str(self.record[i][4]) + '  ' + str(self.record[i][5]) + '\n'
        # 显示结果字符串
        self.debriefContent.setText(string)
        self.setTextEditColor(self.debriefContent, '#224b8f')
        self.debriefContent.setFocusPolicy(Qt.NoFocus)

    # 显示finalMoney标题上方闪烁条，采用QLable实现
    def showBar(self):
        self.finalBar.setStyleSheet('border-width:0px;background-color:rgb(255, 0, 0);')
        self.barFlag = True

    # 闪烁条定时处理函数，定时切换Bar（QLabel）的颜色
    def barTimer(self):
        if self.barFlag:
            self.finalBar.setStyleSheet('border-width:0px;background-color:rgb(29, 149, 63);')
            self.barFlag = False
        else:
            self.finalBar.setStyleSheet('border-width:0px;background-color:rgb(255, 0, 0);')
            self.barFlag = True

    #--------------------------------------------------------- debriefPage -----------------------------------------------------#
    # 最后一页，设置“Quit”按钮，按下后先将测试结果保存成csv文件，然后退出程序
    def debriefQuitOnClicked(self):
        self.saveData()
        app.exit()

    # 保存测试结果到csv文件，先保存受试者信息，再保存每轮结果
    def saveData(self):
        import csv
        testerInfo = [self.age,self.gender,self.education]
        with open('iowarecord.csv',"wt",newline='') as csvfile:
            f = csv.writer(csvfile)
            f.writerow(testerInfoTitle)
            f.writerow(testerInfo)
            f.writerow(recordTitle)
            f.writerows(self.record)

#---------------------- 主程序 ----------------------#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 实例化窗口
    window = Iowa()
    window.setWindowTitle("Iowa Gambling Test")
    window.setWindowIcon(QIcon('./iowa.png'))
    window.show()
    sys.exit(app.exec_())


