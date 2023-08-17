from dbConnection import getData
import numpy as np
import math

class test:
    def normalisasi1(self, arr):
        normal = np.zeros(arr.shape[0])
        nilMax = np.max(arr)
        nilMin = np.min(arr)
        for i in range(arr.shape[0]):
            normal[i] = (arr[i]-nilMin)/(nilMax-nilMin)
        return normal

    def normalisasi2(self,arr):
        normal = np.zeros((arr.shape[0], arr.shape[1]))
        for i in range(arr.shape[0]):
            nilMax = np.max(arr[i])
            nilMin = np.min(arr[i])
            for j in range(arr.shape[1]):
                normal[i][j] = (arr[i][j]-nilMin)/(nilMax-nilMin)

        return normal
        
    def testLgcnn(arr):
        #print(arr)
        data = np.array([arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8]])
        tes = test()
        dt_variasi = 0
        arr_variasi = np.array(getData().getVariasi())
        variasi = arr_variasi[dt_variasi][2]
        if variasi == None:
            variasi = 0.4

        kelas = 9
        ymax = 0.9
        #print(arr_variasi[dt_variasi][0])
        dataTraining = np.array(getData().getTraining(int(arr_variasi[dt_variasi][0])))
        dataTKelas = np.array(getData().getTrainingKelas(int(arr_variasi[dt_variasi][0])))
        norData = tes.normalisasi1(data)
        norTraining = tes.normalisasi2(dataTraining)

        dist = np.zeros(norTraining.shape[0])
        rbf = np.zeros(norTraining.shape[0])
        y = np.zeros((norTraining.shape[0], kelas))
        dji = np.zeros((norTraining.shape[0], kelas))
        divEffect = np.zeros((norTraining.shape[0], kelas))
        D = np.zeros(norTraining.shape[0])

        for j in range(norTraining.shape[0]):
            # distance
            arr_dist = np.zeros(norData.shape[0])

            for i in range(len(norData)):
                if i == 0:
                    arr_dist[i] = pow(abs(norData[i]-norTraining[j][i]), 2)
                else:
                    arr_dist[i] = arr_dist[i-1] + \
                        pow(abs(norData[i]-norTraining[j][i]), 2)
            dist[j] = arr_dist[-1]

            # rbf
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
                else:
                    divEffect[j][k] = divEffect[j-1][k]+(dji[j][k]*rbf[j])

            if j == 0:
                D[j] = rbf[j]
            else:
                D[j] = D[j-1]+rbf[j]

        cid = 0
        kid = 0
        for k in range(kelas):
            ck = divEffect[-1][k]/D[-1]
            if cid < ck:
                cid = ck
                kid = k
        kid = kid + 1
        data = np.append(arr,[kid])
        getData().insertHasil(data)
        return kid
