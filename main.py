import spectral
import multiprocessing
import check_pixels as ck
import os
import exports
import datetime, time


def check_block(block):
    process_pixel_result_list = []
    row_counter = 0
    start_row, day_block, night_block = block
    for row in range(start_row, start_row + day_block.shape[0]):
        # process_id = str(os.getpid())
        # text_file = open('temp\\' + process_id + ".txt", "a")
        # text = str(block) + "\r\n"
        # text_file.write(text)()
        # text_file.close
        for k in range(day_block.shape[1]):
            pixel = (row, k, day_block[row_counter, k], night_block[row_counter, k])
            a = ck.checkpixels_par(pixel)

            if a is not None:
                process_pixel_result_list.append(a)
        row_counter += 1
    return process_pixel_result_list


# def process_pixel(pixel):
#     # gets a 4 value tuple and sends it to checkpixels
#     check_pixel = ck.checkpixels_par(pixel)
#     return check_pixel

if __name__ == '__main__':
    print datetime.datetime.now()
    '''set working directory and output'''
    folder = r'D:\my tools\Desktop\ramons_trial'
    os.chdir(folder)

    ###################################

    # read the files and open meta data
    day_file = r'RamonB_D_E_78b_mosaic'
    night_file = r'RamonB_N_E_78b_mosaic'
    day_img = spectral.envi.open(day_file + '.hdr', day_file)
    night_img = spectral.envi.open(night_file + '.hdr', night_file)
    rows = day_img.shape[0]
    columns = day_img.shape[1]
    totalPixelsInImage = rows * columns
    print rows, columns

    # set a queue and start a pool of workers

    m = multiprocessing.Manager()
    # que = m.Queue()
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    rowsBlockSize = 100

    multiple_results_async = []
    for i in range(0, day_img.shape[0] - rowsBlockSize, rowsBlockSize):
    # for i in range(2200, 3000, rowsBlockSize):
        endRow = rowsBlockSize  # - 1
        day_sub = day_img[i: i + endRow, 0: day_img.shape[1]+1]
        night_sub = night_img[i: i + endRow, 0: day_img.shape[1]+1]
        sub_block = (i, day_sub, night_sub)
        print i
        multiple_results_async.append(pool.apply_async(check_block, (sub_block,)))
        save_i = i

    end_row = save_i
    print datetime.datetime.now()

    multiple_results = []
    for res in multiple_results_async:
        multiple_results.extend(res.get())
    # multiple_results = multiple_results_async
    print datetime.datetime.now()

    day_sub = day_img.read_subregion((end_row, day_img.shape[0]), (0, day_img.shape[1]))
    night_sub = night_img.read_subregion((end_row, day_img.shape[0]), (0, day_img.shape[1]))
    sub_block = (end_row, day_sub, night_sub)
    multiple_results.extend(check_block(sub_block))
    print datetime.datetime.now()
    # pool.terminate()
    # pool.join()

    dicti = {}
    # make a dictionary from the list so i can use the same export method as before
    # output = [p for p in results]
    for item in multiple_results:
        # with open('temp\\' + (str(item) + '.txt'), 'w') as f:
        #     f.write('%s:%s\n' % (str(item)))
        keyInsert = item[0]

        # print keyInsert
        # ha = item.values()
        # print ha
        # dicti.setdefault(keyInsert, []).extend(ha)
        rowCount, colCount = item[1:]
        dicti.setdefault(keyInsert, []).extend([rowCount, colCount])
    print 'done'

    # #######################################
    # a bunch of stuff to edit the output and
    # save and export
    exports.exports(dicti, folder, totalPixelsInImage)
    print datetime.datetime.now()