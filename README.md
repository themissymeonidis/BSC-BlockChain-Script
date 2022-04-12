# BSC-BlockChain-Script
A blockchain script made to snipe nfts out of a spesific marketplace

THIS PROJECT IS FOR ACADEMIC PURPOSES ONLY! BE AWARE THAT USING IT MIGHT BE ILLIGAL IN YOUR COUNTRY!!!

The idea behind the project is simple, attemp to buy an nft as soon as it reaches the blockchain.

First the script will send a request to load the marketplace every 1 - 2 seconds.
Then it will scan the nft and do some calculations to examine if there is any profit.
If there is profit to be made, the script will attempt to buy the nft by sending a transaction on the BSC-Blockchain
Should the transaction fail, it will log it on the logs.txt file.
If it succeeds, it will examine the remaining balance on your wallet and calculate if it should continue running or stop.
The script will stop after it reaches a spesified balance.
Be aware that the competition is high and thus the script most likely wont be able to purchase the nft (Unless you use a Dedicated Server as a Node)

The script was made for a play 2 earn game (Thetan Arena) and the nfts are actually Heroes required to play the game.




