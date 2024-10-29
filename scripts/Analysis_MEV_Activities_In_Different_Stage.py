import json
import matplotlib.pyplot as plt
from collections import defaultdict
import pickle
def generate_line_chart(ax, tx_info, category, color, alpha):
    block_count = defaultdict(int)
    for tx_hash, block_number in tx_info.items():
        grouped_block_number = (block_number // 5000) * 5000
        block_count[grouped_block_number] += 1
    if category == "Mempool MEV Activity":
        del block_count[11830000]
    all_blocks, all_counts = zip(*sorted(block_count.items()))
    ax.plot(all_blocks, all_counts, linestyle='-', color=color, label=category, alpha=alpha)
    ax.set_xlabel('Block Number', fontsize=32)
    ax.set_ylabel('Number of MEV Activities', fontsize=32)
    ax.grid(True)
    plt.xticks( fontsize=24)
    plt.yticks(fontsize=24)
    ax.legend()


def main():
    fig, ax = plt.subplots(figsize=(24, 8))
    with open('../datasets/tx_state.pkl', 'rb') as f:
        tx_state = pickle.load(f)
    with open('../datasets/MEV_transactions.pkl','rb') as f:
        MEV_transactions = pickle.load(f)
    with open('../datasets/tx_data.pkl','rb') as f:
        tx_data = pickle.load(f)
    MEV_transactions = {k: v for k, v in MEV_transactions.items() if v != "Toxic Arbitrage"}
    stage_1 = {}
    stage_23_mempool = {}
    stage_23_private = {}
    merged_stage_23 = {}
    for ii in MEV_transactions:
        tx = ii.split(" ")[0]

        if tx_data[tx]['BlockNumber'] < 11834049:
            stage_1[tx] = tx_data[tx]['BlockNumber']
        else:
            if tx in tx_state and tx_state[tx] == "mempool":
                stage_23_mempool[tx] = tx_data[tx]['BlockNumber']
                merged_stage_23[tx] = tx_data[tx]['BlockNumber']
            elif tx in tx_state and tx_state[tx] == "private":
                stage_23_private[tx] = tx_data[tx]['BlockNumber']
                merged_stage_23[tx] = tx_data[tx]['BlockNumber']
    generate_line_chart(ax, stage_1, 'MEV Activity', 'brown', 0.8)
    generate_line_chart(ax, merged_stage_23, 'MEV Activity', 'brown', 0.8)
    generate_line_chart(ax, stage_23_mempool, 'Mempool MEV Activity', 'green', 0.8)
    generate_line_chart(ax, stage_23_private, 'Private MEV Activity', '#1F77B4', 0.8)
    ylim = ax.get_ylim()
    ax.set_ylim(ylim[0], ylim[1] * 1.1)  
    vertical_offset = ylim[1] * 0.02  
    ax.text(8591505, ax.get_ylim()[1] + vertical_offset, 'Stage I', ha='center', va='bottom', fontsize=32, color='black')
    ax.text(13685721.5, ax.get_ylim()[1] + vertical_offset, 'Stage II', ha='center', va='bottom', fontsize=32, color='black')
    ax.text(16768697, ax.get_ylim()[1] + vertical_offset, 'Stage III', ha='center', va='bottom', fontsize=32, color='black')
    ax.axvline(x=11834049, color='red', linestyle='--', alpha=0.8, linewidth=3, ymax=1.05, clip_on = False)  
    ax.axvline(x=15537394, color='blue', linestyle='--', alpha=0.8, linewidth=3, ymax=1.05, clip_on = False)
    ax.legend(loc='upper left', fontsize=24)
    plt.tight_layout(pad=4)
    ax.ticklabel_format(style='plain', useOffset=False)
    plt.show()

if __name__ == "__main__":
    main()