# import pandas as pd # читать таблицы
# import requests #отправлять запросы в api
# import time #делать задержку между запросами


# dataset = pd.read_csv('data/dataset.csv')
# answers = pd.read_csv('data/answers.csv')

# #адрес апи
# url = "http://127.0.0.1:8001/v1/authz"

# results = []

# #отправка запросов в цикл
# for idx, row in dataset.iterrows():
#     response = requests.post(url, json ={
#         "t": int(row['t']),
#         "d": int(row['d']),
#         "a": int(row['a']),
#         "c": int(row['c'])
#     })
#     pred = response.json()
#     results.append({
#         'user': row['user'],
#         'predicted_R': pred['riskScore'],
#         'predocted_pdase': pred['phase']
#     })

#     time.sleep(0.05)

# df_results = pd.DataFrame(results)
# df_results.to_csv('data/predictions.csv', index=False)

# print("Сохранение результата обработки в data/predictions.csv")
# print(f"Всего обработано: {len(results)} записей")

import pandas as pd
import requests
import time

# читаем данные CERT
cert = pd.read_csv('all_features.csv')

# извлекаем признаки t, d, a, c из CERT
dataset = []

for idx, row in cert.iterrows():
    # t - отклонение от рабочего времени
    t = 1 if (row['after_hours_logons'] > 0 or row['avg_after_hours_browsing_per_day'] > 0) else 0
    # d - нештатное устройство
    d = 1 if (row['distinct_pcs_used'] > 1 or row['late_hour_device_use'] > 0) else 0
    # a - нетипичное действие
    a = 1 if (row['total_files_copied'] > 10 or row['avg_potentially_malicious_urls_per_day'] > 0) else 0
    # c - количество команд (аналог - скопированные файлы, ограничиваем 10)
    c = min(row['total_files_copied'], 10)
    
    dataset.append({
        'user': row['user'],
        't': t,
        'd': d,
        'a': a,
        'c': c
    })

dataset = pd.DataFrame(dataset)

# адрес апи
url = "http://127.0.0.1:8001/v1/authz"

results = []

# отправка запросов в цикл
for idx, row in dataset.iterrows():
    response = requests.post(url, json={
        "t": int(row['t']),
        "d": int(row['d']),
        "a": int(row['a']),
        "c": int(row['c'])
    })
    pred = response.json()
    results.append({
        'user': row['user'],
        'predicted_R': pred['riskScore'],
        'predicted_phase': pred['phase']
    })
    time.sleep(0.05)

df_results = pd.DataFrame(results)
df_results.to_csv('data/predictions_cert.csv', index=False)

print("Сохранение результата обработки в data/predictions_cert.csv")
print(f"Всего обработано: {len(results)} записей")