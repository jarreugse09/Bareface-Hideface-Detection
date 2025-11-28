import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt

# Actual labels
y_true = ['bareface'] * 1142 + ['hide-face'] * 1612 + ['background'] * 460

# Predicted labels
y_pred = ['bareface'] * 1016 + ['hide-face'] * 27 + ['background'] * 99 + ['bareface'] * 29 + ['hide-face'] * 1424 + ['background'] * 159 + ['bareface'] * 168 + ['hide-face'] * 292

# Classes
classes = ['bareface', 'hide-face', 'background']

# Generate the confusion matrix
cm = confusion_matrix(y_true, y_pred, labels=classes)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix', fontsize=15, pad=20)
plt.xlabel('Prediction', fontsize=11)
plt.ylabel('Actual', fontsize=11)
#Customizations
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()
plt.gca().figure.subplots_adjust(bottom=0.2)
plt.gca().figure.text(0.5, 0.05, 'Prediction', ha='center', fontsize=13)

# Print classification report
print(classification_report(y_true, y_pred, target_names=classes))

plt.show()


