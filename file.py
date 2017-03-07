import dicom
from dicom.dataset import Dataset, FileDataset
import dicom.uid
import datetime


def readDicomFileToNumpyArray(filename):
    file = readDicomFile(filename)

def readDicomFile(filename):
    return dicom.read_file(filename)

def saveDicomFile(filename, patientName, patientId, imageArray):
        meta = Dataset()

        #TODO set meta params

        dataSet = FileDataset(filename, {}, file_meta=meta, preamble=b"\0"*128)
        dataSet.PatientName = patientName
        dataSet.PatientId=patientId
        dataSet.is_little_endian=True
        dataSet.is_implicit_VR=True
        dataSet.ContentTime=datetime.datetime.now().strftime('%H%M%S.%f')
        dataSet.save_as(filename)