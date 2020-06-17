from flask import Flask,render_template, url_for, request, redirect,json,jsonify, make_response
import pandas as pd
import csv
import numpy as np
import os
import codecs

app= Flask(__name__)

UPLOAD_FOLDER = '.\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


MASTERDATA='ajiomaster_ak1.csv'

# def transform(text_file_contents):
#     return text_file_contents.replace("=", ",")
# df = pd.read_csv(MASTERDATA)
# df['Date']=df['Date'].astype(str)
# df['OptionID']=df['OptionID'].astype(int)
# df['TradeDiscount']=df['TradeDiscount'].astype(float)
# df['CouponDiscount']=df['CouponDiscount'].astype(float)
# df['TotalDiscount']=df['TotalDiscount'].astype(float)
# df['BookedMRP']=df['BookedMRP'].astype(float)
# df['BookedRevenue']=df['BookedRevenue'].astype(float)
# df['BookedQuantity']=df['BookedQuantity'].astype(int)
# df['RGM']=df['RGM'].astype(int)
# df['GM']=df['GM'].astype(int)
# df['PredictedQuant']=df['PredictedQuant'].astype(int)
# df['OptimalDiscount']=df['OptimalDiscount'].astype(float)
# df['Segment']=df['Segment'].astype(str)
# df['Brand']=df['Brand'].astype(str)
# df['Ageing']=df['Ageing'].astype(int)
# df['Portfolio']=df['Portfolio'].astype(str)
# df['Brick']=df['Brick'].astype(str)


df = pd.read_csv(MASTERDATA)

# print(df.shape)
# print(df.dtypes)
# print(df.head())
df['BookedMRP'] = df['BookedMRP'].astype(float)
df['BookedRevenue'] = df['BookedRevenue'].astype(float)
df['RGM'] = df['RGM'].astype(float)
df['GM'] = df['GM'].astype(float)
df['OptimalDiscount'] = df['OptimalDiscount'].astype(float)
df['TradeDiscount'] = df['TradeDiscount'].astype(float)
df['CouponDiscount'] = df['CouponDiscount'].astype(float)
df['TotalDiscount'] = df['TotalDiscount'].astype(float)
df['OptionID'] = df['OptionID'].astype(str)
print(df.dtypes)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dropdown', methods=['GET', 'POST'])
def dropdown():
    if request.method == "GET":
        data ={
            "Segment":  Segment(),
            "Portfolio":  Portfolio(),
            "Brand":  Brand(),
            "Brick":  Brick()
        }
        return json.dumps(data)

def Segment():
    dffinal=df['Segment'].unique()
    col=list(dffinal)
    return col

def Portfolio():
    dffinal=df['Portfolio'].unique()
    col=list(dffinal)
    return col

def Brand():
    dffinal=df['Brand'].unique()
    col=list(dffinal)
    return col

def Brick():
    dffinal=df['Brick'].unique()
    col=list(dffinal)
    return col

Date=[]
OptionID=[]
TradeDiscount=[]
CouponDiscount=[]
TotalDiscount=[]
BookedMRP=[]	
BookedRevenue=[]	
BookedQuantity=[]	
RGM=[]	
GM=[]	
PredictedQuant=[]	
OptimalDiscount=[]

@app.route('/table',methods=['GET','POST'])
def table():
    return json.dumps(df1)

with open(MASTERDATA, 'r') as data_file:
    csv_data = csv.DictReader(data_file)

    # We don't want first line of bad data
    # next(csv_data)

    for line in csv_data:
        Date.append(f"{line['Date']}")
        OptionID.append(f"{line['OptionID']}")
        TradeDiscount.append(f"{line['TradeDiscount']}")
        CouponDiscount.append(f"{line['CouponDiscount']}")
        TotalDiscount.append(f"{line['TotalDiscount']}")
        BookedMRP.append(f"{line['BookedMRP']}")
        BookedRevenue.append(f"{line['BookedRevenue']}")
        BookedQuantity.append(f"{line['BookedQuantity']}")
        RGM.append(f"{line['RGM']}")
        GM.append(f"{line['GM']}")
        PredictedQuant.append(f"{line['PredictedQuant']}")
        OptimalDiscount.append(f"{line['OptimalDiscount']}")
    df1={
            "Date":Date,
            "OptionID":OptionID,
            "TradeDiscount":TradeDiscount,
            "CouponDiscount":CouponDiscount,
            "TotalDiscount":TotalDiscount,
            "BookedMRP":BookedMRP,
            "BookedRevenue":BookedRevenue,
            "BookedQuantity":BookedQuantity,
            "RGM":RGM,
            "GM":GM,
            "PredictedQuant":PredictedQuant,
            "OptimalDiscount":OptimalDiscount

        }
# print(df1)


filterlist=[]
@app.route('/filtervalues', methods=['GET','POST']) 
def filtervalues():
    if request.method == "POST":
        print(request.get_json())
        Segment = request.get_json()['Segment']
        Portfolio= request.get_json()['Portfolio']
        Brand= request.get_json()['Brand']
        Brick= request.get_json()['Brick']
        MRPMIN= request.get_json()['MRPMIN']
        MRPMAX= request.get_json()['MRPMAX']
        TDMIN= request.get_json()['TDMIN']
        TDMAX= request.get_json()['TDMAX']
        DOH= request.get_json()['DOH']
        Ageing= request.get_json()['Ageing']
        # print(priceSegment)
        filterlist={
            "Segment":Segment,
            "Portfolio": Portfolio,
            "Brand": Brand,
            "Brick":Brick,
            "MRPMIN":MRPMIN,
            "MRPMAX":MRPMAX,
            "TDMIN":TDMIN,
            "TDMAX":TDMAX,
            "DOH":DOH,
            "Ageing":Ageing
        }
        result=filterprod(Segment,Portfolio,Brand,Brick,MRPMIN,MRPMAX,TDMIN,TDMAX,Ageing)
        print(result)
        result=result.to_dict(orient='list')
        print(result)
    return json.dumps(result)

def filterprod(Segment,Portfolio,Brand,Brick,MRPMIN,MRPMAX,TDMIN,TDMAX,Ageing):
    df1=df
    if Segment!= '':
        df1=df1[df1['Segment']==Segment]
    if Portfolio!= '':
        df1=df1[df1['Portfolio']==Portfolio]
    if Brand!= '':
        df1=df1[df1['Brand']==Brand]
    if Brick!= '':
        df1=df1[df1['Brick']==Brick]
        print(df1)
    if MRPMIN!= '':
        print(MRPMIN)
        df1=df1[df1['BookedMRP']>float(MRPMIN)]
        print(df1)
    if MRPMAX!= '':
        df1=df1[df1['BookedMRP']<float(MRPMAX)]
        print(df1)
    if TDMIN!= '':
         df1=df1[df1['TotalDiscount']>float(TDMIN)]
    if TDMAX!= '':
         df1=df1[df1['TotalDiscount']<float(TDMAX)]
    if Ageing!= '':
        df1=df1[df1['Ageing']>float(Ageing)]

    return df1

@app.route('/datafromcsv',methods=["GET","POST"])
def datafromcsv():
    if request.method == "POST":
        # f=request.form['filename']
        # print(request.body)
        f = request.files['filename']
        # xlsx_sig = b'\x50\x4B\x05\06'
        # xls_sig = b'\x09\x08\x10\x00\x00\x06\x05\x00'

        # filenames = [
        #     ('spreadsheet.xls', 0, 512, 8),
        #     ('spreadsheet.xlsx', 2, -22, 4)]

        # for filename, whence, offset, size in filenames:
        #     with open(filename, 'rb') as f:
        #         f.seek(offset, whence) # Seek to the offset.
        #         bytes = f.read(size)   # Capture the specified number of bytes.

        #         print(codecs.getencoder('hex')(bytes))

        #         if bytes == xls_sig:
        #             msg = '"{}" is an xls.'
        #         elif bytes == xlsx_sig:
        #             msg = '"{}" is an xlsx.'
        #         else:
        #             msg = '"{}" is not an Excel document.'
        #         print(msg.format(filename))
        # print(f)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'xyz.csv'))
        datacsv=[]
        #for row in z:
        #        datacsv.append(row)
        #print(datacsv)
        with open(os.path.join(app.config['UPLOAD_FOLDER'],'xyz.csv')) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                 datacsv.append(row)
        print(datacsv)
        datacsv=[j for i in datacsv for j in i]
        dffiltered=df[df['OptionID'].isin(datacsv)]
        dffiltered=dffiltered.to_dict(orient='list')
        print(dffiltered)
        return json.dumps(dffiltered)


if __name__ == "__main__":
    app.run(debug=True)