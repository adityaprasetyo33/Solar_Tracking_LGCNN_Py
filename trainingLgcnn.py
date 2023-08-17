from dbConnection import getData
import numpy as np
import math
#import matplotlib.pyplot as plt

class training:
    def normalisasi(self,arr):
        normal = np.zeros((arr.shape[0], arr.shape[1]))
        for i in range(arr.shape[0]):
            nilMax = np.max(arr[i])
            nilMin = np.min(arr[i])
            for j in range(arr.shape[1]):
                normal[i][j] = (arr[i][j]-nilMin)/(nilMax-nilMin)

        return normal
    
    def trainingLgcnn():
        train = training()
        dt_variasi = 0
        arr_variasi = np.array(getData().getVariasi())
        variasi = arr_variasi[dt_variasi][2]
        getData().generateDataUji(arr_variasi[dt_variasi][0])
        #print(arr_variasi)
        if variasi == None:
            variasi = 0.4

        epoch = arr_variasi[dt_variasi][1]
        # epoch = 1
        lr = 1
        iterasi = 0
        kelas = 9

        errorMax = 1
        errorLama = 0
        error = np.array([])
        errorDerivatif = 0
        ymax = 0.9

        dataTraining = np.array(getData().getTraining(arr_variasi[dt_variasi][0]))
        dataTKelas = np.array(getData().getTrainingKelas(arr_variasi[dt_variasi][0]))
        nor = train.normalisasi(dataTraining)

        while iterasi < epoch and abs(errorMax) > 0.0001:
            dist = np.zeros(nor.shape[0])
            rbf = np.zeros(nor.shape[0])
            y = np.zeros((nor.shape[0], kelas))
            dji = np.zeros((nor.shape[0], kelas))
            divEffect = np.zeros((nor.shape[0], kelas))
            b = np.zeros((nor.shape[0], kelas))
            l = np.zeros(nor.shape[0])
            D = np.zeros(nor.shape[0])
            # print(nor[iterasi])
            if iterasi > 0 and variasi + lr * errorDerivatif > 0:
                variasi = variasi + (lr * errorDerivatif)
            for j in range(nor.shape[0]):
                # distance
                arr_dist = np.zeros(nor.shape[1])

                for i in range(len(nor[iterasi])):
                    if i == 0:
                        arr_dist[i] = pow(abs(nor[iterasi][i]-nor[j][i]), 2)
                    else:
                        arr_dist[i] = arr_dist[i-1] + \
                            pow(abs(nor[iterasi][i]-nor[j][i]), 2)
                dist[j] = arr_dist[-1]

                # rbf
                if j == iterasi:
                    rbf[j] = 0
                else:
                    rbf[j] = math.exp(-1*(dist[j]/(2*(pow(variasi, 2)))))

                for k in range(kelas):
                    # y(j,i)
                    if k == dataTKelas[j]-1:
                        y[j][k] = 0.9
                    else:
                        y[j][k] = 0.1

                    # d(j,i)
                    dji[j][k] = math.exp(y[j][k]-ymax)*y[j][k]

                    # ui dan b(id)
                    if j == 0:
                        divEffect[j][k] = dji[j][k]*rbf[j]
                        b[j][k] = dji[j][k]*rbf[j]*(dist[j]/pow(variasi, 3))
                    else:
                        divEffect[j][k] = divEffect[j-1][k]+(dji[j][k]*rbf[j])
                        b[j][k] = b[j-1][k] + \
                            (dji[j][k]*rbf[j]*(dist[j]/pow(variasi, 3)))
                # denom dan l(id)
                if j == 0:
                    D[j] = rbf[j]
                    l[j] = rbf[j]*(dist[j]/pow(variasi, 3))
                else:
                    D[j] = D[j-1]+rbf[j]
                    l[j] = l[j-1]+rbf[j]*(dist[j]/pow(variasi, 3))

            cid = 0
            kid = 0
            for k in range(kelas):
                ck = divEffect[-1][k]/D[-1]
                if cid < ck:
                    cid = ck
                    kid = k
            cost = (y[iterasi][kid] * math.log(cid, 10)) + \
                (1 - y[iterasi][kid]) * math.log(1-cid, 10)
            cidDerivatif = ((2 * b[-1][kid]) - ((2 * l[-1]) * cid)) / D[-1]
            errorDerivatif = (y[iterasi][kid] * (cidDerivatif / cid)) + \
                (1 - y[iterasi][kid] * ((-cidDerivatif) / cid))

            errorMax = cost
            error = np.append(error, np.array([cost]))
            ymax = cid
            iterasi = iterasi + 1

        arr_variasi[dt_variasi][2] = variasi
        arr_variasi[dt_variasi][3] = errorMax
        arr_variasi[dt_variasi][4] = iterasi
        getData().updateVariasi(arr_variasi[dt_variasi])
