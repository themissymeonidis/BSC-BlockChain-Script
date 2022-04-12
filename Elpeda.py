from asyncio.windows_events import NULL
import requests, json
import time, random, sys
import aiohttp
import asyncio
from requests.structures import CaseInsensitiveDict
from web3 import Web3

def getException(status, error):
  file_object = open('exceptions.txt', 'a')
  file_object.write('\nStatus Code Error ---> ' + str(status))
  file_object.write('\nException Message:')
  file_object.write('\n' + str(error))
  file_object.close()

def getLog(price, tokenId, recite, profits):
  price = web3.fromWei(price, 'ether')
  file_object = open('logs.txt', 'a')
  file_object.write('\nPurchased Token ---> ' + str(tokenId) + " With Price At ---> " + str("{:.2f}".format(price)) + " Profit ---> " + str("{:.2f}".format(profits)) + " Recite ---> " + recite)
  file_object.close()

def buyItem(data, gas, profits):
  contract_address = '0x7Bf5D1dec7e36d5B4e9097B48A1B9771e6c96AA4'
  abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"address","name":"contractAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"},{"indexed":false,"internalType":"address","name":"paymentToken","type":"address"},{"indexed":false,"internalType":"address","name":"seller","type":"address"},{"indexed":false,"internalType":"address","name":"buyer","type":"address"},{"indexed":false,"internalType":"uint256","name":"fee","type":"uint256"}],"name":"MatchTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"feeToAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_nftAddress","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"address","name":"_paymentErc20","type":"address"},{"internalType":"uint256","name":"_price","type":"uint256"},{"internalType":"uint256","name":"_saltNonce","type":"uint256"}],"name":"getMessageHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address[2]","name":"addresses","type":"address[2]"},{"internalType":"uint256[3]","name":"values","type":"uint256[3]"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"ignoreSignature","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[3]","name":"addresses","type":"address[3]"},{"internalType":"uint256[3]","name":"values","type":"uint256[3]"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"matchTransaction","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"paymentTokens","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"_removedPaymentTokens","type":"address[]"}],"name":"removePaymentTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeToAddress","type":"address"}],"name":"setFeeToAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_paymentTokens","type":"address[]"}],"name":"setPaymentTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_transactionFee","type":"uint256"}],"name":"setTransactionFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transactionFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"","type":"bytes"}],"name":"usedSignatures","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
  contract = web3.eth.contract(address=contract_address, abi=abi)
  nonce = web3.eth.getTransactionCount(my_address)

  addresses = [web3.toChecksumAddress(data[0]),web3.toChecksumAddress('0x98eb46CbF76B19824105DfBCfa80EA8ED020c6f4'),web3.toChecksumAddress('0x24802247bd157d771b7effa205237d8e9269ba8a')]
  values = [int(data[1]),int(data[3]),int(data[2])]

  token_tx = contract.functions.matchTransaction(addresses, values, data[4]).buildTransaction({
        'chainId': 56, 'gas': 250000, 'gasPrice':web3.toWei(gas,'gwei'), 'nonce': nonce
  })
  sign_txn = web3.eth.account.sign_transaction(token_tx, private_key)
  tx_hash = web3.eth.send_raw_transaction(sign_txn.rawTransaction)


  print("Atempting to buy the following item from the marketplace")
  print("Owner Address --> " + web3.toChecksumAddress(data[0]))
  print("TokenId --> " + str(data[1]))
  print("Price --> " + str(data[3])) 
  print("saltNonce --> " + str(data[2]))
  print("Signature --> " + str(data[4]))
  print("recite Hash --> " + web3.toHex(tx_hash))
  print("Waiting For Transtaction Confirmation...")
  receipt = web3.eth.waitForTransactionReceipt(tx_hash)
  status = receipt["status"]
  if status == 1:
    print("Transaction Success")
    getLog(data[3], data[1], web3.toHex(tx_hash), profits)
  else:
    print("Transaction Failure")

async def getResponses(nftId):
  results = []
  headers = CaseInsensitiveDict()
  headers["Accept"] = "application/json"
  headers["Authorization"] = "Your Bearier"
  async with aiohttp.ClientSession() as session:
    tasks = [session.get("https://data.thetanarena.com/thetan/v1/items/" + nftId + "?id="  + nftId, ssl=False), session.get("https://data.thetanarena.com/thetan/v1/items/" + nftId + "/signed-signature?id="  + nftId, headers=headers)]
    responses = await asyncio.gather(*tasks)
    for response in responses:
      results.append(await response.json())
    return(results)

def getData(id):
  loop = asyncio.get_event_loop()
  data = loop.run_until_complete(getResponses(id))

  signature_data = data[1]
  general_data = data[0]
  signature = signature_data["data"]
  data_read = general_data["data"]
  owner_address = data_read["ownerAddress"]
  token_id = data_read["tokenId"]
  salt_nonce = data_read["saltNonce"]
  sale = data_read["sale"]
  price = sale["price"]
  price = price*pow(10, 10)
  return(owner_address, token_id, salt_nonce, price, signature)

def getWbnbPrice():
  url = requests.get("https://exchange.thetanarena.com/exchange/v1/currency/price/32", timeout=10)
  while(not(url.status_code == 200)):
    time.sleep(10)
    url = requests.get("https://exchange.thetanarena.com/exchange/v1/currency/price/32", timeout=10)
  
  text = url.text
  data = json.loads(text)
  wbnb_price = data['data']
  return(wbnb_price)

def getThcPrice():
  url = requests.get("https://exchange.thetanarena.com/exchange/v1/currency/price/1", timeout=10)
  while(not(url.status_code == 200)):
    time.sleep(10)
    url = requests.get("https://exchange.thetanarena.com/exchange/v1/currency/price/1", timeout=10)
  text = url.text
  data = json.loads(text)
  thc_price = data['data']
  if thc_price > 0.08 or thc_price < 0.02:
    thc_price=0.015
  return(thc_price)

def runMarket():
  global wbnb_price
  global thc_price
  flag = False
  count = 501
  exception_count = 0
  while (flag == False):
    if(exception_count == 20):
      sys.exit('Requested data from thetanarena.com encountered 20 Erros, shuting down Project Elpeda')
    if(count == 1):
      print("Fetching")
      wbnb_price = getWbnbPrice()
      thc_price = getThcPrice()
      print("Fetched THC Price --> " + str(thc_price))
      print("Fetched WBNB Price --> " + str(wbnb_price))
      count = 501
    count = count - 1
    try:
      url = requests.get("https://data.thetanarena.com/thetan/v1/nif/search?sort=Latest&batPercentMin=60&from=0&size=3", timeout=10)
      status = url.status_code
    except Exception as errorMsg:
      getException(status, errorMsg)
      exception_count = exception_count + 1
      pass
    text = url.text
    if status == 200:
      data = json.loads(text)
      for i in data['data']:
        id = i["id"]
        price = i['price']
        wbnb = price/pow(10, 8)
        price = wbnb * thc_price
        name = i["name"]
        remainingbattles = i["battleCap"]
        heroRarity = i["heroRarity"]
        if heroRarity == 0:
          profits = ((remainingbattles * 9.25 * thc_price * 0.3) + (remainingbattles * thc_price * 0.7) * 0.96) - price
          profits = profits - 2
        elif heroRarity == 1:
          profits = ((remainingbattles * 12.5 * thc_price * 0.4) + (remainingbattles * thc_price * 0.6) * 0.96) - price
          profits = profits - 5
        else:
          profits = -100
        
        if (profits > -2) & (profits < 4) & ((name in "Cluster") or (name in "Breaker") or (name in "Mary")):
          Gas = 5
          print("id ---> " + i["refId"] + " | Profit ---> " + str("{:.1f}".format(profits)) + " | Hero ---> " + name + " | ---> WORTH with Calculated Gas Price ---> " +  str(Gas))
          flag = True
          break
        elif (profits > 0) & (profits < 10) & (price < 60) & ((name in "Steel Shot") or (name in "Errand Ghost") or (name in "Serp") or (name in "Raidon")):
          Gas = 5
          print("id ---> " + i["refId"] + " | Profit ---> " + str("{:.1f}".format(profits)) + " | Hero ---> " + name + " | ---> WORTH with Calculated Gas Price ---> " +  str(Gas))
          flag = True
          break
        elif (profits > 2) & (profits < 10) & (price < 60) & ((name in "Veinka") or (name in "Destroid")):
          Gas = 5
          print("id ---> " + i["refId"] + " | Profit ---> " + str("{:.1f}".format(profits)) + " | Hero ---> " + name + " | ---> WORTH with Calculated Gas Price ---> " +  str(Gas))
          flag = True
          break
        elif (profits > 5) & (price < 60) & ((name in "Rei") or (name in "Durass") or (name in "El Dragon")):
          Gas = 5
          print("id ---> " + i["refId"] + " | Winrate(40%) Profit ---> " + str("{:.1f}".format(profits)) + " | Hero ---> " + name + " | ---> WORTH with Calculated Gas Price ---> " +  str(Gas))
          flag = True
          break
        elif (profits > 5) & (profits < 20) & (price < 60) & ((name in "Vathos") or (name in "Lucy Muffy") or (name in "Meiko") or (name in "Benjamin") or (name in "Morrod")):
          Gas = 5
          print("id ---> " + i["refId"] + " | Winrate(40%) Profit ---> " + str("{:.1f}".format(profits)) + " | Hero ---> " + name + " | ---> WORTH with Calculated Gas Price ---> " +  str(Gas))
          flag = True
          break
        else:
          print("id ---> " + i["refId"] + " | Profit ---> " + str("{:.1f}".format(profits)) + " | Hero ---> " + name)
    else:
      print("Encountered Error With Request Status Code ---> " + str(status))
        
    if(flag == False):
      wait_time = random.randint(10, 15)
      print('Waiting ' + str(wait_time/100) + ' sec')
      time.sleep(wait_time/100)

  if flag == True:
    data = getData(id)
    buyItem(data, Gas, profits)

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print('Connection ---> ' + str(web3.isConnected()) + " ---> Starting Market ")
private_key = 'Your Key'
my_address = web3.toChecksumAddress('Your Address')
wbnb_contract = '0x24802247bD157d771b7EFFA205237D8e9269BA8A'
wbnb_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINTER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"initializedCap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
token = web3.eth.contract(address = wbnb_contract, abi=wbnb_abi)
wbnb_balance = token.functions.balanceOf(my_address).call()
print("Balance ---> " + str(web3.fromWei(wbnb_balance, 'ether')) + " THC")

while (web3.fromWei(wbnb_balance, 'ether') > 1000):
  wbnb_price = getWbnbPrice()
  thc_price= getThcPrice()
  print("Fetched THC Price --> " + str(thc_price))
  print("Fetched WBNB Price --> " + str(wbnb_price))
  runMarket()
  time.sleep(60)
  wbnb_balance = token.functions.balanceOf(my_address).call()
  print("Balance ---> " + str(web3.fromWei(wbnb_balance, 'ether')) + " THC")
print("Balance Limit Reached.")
print("Shuting Project Elpeda Down Now...")
print("It's Been A Pleasure")