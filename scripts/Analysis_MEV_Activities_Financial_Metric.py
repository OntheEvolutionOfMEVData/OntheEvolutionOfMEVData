import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import pickle


def get_list(infoDict, tag):
    _list = []
    for ii in infoDict:
        if tag == "profit" or tag == "revenue":
            _list.append(infoDict[ii][tag] / 10 ** 18)
        else:
            if int(infoDict[ii]["revenue"]) <= 0:
                _list.append(0)
            else:
                _list.append(int(infoDict[ii]["profit"]) / int(infoDict[ii]["revenue"]))
    return _list

def generate_boxplot(ax, data, ylabel,colors):
    bp = ax.boxplot(data, patch_artist=True, showfliers=False, vert=False)
    ax.set_yticklabels(['Mempool', 'Private', 'Mempool', 'Private'], rotation=90, va='center', ha='right')
    ax.set_xlabel(ylabel, fontsize=30)
    ax.tick_params(axis='x', which='major', labelsize=24)  
    ax.tick_params(axis='y', which='major', labelsize=30)  
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=4))
    if ylabel == "Profit Margin(%)":
        formatter = FuncFormatter(lambda y, _: '{:.0%}'.format(y))
        ax.xaxis.set_major_formatter(formatter)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    plt.setp(bp['medians'], color='black')
    ax.axhline(2.5, color='black', linestyle='--',alpha=0.8, linewidth=3, xmax=1.05, clip_on = False)
    xlim = ax.get_xlim()
    horizontal_offset = xlim[1] * 0.02  
    ax.text(xlim[1] + horizontal_offset, 3.5, 'Stage II', ha='left', va='center', fontsize=30, color='black',rotation=90)
    ax.text(xlim[1] + horizontal_offset, 1.5, 'Stage III', ha='left', va='center', fontsize=30, color='black',rotation=90)

def main():
    after_mempool = {}
    after_private = {}
    before_mempool = {}
    before_private = {}
    with open('../datasets/tx_profit.pkl','rb') as f:
        tx_profit = pickle.load(f)
    with open('../datasets/tx_data.pkl','rb') as f:
        tx_data = pickle.load(f)
    with open('../datasets/tx_state.pkl','rb') as f:
        tx_state = pickle.load(f)
    for tx_hash in  tx_profit:
        if tx_data[tx_hash]['BlockNumber'] >= 11834049 and tx_data[tx_hash]['BlockNumber'] <= 15537393:
            if tx_hash in tx_state and tx_state[tx_hash] == "mempool":
                before_mempool[tx_hash] = tx_profit[tx_hash]
            if tx_hash in tx_state and tx_state[tx_hash] == "private":
                before_private[tx_hash] = tx_profit[tx_hash]
        if tx_data[tx_hash]['BlockNumber'] > 15537393:
            if tx_hash in tx_state and tx_state[tx_hash] == "mempool":
                after_mempool[tx_hash] = tx_profit[tx_hash]
            if tx_hash in tx_state and tx_state[tx_hash] == "private":
                after_private[tx_hash] = tx_profit[tx_hash]


    colors = ['green', '#1f77b4', 'green', '#1f77b4']   
    fig1, ax1 = plt.subplots(figsize=(5, 10))
    profit_data = [get_list(x, "profit") for x in [after_mempool, after_private, before_mempool, before_private]]
    generate_boxplot(ax1, profit_data, 'Profit(ETH)',colors)
    plt.tight_layout()
    plt.savefig('Finance_A.pdf')
    plt.close()


    fig2, ax2 = plt.subplots(figsize=(5, 10))
    profit_margin_data = [get_list(x, "profit margin") for x in [after_mempool, after_private, before_mempool, before_private]]
    generate_boxplot(ax2, profit_margin_data, 'Profit Margin(%)',colors)
    plt.tight_layout()
    plt.savefig('Finance_B.pdf')
    plt.close()



    fig3, ax3 = plt.subplots(figsize=(5, 10))
    revenue_data = [get_list(x, "revenue") for x in [after_mempool, after_private, before_mempool, before_private]]
    generate_boxplot(ax3, revenue_data, 'Revenue(ETH)',colors)
    plt.tight_layout()
    plt.savefig('Finance_C.pdf')
    plt.close()

if __name__ == "__main__":
    main()


