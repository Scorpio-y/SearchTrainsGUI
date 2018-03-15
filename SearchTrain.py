#-*- coding:utf-8 -*-
'''
火车票查询系统
TableWidget
'''
__author__ = 'Scorpio'
import sys
from PyQt5.QtCore import Qt,QDateTime
from PyQt5.QtWidgets import QWidget,QMessageBox,QApplication,QLabel,QTableWidget,QLineEdit,QHBoxLayout,QGridLayout,QVBoxLayout,QPushButton,QTableWidgetItem,QFrame,QDateTimeEdit
from PyQt5.QtGui import QFont,QColor,QBrush
from get_stations import stations
import warnings
import requests
class TableSheet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        #self.setWindowFlags(Qt.WindowCloseButtonHint && Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('火车票查询系统')
        #self.setGeometry(40,80,1500,720)
        #第一部分，输入出发地、目的地和日期
        controlsLayout = QGridLayout()      #栅格布局
        self.label1 = QLabel("出发地：")
        self.Editlabel1 = QLineEdit()
        self.label2 = QLabel("目的地：")
        self.Editlabel2 = QLineEdit()
        self.label3 = QLabel("乘车日期：")

        self.Editlabel3 = QDateTimeEdit()
        now = QDateTime.currentDateTime()
        #print(now)
        self.Editlabel3.setDateTime(now)
        self.Editlabel3.setDisplayFormat("yyyy-MM-dd")      #小写m为分钟
        self.Editlabel3.setCalendarPopup(True)

        self.buttonOK = QPushButton("确定")

        controlsLayout.addWidget(QLabel(""),0,0,1,6)
        self.message = QLabel("暂未查询车次信息！")
        controlsLayout.addWidget(self.message,0,7,1,4)
        
        controlsLayout.addWidget(self.label1,0,11,1,1)
        controlsLayout.addWidget(self.Editlabel1,0,12,1,2)
        controlsLayout.addWidget(QLabel(" "),0,14,1,1)
        
        controlsLayout.addWidget(self.label2,0,15,1,1)
        controlsLayout.addWidget(self.Editlabel2,0,16,1,2)
        controlsLayout.addWidget(QLabel(" "),0,18,1,1)

        controlsLayout.addWidget(self.label3,0,19,1,1)
        controlsLayout.addWidget(self.Editlabel3,0,20,1,2)
        controlsLayout.addWidget(QLabel(" "),0,22,1,1)
        
        controlsLayout.addWidget(self.buttonOK,0,23,1,1)
        controlsLayout.addWidget(QLabel(" "),0,25,1,8)

        #第二部分，显示查询到的车次信息
        horizontalHeader = ["车次","车站","时间","历时","商务座","一等座","二等座","高级软卧","软卧","动卧","硬卧","软座","硬座","无座","其他"]
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        self.table.setRowCount(0)       #初始化为0行
        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)     #不能编辑
        self.table.setSelectionBehavior(QTableWidget.SelectRows)    #选中整行
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        #self.table.setFrameShape(QFrame.HLine)#设定样式
        #self.table.setShowGrid(False) #取消网格线
        #self.table.verticalHeader().setVisible(False) #隐藏垂直表头
        #row_count = self.table.rowCount()
        #self.table.setColumnWidth(0,200)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        layout = QVBoxLayout()
        layout.addLayout(controlsLayout)
        layout.addLayout(mainLayout)
        self.setLayout(layout)
        self.buttonOK.clicked.connect(self.showMessage)
        self.showMaximized()

    def closeEvent(self, event):        #关闭时弹窗提示
        reply = QMessageBox.question(self, '警告', '查询记录不会被保存，\n确认退出？',QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def showMessage(self):      #显示查询信息
        stations_fz = dict(map(lambda t:(t[1],t[0]), stations.items()))     #反转字典
        from_s = self.Editlabel1.text()   #获取文本框内容
        f = stations[from_s]     # 通过字典转化为车站对应的缩写字母
        to_s = self.Editlabel2.text()
        t = stations[to_s]       # 通过字典转化为车站对应的缩写字母
        date = self.Editlabel3.text()
        d = str(date)
        print(d)
        print('正在查询' + from_s + '至' + to_s + '的列车...')
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=' + d + '&leftTicketDTO.from_station=' + f + '&leftTicketDTO.to_station=' + t +'&purpose_codes=ADULT'
        # print(url)
        warnings.filterwarnings("ignore")  # 这个网站是有安全警告的，这段代码可以忽略警告
        r = requests.get(url, verify=False)
        raw_trains = r.json()['data']['result']     # 获取车次信息
        num = len(raw_trains)       # 获取车次数目
        print('共查询到%d个车次信息'%num)
        self.message.setText("共查询到%d个车次信息"%num)
        i=0
        self.table.setRowCount(num)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)      #关闭水平滚动条
        for raw_train in raw_trains:
            # split分割之后得到的是一个列表
            data_list = raw_train.split("|")
            # print(data_list)
            tra_no = data_list[2]     #train_no
            from_s_no = data_list[16]   #from_station_no
            to_s_no = data_list[17]     #to_station_no
            seat_type = data_list[35]       #seat_types
            tra_date = d            #train_date
            checi = data_list[3]     # 车次
            cfd = stations_fz[data_list[6]]      #出发地，通过字典转换
            mdd = stations_fz[data_list[7]]      #目的地
            fctime = data_list[8]    # 发车时间
            ddtime = data_list[9]    # 到达时间
            lishi = data_list[10]    # 历时
            shangwuzuo = data_list[32] or "--"    # 商务座/特等座
            yidengzuo = data_list[31] or "--"     # 一等座
            erdengzuo = data_list[30] or "--"     # 二等座
            gjruanwo = data_list[21] or "--"      # 高级软卧
            ruanwo = data_list[23] or "--"        # 软卧
            dongwo = data_list[33] or "--"        # 动卧
            yingwo = data_list[28] or "--"        # 硬卧
            ruanzuo = data_list[24] or "--"       # 软座
            yingzuo = data_list[29] or "--"       # 硬座
            wuzuo = data_list[26] or "--"         # 无座
            others = data_list[22] or "--"        # 其他

            price_url = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no="+tra_no+"&from_station_no="+from_s_no+"&to_station_no="+to_s_no+"&seat_types="+seat_type+"&train_date="+tra_date
            r1 = requests.get(price_url, verify=False)
            # print(price_url)
            raw_prices = r1.json()['data']  # 获取车次信息
            if 'A1' in raw_prices.keys():           #A1:硬座
                pr_yz = raw_prices['A1']
            else:
                pr_yz = ''
            if 'A2' in raw_prices.keys():           # A2:软座
                pr_rz = raw_prices['A2']
            else:
                pr_rz = ''
            if 'A3' in raw_prices.keys():           # A3:硬卧
                pr_yw = raw_prices['A3']
            else:
                pr_yw = ''
            if 'A4' in raw_prices.keys():           # A4:软卧
                pr_rw = raw_prices['A4']
            else:
                pr_rw = ''
            if 'A6' in raw_prices.keys():           # A6:高级软卧
                pr_gjrw = raw_prices['A6']
            else:
                pr_gjrw = ''
            if 'A9' in raw_prices.keys():           # A9:商务座，特等座
                pr_swz = raw_prices['A9']
            else:
                pr_swz = ''
            if 'WZ' in raw_prices.keys():           # WZ:无座
                pr_wz = raw_prices['WZ']
            else:
                pr_wz = ''
            if 'M' in raw_prices.keys():            # M:一等座
                pr_ydz = raw_prices['M']
            else:
                pr_ydz = ''
            if 'O' in raw_prices.keys():            # O:二等座
                pr_edz = raw_prices['O']
            else:
                pr_edz = ''
            if 'F' in raw_prices.keys():            # F:动卧
                pr_dw = raw_prices['F']
            else:
                pr_dw = ''
            # print(pr_yz,pr_rz,pr_yw,pr_rw,pr_gjrw,pr_swz,pr_wz,pr_ydz,pr_edz,pr_dw)
            NewItem=QTableWidgetItem(checi)
            NewItem.setForeground(QColor(Qt.red))
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  #垂直居中
            self.table.setItem(i,0,NewItem)

            NewItem=QTableWidgetItem(cfd +'\n-\n'+mdd)
            NewItem.setFont(QFont("song", 9, QFont.Bold))
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,1,NewItem)

            NewItem=QTableWidgetItem(fctime+'\n-\n'+ddtime)
            NewItem.setFont(QFont("song", 9, QFont.Bold))
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,2,NewItem)

            NewItem=QTableWidgetItem(lishi)
            NewItem.setFont(QFont("song", 9, QFont.Bold))
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,3,NewItem)

            NewItem=QTableWidgetItem(shangwuzuo+'\n'+ pr_swz)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,4,NewItem)

            NewItem=QTableWidgetItem(yidengzuo+'\n'+ pr_ydz)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,5,NewItem)

            NewItem=QTableWidgetItem(erdengzuo+'\n'+ pr_edz)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,6,NewItem)

            NewItem=QTableWidgetItem(gjruanwo+'\n'+ pr_gjrw)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,7,NewItem)

            NewItem=QTableWidgetItem(ruanwo+'\n'+ pr_rw)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,8,NewItem)

            NewItem=QTableWidgetItem(dongwo+'\n'+ pr_dw)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,9,NewItem)

            NewItem=QTableWidgetItem(yingwo+'\n'+ pr_yw)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,10,NewItem)

            NewItem=QTableWidgetItem(ruanzuo+'\n'+ pr_rz)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,11,NewItem)

            NewItem=QTableWidgetItem(yingzuo+'\n'+ pr_yz)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,12,NewItem)

            NewItem=QTableWidgetItem(wuzuo+'\n'+ pr_wz)
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,13,NewItem)

            NewItem=QTableWidgetItem(others+'\n'+'')
            NewItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(i,14,NewItem)

            self.table.setRowHeight(i, 60)      #设置行高

            i=i+1
        #self.table.setSpan(0, 8, 2, 1)     #合并单元格
if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = TableSheet()
    table.show()
    sys.exit(app.exec_())