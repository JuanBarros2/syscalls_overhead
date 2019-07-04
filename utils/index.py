#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pandas as pd
import matplotlib.pyplot as plt
import hip1_code as h1
import hip3_code as h3
import hip4_code as h4
import matplotlib.pyplot as plt

def main():
    print("Processando hipotese 1...")
    h1_df = pd.DataFrame.from_dict(h1.process_hip1()).groupby(['syscall', 'tool', 'depth']).median().reset_index()
    print("Gerando CSV de resultado")
    h1_df.to_csv('reports/hip1/result.csv', index=False)
    print("Salvando gráfico")
    plt.figure(figsize=(12,5))
    h1.make_chart_hip1(h1_df)
    print("Processando hipotese 3...")
    h3_df = pd.DataFrame.from_dict(h3.process_hip3()).groupby(['syscall', 'tool', 'depth']).median().reset_index()
    print("Gerando CSV de resultado")
    h3_df.to_csv('reports/hip3/result.csv', index=False)
    print("Salvando gráfico")
    plt.figure(figsize=(12,5))
    h3.make_chart_hip3(h3_df)
    print("Processando hipotese 4...")
    h4_df = pd.DataFrame.from_dict(h4.process_hip4()).groupby(['syscall', 'tool']).median().reset_index()
    print("Gerando CSV de resultado")
    h4_df.to_csv('reports/hip4/result.csv', index=False)
    print("Salvando gráfico")
    plt.figure(figsize=(6,6))
    h4.make_chart_hip4(h4_df)

if __name__ == "__main__":
    main()