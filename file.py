import dicom
from dicom.dataset import Dataset, FileDataset
import datetime
import numpy as np
import skimage


def readDicomFileToNumpyArray(filename):
    file = readDicomFile(filename)
    name = str(file.PatientName)
    name = name.split('^')
    lastName = name[0]
    firstName = name[1]
    id = str(file.PatientID)
    birthday = str(file.PatientBirthDate)
    birthday = birthday[0:4] + "-" + birthday[4:6] + "-" + birthday[6:8]
    gender = str(file.PatientSex)
    date = str(file.StudyDate)  # Study date
    time = str(file.StudyTime)   # Study time
    date = date[0:4]+"-"+date[4:6]+"-"+date[6:8]
    time = time[0:2]+":"+time[2:4]+":"+time[4:6]
    image = file.pixel_array
    return lastName, firstName, id, birthday, gender, date, time, image


def readDicomFile(filename):
    return dicom.read_file(filename)

def saveDicomFile(filename, patientName, patientId, gender, birthday, imageArray, transpose=False):

    meta = Dataset()
    SOPClassUID = "1.2.840.10008.5.1.4.1.1.2" # sop class UID dla obrazow CT
    meta.MediaStorageSOPClassUID = SOPClassUID  # Wygenerowany unikalny UID
    date=datetime.datetime.now().strftime('%Y%m%d') # Obecny czas
    time=datetime.datetime.now().strftime('%H%M%S.%f') # Obecny czas
    randomUId = SOPClassUID + "."+date+time # Wygenerowany unikalny UID
    meta.MediaStorageSOPInstanceUID = randomUId # Wygenerowany unikalny UID
    meta.ImplementationClassUID = randomUId+"."+"1" # Wygenerowany unikalny UID

    dataSet = FileDataset(filename, {}, file_meta=meta, preamble=b"\0"*128) # Utworzenie obiektu DICOM
    dataSet.PatientName = patientName   # Imie pacjenta
    dataSet.PatientID=patientId # Id pacjenta
    dataSet.PatientBirthDate = birthday # Data urodzenia pacjenta
    dataSet.PatientSex = gender # Plec pacjenta
    dataSet.is_little_endian=True
    dataSet.is_implicit_VR=True
    dataSet.ContentDate = date  # Czas utworzenia pliku (YYYY:MM:DD)
    dataSet.StudyDate = date    # Czas ostatniego otworzenia obrazu (YYYY-MM-DD)
    dataSet.StudyTime = time    # Czas ostatniego otworzenia obrazu (HH:MM:SS)
    dataSet.ContentTime=time    # Czas utworzenia pliku (HH:MM:SS)
    dataSet.StudyInstanceUID = randomUId+"."+"2"   # Wygenerowany unikalny UID
    dataSet.SeriesInstanceUID = randomUId+"."+"3"   # Wygenerowany unikalny UID
    dataSet.SOPInstanceUID = randomUId+"."+"4"   # Wygenerowany unikalny UID
    dataSet.SOPClassUID = "CT."+date+time   # Wygenerowany unikalny UID

    dataSet.SamplesPerPixel = 1 # Liczba kanałów. 1 - dla skali szarosci
    dataSet.PhotometricInterpretation = "MONOCHROME2" # MONOCHROE - obraz jest w skali szarości, 2 - maksymalna wartosc wskazuje kolor bialy
    dataSet.PixelRepresentation = 0 # 0 - wartosci sa tylko dodatnie (unsigned) 1 - wartosci sa tez ujemne
    dataSet.HighBit = 15    # Najważniejszy bit w pliku z obrazem
    dataSet.BitsStored = 16 # Liczba bitow na jedna wartosc w obrazie
    dataSet.BitsAllocated = 16  # Liczba bitow na jedna wartosc ktora jest zaalokowana dla obrazu
    dataSet.SmallestImagePixelValue = b'\\x00\\x00' # Wskazanie minimalnej wartosci dla kanalu
    dataSet.LargestImagePixelValue = b'\\xff\\xff'  # Wskazanie maksymalnej wartosci dla kanalu
    dataSet.Rows = imageArray.shape[1]  # Liczba wierszy
    dataSet.Columns = imageArray.shape[0]   # Liczba kolumn
    if imageArray.dtype != np.uint16:   # Sprawdzenie czy wartosci sa w przedziale [0,255]
        imageArray = skimage.img_as_uint(imageArray)    # Zamiana na wartosci w przedziale [0,255]
        if transpose == True:   # Zamiana wierszy i kolumn (opcjonalne)
            dataSet.Rows = imageArray.shape[0]
            dataSet.Columns = imageArray.shape[1]
    dataSet.PixelData = imageArray.tostring()   # Zapisanie obrazu
    dataSet.save_as(filename)   # Zapisanie pliku na dysku

