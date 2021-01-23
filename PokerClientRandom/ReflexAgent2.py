import socket
import random
import ClientBase
import copy

# IP address and port
TCP_IP = '192.168.227.140'
TCP_PORT = 5000
BUFFER_SIZE = 1024


rankValues = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"T":10,"J":11,"Q":12,"K":13,"A":14}
rankValues2 = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"T":10,"J":11,"Q":12,"K":13,"A":1}

# Agent
POKER_CLIENT_NAME = 'MoaTommy'
CURRENT_HAND = []

toThrow = []
ante = 0
handStrength = ""
playerCount = 0
playerTurn = 0


class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

def isFlush(hand):
    global toThrow
    toThrow = []
    if hand[0][1] == hand[1][1] and hand[0][1] == hand[2][1] and hand[0][1] == hand[3][1] and hand[0][1] == hand[4][1]:
        return True
    return False

def isStraight(hand):
    global toThrow
    toThrow = []
    sort1 = sorted(hand, key=lambda x:rankValues[x[0]])
    sort2 = sorted(hand, key=lambda x:rankValues2[x[0]]) 
    if rankValues[sort1[0][0]] == rankValues[sort1[1][0]]-1 and rankValues[sort1[0][0]] == rankValues[sort1[2][0]]-2  and rankValues[sort1[0][0]] == rankValues[sort1[3][0]]-3 and rankValues[sort1[0][0]] == rankValues[sort1[4][0]]-4:
        return True
    if rankValues2[sort2[0][0]] == rankValues2[sort2[1][0]]-1 and rankValues2[sort2[0][0]] == rankValues2[sort2[2][0]]-2  and rankValues2[sort2[0][0]] == rankValues2[sort2[3][0]]-3 and rankValues2[sort2[0][0]] == rankValues2[sort2[4][0]]-4:
        return True    
    return False

def isFourOfKind(hand):
    global toThrow
    toThrow = []
    countHand = {}
    for card in hand:
        if card[0] in countHand:
            countHand[card[0]] = countHand[card[0]]+1
        else:
            countHand[card[0]] = 1            
    for card in countHand:
        if countHand[card[0]] == 4:
            return True             
    return False

def isFullHouse(hand):
    global toThrow
    toThrow = []
    if isPair(hand) and isThreeOfKind(hand):
        toThrow = []
        return True    
    return False

def isPair(hand):
    global toThrow
    toThrow = []
    countHand = {}
    returnValue = False
    for card in hand:
        if card[0] in countHand:
            countHand[card[0]] = countHand[card[0]]+1
        else:
            countHand[card[0]] = 1            
    for rank in countHand:
        if countHand[rank[0]] == 2:
            returnValue = True
            for card in hand:
                if rank not in card:
                    toThrow.append(card)                                       
    return returnValue

def isTwoPair(hand):
    global toThrow
    toThrow = copy.copy(hand)
    countHand = {}
    returnValue = False
    counter = 0
    for card in hand:
        if card[0] in countHand:
            countHand[card[0]] = countHand[card[0]]+1
        else:
            countHand[card[0]] = 1            
    for rank in countHand:        
        if countHand[rank[0]] == 2:
            counter +=1
            temp = toThrow[:]
            for card in temp:
                if rank in card:
                    toThrow.remove(card)       
    if counter == 2:   
        returnValue = True          
    return returnValue


def isThreeOfKind(hand):
    global toThrow
    toThrow = []
    countHand = {}
    returnValue = False
    for card in hand:
        if card[0] in countHand:
            countHand[card[0]] = countHand[card[0]]+1
        else:
            countHand[card[0]] = 1            
    for rank in countHand:
        if countHand[rank]== 3:
            returnValue = True
            for card in hand:
                if rank not in card:
                    toThrow.append(card)                         
    return returnValue

def isHigh(hand):
    global toThrow
    toThrow = []
    sort = sorted(hand, key=lambda x:rankValues[x[0]])
    toThrow = copy.copy(hand)
    return sort[4]

def identifyHand(currentHand):
    global handStrength
    if isFlush(currentHand) and isStraight(currentHand):
        handStrength = "Very Strong"
        return "Straight Flush"
    if isFourOfKind(currentHand):
        handStrength = "Very Strong"
        return "Four of a kind"
    if isFullHouse(currentHand):
        handStrength = "Very Strong"
        return "Full House"
    if isFlush(currentHand):
        handStrength = "Very Strong"
        return "Flush"
    if isStraight(currentHand):
        handStrength = "Very Strong"
        return "Straight"
    if isThreeOfKind(currentHand):
        handStrength = "Very Strong"
        return "Three of a kind"
    if isTwoPair(currentHand):
        handStrength = "Very Strong"
        return"Two Pair"
    if isPair(currentHand):
        handStrength = "Strong"
        return "One Pair"
    else:
        handStrength = "Weak"
        return "High Card", isHigh(currentHand)
    
def lastToAct():
    if playerCount == playerTurn :
        return True
    return False
  
'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the anser must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")
    global CURRENT_HAND 
    global ante
    handtype = identifyHand(CURRENT_HAND)
    if lastToAct():
        return ClientBase.BettingAnswer.ACTION_OPEN, min(3*ante, _playersRemainingChips) 
    if isHigh(CURRENT_HAND):
        return ClientBase.BettingAnswer.ACTION_CHECK       
    else:   
        return ClientBase.BettingAnswer.ACTION_OPEN, min(3*ante,_playersRemainingChips)
    
    # Random Open Action
    #def chooseOpenOrCheck():
    #   if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
            #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
   #         return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else _minimumPotAfterOpen
   #    else:
   #         return ClientBase.BettingAnswer.ACTION_CHECK

   # return {
     #   0: ClientBase.BettingAnswer.ACTION_CHECK,
   #     1: ClientBase.BettingAnswer.ACTION_CHECK,
   # }.get(random.randint(0, 2), chooseOpenOrCheck())

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    global handStrength
    if handStrength == "Very Strong":
        return ClientBase.BettingAnswer.ACTION_ALLIN
    if handStrength == "Strong":
        if _minimumAmountToRaiseTo > _playersRemainingChips:
            return ClientBase.BettingAnswer.ACTION_ALLIN
        else:
            return ClientBase.BettingAnswer.ACTION_RAISE, max(_minimumAmountToRaiseTo,min(_maximumBet * 3, _playersRemainingChips))
    else:
        return ClientBase.BettingAnswer.ACTION_FOLD
        
        
    
    
    # Random Open Action
    #def chooseRaiseOrFold():
    #    if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
     #       return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
     #   else:
     #       return ClientBase.BettingAnswer.ACTION_FOLD
   # return {
   #     0: ClientBase.BettingAnswer.ACTION_FOLD,
        #1: ClientBase.BettingAnswer.ACTION_ALLIN,
     #   1: ClientBase.BettingAnswer.ACTION_FOLD,
     #   2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
   # }.get(random.randint(0, 3), chooseRaiseOrFold())

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    global toThrow
    print("Requested information about what cards to throw")
    print(_hand)
    identifyHand(_hand)
    toThrowStr = " "
    return toThrowStr.join(toThrow)  

# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    global playerTurn
    global playerCount
    playerTurn = 0
    playerCount = 0
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    global ante
    ante = int(_ante)
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    global playerCount
    playerCount +=1
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    global playerTurn
    playerTurn +=1
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    global playerTurn
    playerTurn +=1
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    global playerTurn
    playerTurn +=1
    print("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    global playerTurn
    playerTurn +=1
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    global playerTurn
    playerTurn +=1
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    global playerTurn
    playerTurn = 0
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    global CURRENT_HAND
    global POKER_CLIENT_NAME
    if _playerName == POKER_CLIENT_NAME:
        CURRENT_HAND = _hand  
    print("Player "+ _playerName +" hand " + str(_hand))

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")

