import numpy as np
import os

def checkpixels_par(pixel):
    dicti = {}
    rowCount = pixel[0] + 1
    colCount = pixel[1] + 1
    day_pixel = pixel[2]
    night_pixel = pixel[3]

    # with open('temp\\' + (str(os.getpid()) + '-' + str(rowCount) + '-' + str(colCount) + '.txt'), 'w') as f:
    #     f.write((str((rowCount, colCount))))

    if day_pixel[0] == 0. or np.isnan(day_pixel[0]):
        return None

    counter = 0
    # run on the bands, start from the second band in order to compare to the previous one and calc M
    for k in range(len(day_pixel) - 1):
        dayValue1 = day_pixel[k + 1]
        dayValue2 = day_pixel[k]
        nightValue1 = night_pixel[k + 1]
        nightValue2 = night_pixel[k]
        mDay = (dayValue1 - dayValue2) / ((k + 1) - k)
        mNight = (nightValue1 - nightValue2) / ((k + 1) - k)
        if (mDay > 0 > mNight) or (mDay < 0 < mNight):
            counter += 1
    specdev = (1.0 * counter / (len(day_pixel) - 1))

    if specdev > 0.70:
        keyInsert = '{0:.2f}'.format((specdev * 100) / 100)
        # dicti[keyInsert] = (rowCount, colCount)
        # dicti.setdefault(keyInsert, []).extend([])
        # dicti[keyInsert] = dicti.get(keyInsert, []) + [rowCount, colCount]
        # dicti[keyInsert] = dicti.get(keyInsert, []) + [colCount]
        ab = (keyInsert, rowCount, colCount)

        return ab
    else:
        return None
    # return dicti


