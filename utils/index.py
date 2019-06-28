import pandas as pd
import matplotlib.pyplot as plt
import hip1_code as h1
import hip4_code as h4
import matplotlib.pyplot as plt

def main():
    h1_df = pd.DataFrame.from_dict(h1.process_hip1())
    h1_df.to_csv('reports/hip1/result.csv', index=False)
    h4_df = pd.DataFrame.from_dict(h4.process_hip4())
    h4_df.to_csv('reports/hip4/result.csv', index=False)
    
    plt.figure(figsize=(12,5))
    h1.make_chart_hip1(h1_df)
    plt.figure(figsize=(6,6))
    h4.make_chart_hip4(h4_df)

if __name__ == "__main__":
    main()