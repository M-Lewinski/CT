import dicom
from dicom.dataset import Dataset, FileDataset
import datetime
import numpy as np


def readDicomFileToNumpyArray(filename):
    file = readDicomFile(filename)
    name = str(file[0x10,0x10].value)# Patient name format: 'Last^First^mid^pre'
    name = name.split('^')
    lastName = name[0]
    firstName = name[1]
    id = str(file[0x10, 0x20].value)    # Patient id
    birthday = str(file[0x10, 0x30].value)  # Patient birth date
    gender = str(file[0x10, 0x40].value)    # Patient sex
    birthday = birthday[0:4] + "-" + birthday[4:6] + "-" + birthday[6:8]
    date = str(file[0x08, 0x20].value)  # Study date
    time = str(file[0x08,0x30].value)   # Study time
    date = date[0:4]+"-"+date[4:6]+"-"+date[6:8]
    time = time[0:2]+":"+time[2:4]+":"+time[4:6]
    image = file.pixel_array
    return lastName, firstName, id, birthday, gender, date, time, image


def readDicomFile(filename):
    return dicom.read_file(filename)

def saveDicomFile(filename, patientName, patientId, gender, birthday, imageArray):
        meta = Dataset()
        SOPClassUID = "1.2.840.10008.5.1.4.1.1.2" # sop class UID for CT images
        meta.MediaStorageSOPClassUID = SOPClassUID
        date=datetime.datetime.now().strftime('%Y%m%d')
        time=datetime.datetime.now().strftime('%H%M%S.%f')
        randomUId = SOPClassUID + "."+date+time
        meta.MediaStorageSOPInstanceUID = randomUId
        meta.ImplementationClassUID = randomUId+"."+"1"

        #TODO set meta params

        dataSet = FileDataset(filename, {}, file_meta=meta, preamble="\0"*128)
        dataSet.PatientName = patientName
        dataSet.PatientId=patientId
        dataSet[0x10, 0x30] = birthday
        dataSet[0x10, 0x40] = gender
        dataSet.is_little_endian=True
        dataSet.is_implicit_VR=True
        dataSet.ContentDate=date
        dataSet[0x08, 0x20].value=date
        dataSet[0x08, 0x30].value=time
        dataSet.ContentTime=time
        dataSet.StudyInstanceUID = randomUId+"."+"2"
        dataSet.SeriesInstanceUID = randomUId+"."+"3"
        dataSet.SOPInstanceUID = randomUId+"."+"4"
        dataSet.SOPClassUID = "CT."+date+time

        # Image data
        dataSet.SamplesPerPixel = 1
        dataSet.PhotometricInterpretation = "MONOCHROME2" #  Pixel data represent a single monochrome image plane.
        # The minimum sample value is intended to be displayed as black after any VOI gray scale transformations have been performed.
        dataSet.PixelRepresentation = 0
        dataSet.HighBit = 15 # Most significant bit for pixel sample data. Each sample shall have the same high bit.
        dataSet.BitsStored = 16
        dataSet.BitsAllocated = 16
        dataSet.SmallestImagePixelValue = '\\x00\\x00'
        dataSet.LargestImagePixelValue = '\\xff\\xff'
        dataSet.Columns = imageArray.shape[0]
        dataSet.Rows = imageArray.shape[1]
        if imageArray.dtype != np.uint16:
            imageArray = imageArray.astype(np.uint16)
        dataSet.PixelData = imageArray.tostring()
        dataSet.save_as(filename)
