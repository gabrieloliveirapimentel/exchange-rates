import pandas as pd
import matplotlib.pyplot as plt

# Ler o arquivo Excel
df = pd.read_excel('exchange_rates.xlsx')

# Converter a coluna 'Date' para o tipo datetime
df['Date'] = pd.to_datetime(df['Date'])

# Verificar o tipo de dados da coluna 'BRL'
if df['BRL'].dtype == 'object':
    # Se for string, fazer a substituição da vírgula por ponto e a conversão para float
    df['BRL'] = df['BRL'].str.replace(',', '.').astype(float)

# Plotar o gráfico
plt.figure(figsize=(10,6))
plt.plot(df['Date'], df['BRL'], marker='o') 
plt.title('EUR to BRL')
plt.xlabel('Date')
plt.ylabel('BRL')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()