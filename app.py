import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, send_file
# from fileinput import filename
app = Flask(__name__)

formData = {}

@app.get('/')
def upload():
    return render_template('upload-excel.html')

@app.post('/comparefile')
def comparefile(): 
    uploadedExcelFile1 = request.files['SelectedExcelFile_1']
    uploadedExcelFile2 = request.files['SelectedExcelFile_2']
 
    uploadedExcelFile1.save('uploads/' + uploadedExcelFile1.filename)
    uploadedExcelFile2.save('uploads/' + uploadedExcelFile2.filename)
 
    excelFile1Metadata = pd.read_excel(uploadedExcelFile1)
    excelFile2Metadata = pd.read_excel(uploadedExcelFile2)

    result=excelFile1Metadata.values==excelFile2Metadata.values

    rows, cols = np.where(result == False)
    for item in zip(rows, cols):
        excelFile1Metadata.iloc[item[0],item[1]]='{}-->{}'.format(excelFile1Metadata.iloc[item[0],item[1]],excelFile2Metadata.iloc[item[0],item[1]])
 
    excelFile1Metadata.to_excel('uploads/ComparedFile.xlsx', index=False, header=True)
    return redirect("/download")

@app.route('/download')
def downloadFile ():
    path = "uploads/ComparedFile.xlsx"    
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)





