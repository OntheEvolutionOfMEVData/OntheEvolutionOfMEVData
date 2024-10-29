# On the Evolution of Maximal Extractable Value in Ethereum

This repository provides the datasets and scripts created for the paper *On the Evolution of Maximal Extractable Value in Ethereum*.

## Datasets

The `datasets` folder includes the following files:

- **MEV_transactions.pkl**: A dictionary containing all detected MEV transactions along with their corresponding types, including:
  - **Arbitrage**
  - **Sandwich Attack**
  - **Multi-Layered-Burger Attack Transaction**
  - **Conjoined Sandwich Attack Transaction**
  - **Toxic Arbitrage**

- **tx_data.pkl**: A dictionary containing metadata for each transaction, such as:
  - **BlockNumber**: block number
  - **FromAddress**: initiator address
  - **ToAddress**: contract address

- **tx_profit.pkl**: A dictionary containing financial details for each transaction, including:
  - **revenue**: tx revenue, ETH(after conversion) gained from MEV activity
  - **cost**: tx fee, sum of gas fee and `coinbase.transfer`
  - **profit**: tx revenue - tx fee

- **tx_state.pkl**: A dictionary containing the status of each MEV transactions, specifying whether it is a **mempool transaction** or a **private transaction**.

- **contract_bytecode.pkl**: A dictionary containing the bytecode of potential MEV contracts.

- **frontrunning_arbitrage.pkl**: A dictionary containing 107 MEV contracts and their corresponding successful and failed front-running arbitrages (categorized as mempool and private), along with analysis-required transaction data such as gasPrice, gasUsed, cost, and revenue.


## Scripts

The `scripts` folder includes the following files:

- **GasOptimization.dl**: A datalog script for detecting private MEV contracts with address authorization logic and analyzing three gas optimization strategies. Before running, install [Gigahorse](https://github.com/nevillegrech/gigahorse-toolchain) and use `GasOptimization.dl` as the runtime datalog file. This script generates CSV files: `SenderGuard.csv` (address authorization), `MsgValue.csv` (packing data as transferred Ether), `GasSavingStart.csv` (directly jumping in the callee), and `SwapAndTransfer.csv` (calculating swap amount off-chain) with detection semantics.


- **Analysis_MEV_Activities_In_Different_Stage.py**: A script that plots the number of MEV activities in different stages.

- **Analysis_MEV_Activities_Financial_Metric.py**: A script that plots the financial metrics of MEV activities in different stages.

- **Analysis_MEV_Success_Rate.py**: A script that plots the success rate of mempool front-running arbitrages of MEV contracts.

- **Analysis_MEV_Expected_Profit.py**: A script that plots the distribution of expected profit for front-running arbitrages.


