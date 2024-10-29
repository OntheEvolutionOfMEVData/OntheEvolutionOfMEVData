import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def main():
    with open('../datasets/frontrunning_arbitrage.pkl','br') as f:
        frontrunning_arbitrage = pickle.load(f)

    success_rate_list = []
    for contract in frontrunning_arbitrage:
        success_mempool_count = len(frontrunning_arbitrage[contract]['success']['mempool'])
        failure_mempool_count = len(frontrunning_arbitrage[contract]['failure']['mempool'])
        if success_mempool_count + failure_mempool_count  > 1000: 
            success_rate = success_mempool_count / (success_mempool_count + failure_mempool_count)
            success_rate_list.append(success_rate)
    picture(success_rate_list)

def picture(success_rates):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(success_rates, bins=np.arange(0, 1.1, 0.1), edgecolor='none', color='#FFB6C1')
    median_success_rate = np.median(success_rates)
    ax.axvline(x=median_success_rate, color='blue', linestyle='dashed', linewidth=2, label='Median')
    ax.set_ylabel('Contract Count', fontsize=24)
    ax.legend(fontsize=20, frameon=False)
    ax.tick_params(axis='x', labelsize=24)
    ax.tick_params(axis='y', labelsize=24) 
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
    plt.tight_layout()
    plt.savefig('success_rate.pdf')
    plt.close()

if __name__ == "__main__":
    main()
