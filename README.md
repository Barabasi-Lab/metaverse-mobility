# meta-mobility

Data and code repository for metaverse mobility paper. 

The project utilizes two sources of data:

a) Virtual world:

The virtual world data comes from Decentraland (https://decentraland.org/). The software to create the metaverse is publicly accessible on Github (https://github.com/decentraland), and authorized servers use the code to render 3D objects, contents, and enable communication between users. As part of the server architecture, each server is required to post the locations of the users to dynamically update communication nodes between users across (https://docs.decentraland.org/contributor/introduction/architecture/).

We created a bot that automatically pings these servers every ten seconds to extract the precise location of each individual on the platform. The first data collection process lasted from March 15, 2022 to Aug 6, 2022, crawling data from a single server, resulting in data about 81,563 users and 110,416,682 displacements (D1). To ensure that the data is not affected by irregularities pertinent to a single server, we collect additional data from multiple data servers from Aug 7,2022 to September 19, 2022, resulting in 94,149 users and 141,226,580 movements (D2). The combined data captures the mobility of 163,770 users and their 251,643,262 movements across locations in the virtual world.

The code provided at `crawl_decentraland.py` contains the details on fetching new data. A real time (and historical) data snapshot is available at https://dcl-metrics.com/.

Variables collected:

- `peer_address` (unique identifier of the user, also connected with blockchain wallet address)
- `island_id`
- `island_center`
- `island_rad`
- `peer_id`
- `parcel_x` (parcel on x axis)
- `parcel_y` (parcel on y axis)
- `position_x` (user location on x axis)
- `position_y` (user location on y axis)
- `position_z` (user location on z axis)
- `timestamp_crawl` (Time stamp at which the data was recorded)

b) Blockchain (NFT) transactions:

Individuals can also participate in virtual economies, captured by the purchase and selling patterns of NFTs. Each NFT is associated with a specific contract, either of type ERC-721 or ERC-1155 on the Ethereum blockchain. The contracts enforce transaction rules for each NFT sale/transfer, similar to how art galleries set the royalty rates. An individual then uses the contract to purchase a NFT, similar to how collectors purchase a digital art item (NFT) from an art gallery (contract).

We track the purchasing patterns of the same individuals who also interacted in the virtual world, and collect their transaction history from the two most popular blockchains for NFTs, (a) Ethereum, the main chain and (b) Polygon, a side-chain of Ethereum that features cheaper and faster transactions.

b.a) Ethereum

We use Etherscan to extract Ethereum transactions, finding 1,165,310 NFTs from 23,827 contracts collected by 14,732 (9\% of all) users. The code to extract the data is available at `crawl_ethereum.py`.

b.b) Polygon

We use Polygonscan to extract Polygon transactions, finding 3,112,300 NFTs from 54,918 contracts by 41,870 (25\% of all) users. The code to extract the data is available at `crawl_polygon.py`.

Variables collected for blockchain data:

- `origin_acc` (unique identifier of the user who interacted with the contract, mapped with `peer_address`)
- txhash (unique identifier of the transaction)
- `blockNumber`
- `timeStamp`
- `from`
- `to`
- `gas_value`
- `gas_used`
- `contract_add` (unique identifier of the contract address)
- `token_id` (identifier of the contract e.g. FND)
- `token_name` (identifier of the contract e.g. Foundation)
- `token_symbol`
- `token_decimal`

Notes/ Future work:

- The Decentraland metaverse features a 3-dimensional (3D) layout. In fact, the data collected contains all three dimensions (x, y, and z). We do not consider the third dimension to maintain simplicity of the model. Future work could incorporate this.

- The data only considers users who have made an account and movement on the Decentraland metaverse. Indeed, there exists several other metaverses and several other blockchains (Binance, Solana, Cardano). The methdology and code used in the paper could be applied to other blockchains as well.

- We do not consider the value of purchases , i.e. the weight of transactions on a blockchain. The data included in this repository also contains the ETH/ USD value of NFT that could be incorporated in future work.
