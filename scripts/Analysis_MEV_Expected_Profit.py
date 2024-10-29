import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    with open('../datasets/frontrunning_arbitrage.pkl','br') as f:
        frontrunning_arbitrage = pickle.load(f)
    sum_mempool_failure_extra_gas = 0
    sum_success_mempool_count = 0
    sum_failure_mempool_count = 0
    contract_data = {}
    private_tx_expected_profit = []
    mempool_tx_expected_profit = []
    DECIMAL = 10 ** 18

    for contract in frontrunning_arbitrage:
        success_private_count = len(frontrunning_arbitrage[contract]['success']['private'])
        success_mempool_count = len(frontrunning_arbitrage[contract]['success']['mempool'])
        failure_mempool_count = len(frontrunning_arbitrage[contract]['failure']['mempool'])
        if success_private_count + success_mempool_count  > 0 and failure_mempool_count > 0: # have initiated failed mempool contract
            contract_data[contract] = {}
            mempool_failure_extra_gas = sum(frontrunning_arbitrage[contract]['failure']['mempool'][tx]['gasUsed'] for tx in frontrunning_arbitrage[contract]['failure']['mempool'])
            mempool_success_rate = success_mempool_count / (success_mempool_count + failure_mempool_count)

            sum_success_mempool_count += success_mempool_count
            sum_failure_mempool_count += failure_mempool_count
            sum_mempool_failure_extra_gas += mempool_failure_extra_gas

            contract_data[contract]['mempool_failure_extra_gas'] = mempool_failure_extra_gas / failure_mempool_count
            contract_data[contract]['mempool_success_rate'] = mempool_success_rate

    other_mempool_failure_extra_gas = sum_mempool_failure_extra_gas / sum_failure_mempool_count
    other_mempool_success_rate = sum_success_mempool_count / (sum_success_mempool_count + sum_failure_mempool_count)
    
    for contract in frontrunning_arbitrage: # other contract
        if contract not in contract_data:
            contract_data[contract] = {}
            contract_data[contract]['mempool_failure_extra_gas'] = other_mempool_failure_extra_gas
            contract_data[contract]['mempool_success_rate'] = other_mempool_success_rate

    for contract in frontrunning_arbitrage:
        for tx in frontrunning_arbitrage[contract]['success']['private']:
            revenue = frontrunning_arbitrage[contract]['success']['private'][tx]['revenue']
            cost = frontrunning_arbitrage[contract]['success']['private'][tx]['cost']
            tx_profit = revenue - cost
            if tx_profit < 0:
                continue
            tx_success_rate = contract_data[contract]['mempool_success_rate']
            gas_price = frontrunning_arbitrage[contract]['success']['private'][tx]['gasPrice']
            consumed_failure_gas = contract_data[contract]['mempool_failure_extra_gas']
            expected_profit = tx_profit * tx_success_rate - gas_price * consumed_failure_gas * (1 - tx_success_rate)
            expected_profit /= DECIMAL
            private_tx_expected_profit.append(expected_profit)
            
        for tx in frontrunning_arbitrage[contract]['success']['mempool']:
            revenue = frontrunning_arbitrage[contract]['success']['mempool'][tx]['revenue']
            cost = frontrunning_arbitrage[contract]['success']['mempool'][tx]['cost']
            tx_profit = revenue - cost
            if tx_profit < 0:
                continue
            tx_success_rate = contract_data[contract]['mempool_success_rate']
            gas_price = frontrunning_arbitrage[contract]['success']['mempool'][tx]['gasPrice']
            consumed_failure_gas = contract_data[contract]['mempool_failure_extra_gas']
            expected_profit = tx_profit * tx_success_rate - gas_price * consumed_failure_gas * (1 - tx_success_rate)
            expected_profit /= DECIMAL
            mempool_tx_expected_profit.append(expected_profit)

    picture(private_tx_expected_profit,mempool_tx_expected_profit)

            
            

def picture(profits_private,profits_mempool):
    fig, ax = plt.subplots(figsize=(10,4))
    bins = [-10, -1, -0.1, -0.01, -0.001, 0, 0.001, 0.01, 0.1, 1, 10]
    ax.hist(profits_private, bins=bins, color='blue', alpha=0.5, label='Private')
    ax.hist(profits_mempool, bins=bins, color='red', alpha=0.5, label='Mempool')
    ax.set_xscale('symlog', linthresh=0.001)
    formatter = plt.FuncFormatter(lambda x, _: "{:.3g}".format(x))
    ax.xaxis.set_major_formatter(formatter) 
    ax.xaxis.get_offset_text().set_fontsize(18)
    ax.legend(fontsize=20, frameon=False)
    ax.set_ylabel('Tx Count', fontsize=24, rotation=90)
    ax.tick_params(axis='x', labelsize=18)  
    ax.tick_params(axis='y', labelsize=18)  
    plt.setp(ax.get_yticklabels(), rotation=90, va='center', ha='right') 
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=3))
    plt.tight_layout()
    plt.savefig('success_rate_expected_profit.pdf')
    plt.close()

if __name__ == "__main__":
    main()