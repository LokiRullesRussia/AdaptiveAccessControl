import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# загрузка данных
pred = pd.read_csv('data/predictions_cert.csv')
cert = pd.read_csv('all_features.csv')[['user', 'potential_threat']]
df = pd.merge(pred, cert, on='user')

# бинарная классификация (атака = не GREEN)
y_true = df['potential_threat'].astype(int)
y_pred = (df['predicted_phase'] != 'GREEN').astype(int)

# матрица ошибок
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

print(f'TP={tp}, TN={tn}, FP={fp}, FN={fn}')

# тепловая карта
plt.figure(figsize=(7, 5))
sns.heatmap([[tn, fp], [fn, tp]], annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal', 'Attack'], yticklabels=['Normal', 'Attack'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300)
print('Сохранено: confusion_matrix.png')

# сравнение распределений
phases = ['GREEN', 'GRAY', 'BLACK']
true_counts = [sum(df['potential_threat'] == False),  # GREEN
               sum(df['potential_threat'] == True)]   # GRAY/BLACK
pred_counts = [sum(df['predicted_phase'] == 'GREEN'),
               sum(df['predicted_phase'] != 'GREEN')]

plt.figure(figsize=(8, 5))
x = ['Normal', 'Attack']
plt.bar(x, true_counts, alpha=0.7, label='Actual', color='blue')
plt.bar(x, pred_counts, alpha=0.7, label='Predicted', color='orange')
plt.ylabel('Count')
plt.title('Actual vs Predicted')
plt.legend()
plt.tight_layout()
plt.savefig('phase_comparison.png', dpi=300)
print('Сохранено: phase_comparison.png')