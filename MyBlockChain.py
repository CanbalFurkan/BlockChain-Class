import Pyro4
@Pyro4.expose
class MyBlock: 
  
    # Function to initialize the node object 
    def __init__(self,transaction): 
        self.transaction = transaction  # Assign data 
        self.next = None  # Initialize next as null 
@Pyro4.expose
class MyBlockChain: 
    def __init__(self,name):  
        self.head = None
        self.chainName=name

        daemon = Pyro4.Daemon()
        Pyro4.locateNS().register(name, daemon.register(self))
        print("BSTServer is ready...")
        daemon.requestLoop()

    def push(self, transaction):  ## WORKING CORRECTLY
        new_block = MyBlock(transaction) 
        new_block.next = self.head 
        self.head =new_block

    def get_chainName(self):
        return self.chainName


    def calculateBalance(self,id):

        current = self.head
        flag=False
        total_currency=0
        while current is not None:
            current_transaction=current.transaction
            if current_transaction[0]=="CREATEACCOUNT":
                if current_transaction[1][0]==id: 
                    flag=True
                    print(total_currency)
                    print(current_transaction[1][1])
                    return total_currency+current_transaction[1][1]

            if current_transaction[0]=="TRANSFER":
                if current_transaction[1][0]==id :
                    total_currency-=current_transaction[1][2]
                elif current_transaction[1][1]==id:
                    total_currency+=current_transaction[1][2]

            if current_transaction[0]=="EXCHANGE":
                if current_transaction[1][0] == id:
                    total_currency-=current_transaction[1][3]
                elif current_transaction[1][1] == id:
                    total_currency+=current_transaction[1][3]

            current=current.next
        if flag==True:
            return total_currency
        elif flag==False:
            return flag


    def createAccount(self,amount): ## WORKİNG CORRECTLY
            current = self.head
            maxnumber=1
            print(current)
            while current is not None:
                if current.transaction[0]=="CREATEACCOUNT" :
                    maxnumber+=1
                current=current.next    
            transaction=("CREATEACCOUNT",(maxnumber,amount))
            self.push(transaction)
            return maxnumber


    def transfer(self,fromm,to,amount):
        
        sender_currency=self.calculateBalance(fromm)
        receiver_currency=self.calculateBalance(to)

        if sender_currency == False:
            return -1
        if receiver_currency == False:
            return -1
        
        if sender_currency > amount:
            if receiver_currency > abs(amount):
                transaction=("TRANSFER",(fromm,to,amount))
                self.push(transaction)
                return 1
        else :
            return -1


    def printChain(self):
        current = self.head

        while current is not None:
            print(current.transaction)
            current=current.next

    def exchange(self,fromm,to,toChain,amount):

        sender_currency=self.calculateBalance(fromm)
        receiver=toChain
        receiver_currency=receiver.calculateBalance(to)
        if sender_currency == False:
            return -1
        if receiver_currency == False:
            return -1
        if amount>0:
            if sender_currency > abs(amount):
                transaction=("EXCHANGE",(fromm,to,receiver.get_chainName(),amount))
                self.push(transaction)
                neg_amount=-1*amount
                transaction2=("EXCHANGE",(to,fromm,self.chainName,neg_amount))
                receiver.push(transaction2)
                return 1
            else: 
                return -1
        elif amount<0:
            if receiver_currency > abs(amount):
                transaction=("EXCHANGE",(fromm,to,receiver.get_chainName(),amount))
                self.push(transaction)
                neg_amount=-1*amount
                transaction2=("EXCHANGE",(to,fromm,self.chainName,neg_amount))
                receiver.push(transaction2)
                return 1
            else:
                return -1
        else :
            return -1


                





        
        



