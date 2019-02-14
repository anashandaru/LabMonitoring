# -*- coding: utf-8 -*-
"""
Created on Wed Feb 06 11:44:09 2019

@author: My Computer
"""

import datetime
from fpdf import FPDF
import MySQLdb
import matplotlib.pyplot as plt

now = datetime.datetime.now()

def getDataList(tabel,date):
    # Open Database COnnection
    db = MySQLdb.connect('localhost','root','','labbpptkg')
    
    # Prepare a cursor object
    cursor = db.cursor()
    
    dateString = date.strftime("%Y-%m-%d")
    sql = """SELECT * FROM %s 
             WHERE CAST(waktu AS DATE) = '%s' ;"""%(tabel, dateString)
    
    try : 
        # Execute SQL
        cursor.execute(sql)
        # fetch all rows in a list of lists
        result = cursor.fetchall()
        return result

    except:
        print("error")
        return
        
def putData2table(lists,pdfO,column=2):
    if(len(lists) == 0):
        return
    
    for row in lists:
        hour = row[0].hour
        minute = row[0].minute

        if(column == 1):
            pdfO.set_xy(40+minute/10*12,108+hour*5)
        else:
            pdfO.set_xy(113+minute/10*12,108+hour*5)

        pdfO.cell(12,5,'%.2f'%(row[1]),border=1,fill=True, align ='C')
    
def plotGraph(lists,columnn=2):
    x = []
    y = []
    filename = ''
    
    for row in lists:
        x.append(row[0])
        y.append(row[1])
        
    plt.plot(x,y)
    
    if(columnn == 1):
        filename = 'suhu.png'
        plt.ylabel(u'Temperature (\N{DEGREE SIGN}C)')
    else:
        filename = 'klmb.png'
        plt.ylabel('Kelembababan (%)')

    fig = plt.gcf()
    fig.autofmt_xdate()
    fig.set_size_inches(7.2,4)
    fig.savefig(filename, dpi=100)
    plt.show()


pdf = FPDF(format='A4')

BPPTKG = 'BALAI PENYELIDIKAN DAN PENGEMBANGAN\n TEKNOLOGI KEBENCANAAN GEOLOGI\n'
PL = 'LABORATORIUM GEOKIMIA'
Lab = 'Laboratorium Petrografi'

info = 'No. Dokumen\nTanggal\nHalaman\nRevisi'

NoD = ': Form.5.3.2/Kond-Ruang\n'
tgl = ': 02-05-2017\n'
hal = ': 1 dari 1\n'
rev = ': 2'

detail = NoD + tgl + hal + rev

form = 'REKAMAN PEMANTAUAN PENGENDALIAN KONDISI RUANGAN PENGUJIAN'

pdf.set_left_margin(30)
pdf.set_top_margin(20)
pdf.set_fill_color(255,255,255)

pdf.add_page()

x = pdf.get_x()
y = pdf.get_y()

#------------ Header --------------#
pdf.set_font("Arial","B",10)
pdf.multi_cell(100,5,BPPTKG,border=0,align='C')

pdf.set_xy(x,y+10)
pdf.set_font("Arial","B",12)
pdf.multi_cell(100,5,PL,border=0, align ='C')

pdf.set_xy(x+100,y)
pdf.set_font("Arial","",8)
pdf.multi_cell(20,3.75,info,border=0, align ='L')

pdf.set_xy(x+120,y)
pdf.set_font("Arial","",8)
pdf.multi_cell(40,3.75,detail,border=0, align ='L')

pdf.rect(x,y-1,100,17)
pdf.rect(x+100,y-1,60,17)

#------------ Title --------------#
pdf.set_xy(x,y+20)
pdf.set_font("Arial","B",12)
pdf.multi_cell(160,5,form,border=0, align ='C')

pdf.set_xy(x,y+27)
pdf.set_font("Arial","",12)
pdf.multi_cell(35,5,'Nama Ruangan : ',border=0, align ='')

pdf.set_xy(x+35,y+27)
pdf.set_font("Arial","B",12)
pdf.multi_cell(80,5,Lab,border=0, align ='')

pdf.set_xy(x+35+80,y+27)
pdf.set_font("Arial","",12)
pdf.multi_cell(21,5,'Tanggal : ',border=0, align ='')

pdf.set_xy(x+35+80+21,y+27)
pdf.set_font("Arial","B",12)
pdf.multi_cell(24,5,now.strftime('%Y-%m-%d'),border=0, align ='')

#------------ Graph --------------#

plotGraph(getDataList('suhuLabPetro',now.date()),1)
plotGraph(getDataList('klmbLabPetro',now.date()),2)

pdf.set_xy(x+10,y+35)
#pdf.cell(72,40,'Grafik Suhu',border=1, align ='C')
pdf.image('suhu.png',w=72,h=40)
pdf.rect(x+10,y+35,w=72,h=40)

pdf.set_xy(x+11+72,y+35)
#pdf.cell(72,40,'Grafik Kelembaban',border=1, align ='C')
pdf.image('klmb.png',w=72,h=40)
pdf.rect(x+11+72,y+35,w=72,h=40)



#------------ Table --------------#
#pdf.set_xy(x,y+78)
#pdf.set_font("Arial","",7)
#pdf.cell(160,175,'Grafik Suhu',border=1, align ='C')
#pdf.cell(14,10,'Jam/Menit',border=1, align ='C')

########### Table Header
pdf.set_xy(x+10,y+78)
pdf.set_font("Arial","",10)
pdf.cell(72,5,u'Temperature (\N{DEGREE SIGN}C)',border=1, align ='C')
pdf.set_xy(x+11+72,y+78)
pdf.set_font("Arial","",10)
pdf.cell(72,5,u'Kelembaban (%)',border=1, align ='C')

pdf.ln()
pdf.set_xy(x+10,y+78+5)
for i in range(0,6):
    pdf.cell(12,5,str(i*10)+'m',border=1, align ='C')
    
pdf.set_xy(x+11+72,y+78+5)
for i in range(0,6):
    pdf.cell(12,5,str(i*10)+'m',border=1, align ='C')

pdf.set_xy(x,y+78+10)
for i in range(0,24):
    pdf.cell(10,5,str(i)+'h',border=1, align ='R')
    pdf.ln()
    
########### Table Data
putData2table(getDataList('suhuLabPetro',now.date()),pdf,1)
putData2table(getDataList('klmbLabPetro',now.date()),pdf,2)


#------------ Footer --------------#

pdf.set_xy(x,y+78+10+125)
pdf.multi_cell(130,10,'Keterangan : \n\n\n\n',border=1, align ='L')
pdf.set_xy(x+130,y+78+10+125)
pdf.multi_cell(30,10,'Paraf \n\n\n\n',border=1, align ='C')


pdf.output('trial.pdf','')