import pandas as pd
import numpy as np
import os


def exports(dicti, folder, totalPixelsInImage):
    path = 'AGS_par_temp'
    new_directory = folder + '\\' + path
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    vec = dicti.keys()
    vec.sort()
    tempVar3 = []
    dict2 = {}
    for element in range((len(vec) - 1), 1, -1):
        tempVar = dicti[vec[element - 1]]
        tempVar2 = dicti[vec[element]]
        tempVar.extend(tempVar2)
        dicti[vec[element - 1]] = tempVar
        numOfPixelsFound = len(dicti[vec[element]]) / 2
        percentOfPixelsFound = 1.0 * numOfPixelsFound / totalPixelsInImage
        thresh = vec[element]
        dict2[thresh] = [numOfPixelsFound, percentOfPixelsFound]
        # generate roi location file
        tempSaveName = str(vec[element])
        a = dicti[vec[element]]
        b = np.array(a[0:len(a) - 1:2])[np.newaxis]
        b = b.T
        c = np.array(a[1:len(a):2])[np.newaxis]
        c = c.T
        b = np.hstack((b, c))
        np.savetxt(new_directory + '\\' + tempSaveName + '.txt', b, fmt="%s")

    # last cast
    # generate ROI location file
    tempSaveName = str(vec[0])
    a = dicti[vec[0]]
    b = np.array(a[0:len(a) - 1:2])[np.newaxis]
    b = b.T
    c = np.array(a[1:len(a):2])[np.newaxis]
    c = c.T
    b = np.hstack((b, c))
    np.savetxt(new_directory + '\\' + tempSaveName + '.txt', b, fmt="%s")

    numOfPixelsFound = len(dicti[vec[0]]) / 2
    percentOfPixelsFound = 1.0 * numOfPixelsFound / totalPixelsInImage
    thresh = vec[0]
    dict2[str(thresh)] = [numOfPixelsFound, percentOfPixelsFound]

    # save algo results
    df = pd.DataFrame.from_dict(dict2, orient='index')
    writer = pd.ExcelWriter(new_directory + '\\' + 'output.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
