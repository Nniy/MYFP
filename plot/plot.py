import numpy as np
import matplotlib.pyplot as plt


data_1 = np.recfromcsv("rnn_val_acc.csv")
data_2 = np.recfromcsv("lstm_val_acc.csv")
data_3 = np.recfromcsv("run_lstm_drop_0.3-tag-val_loss.csv")


x_1 = []
y_1 = []

x_2 = []
y_2 = []

x_3 = []
y_3 = []

for i in data_1:
    x_1.append(i[1])
    y_1.append(i[2])

for i in data_2:
    x_2.append(i[1])
    y_2.append(i[2])

for i in data_3:
    x_3.append(i[1])
    y_3.append(i[2])

plt.plot(x_1, y_1)
plt.plot(x_2, y_2)
# plt.plot(x_3, y_3)

plt.title('Validation accuracy curve')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['RNN', 'LSTM', 'dropout=0.3'], loc='best')
plt.show()
