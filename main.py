from enum import Enum
import random


class PlayState(Enum):
    Lose = 0
    Win = 1
    Tie = 2

class Card:
    name = "Citoyen"
    def __init__(self, value = "Citoyen"):
        self.name = value

class Deck:
    def __init__(self, value = "Empereur"):
        rare = Card(value)
        civilian = Card()
        self.v = []
        self.v.append(rare)
        for x in range(0, 4):
            self.v.append(civilian)
    def removeCard(self, index):
        try:
            del self.v[index]
        except:
            pass
    def print(self):
        for x in range(len(self.v)):
            print("(%d) %s" % (x, self.v[x].name))

class Player:
    def __init__(self, value, rare = "Esclave"):
        self.name = value
        self.deck = Deck(rare)
        self.distanceRemaining = 30
        self.winnings = 0
    def print(self):
        print(self.name + "'s hand: ")
        self.deck.print()
    def cardsRemaining(self):
        return len(self.deck.v)-1
    def cardPlayed(self, index):
        if (index >= len(self.deck.v)):
            return ""
        return self.deck.v[index].name

class Game:

    def __init__(self, p1, p2):
        self.player1 = Player(p1, "Empereur")
        self.player2 = Player(p2)

    def createDecks(self, playsEmperorDeck):
        if (playsEmperorDeck):
            self.player1.deck = Deck("Empereur")
            self.player2.deck = Deck("Esclave")
        else:
            self.player1.deck = Deck("Esclave")
            self.player2.deck = Deck("Empereur")

    def displayTurn(self, r, t):
        print("\nRound: %d , Turn: %d" % (r,t+1))
        self.player1.print()
        print("La distance restant avant la ruine de %s: %d mm" % (self.player1.name, self.player1.distanceRemaining))
        print("les gains de %s: %d yen" % (self.player1.name, self.player1.winnings))

    def howMuchDoesPlayerWantsToBet(self):
        ok = False
        while not ok:
            try:
                question = "How much does " + self.player1.name + " want to bet (mm)? "
                amount = input(question)
                result = int(amount)
                ok = True
                return result
            except ValueError:
                print("Please enter an amount in millimeters.")
    def whichCardPlayerWantsToPlay(self):
        ok = False
        while not ok:
            try:
                cardsRemaining = self.player1.cardsRemaining();
                index = input("Which card does %s want to play (0 to %d)? " % (self.player1.name,  cardsRemaining))
                result = int(index)
                if (result > cardsRemaining):
                    print("Please enter a number between 0 and " + cardsRemaining.str())
                else:
                    ok = True
                    return result
            except ValueError:
                print("Please enter an index.")

    # Determine who won
    def didPlayerWin(self, c1, c2):
        k = self.player1.cardPlayed(c1)
        t = self.player2.cardPlayed(c2)
        print("%s played %s card" % (self.player1.name, self.player1.deck.v[c1].name))
        print("%s played %s card" % (self.player2.name, self.player2.deck.v[c2].name))
        if (k == "Citoyen" and t == "Citoyen"):
            return PlayState.Tie
        if ((k == "Empereur" and t == "Citoyen") or
            (k == "Citoyen" and t == "Esclave") or
            (k == "Esclave" and t == "Empereur")):
            return PlayState.Win
        if ((k == "Empereur" and t == "Esclave") or
            (k == "Esclave" and t == "Citoyen") or
            (k == "Citoyen" and t == "Empereur")):
            return PlayState.Lose

    # Do you want to play again?
    def doYouWantToPlayAgain(self):
        ok = False
        while not ok:
            try:
                question = "Tu veux jouer (Oui ou Non)? "
                answer = input(question)
                if (answer != "Oui" and answer != "Non"):
                    print("Veuillez indiquer Oui ou Non")
                else:
                    ok = True
                    return answer
            except ValueError:
                print("Please enter an index.")

    # Play turn
    def playTurn(self):
        bet = self.howMuchDoesPlayerWantsToBet()
        cardToPlay = self.whichCardPlayerWantsToPlay()
        cardToPlayByOpponent = random.randrange(0, self.player2.cardsRemaining())
        state = self.didPlayerWin(cardToPlay, cardToPlayByOpponent)
        if (state == PlayState.Win):
            winnings = bet * 100000;
            print("%s has won %d yen this turn" % (self.player1.name, winnings))
            self.player1.winnings += winnings
        elif (state == PlayState.Lose):
            if (self.player1.distanceRemaining == 0):
                print("Doom has arrived. %s's eye is lost. T_x" % (self.player1.name))
            else:
                print("%s a perdu ce turn" % (self.player1.name))
                print("Doom approaches by %dmm" % (bet))
                self.player1.distanceRemaining -= bet;
                print("Doom is %dmm away" % (self.player1.distanceRemaining))
        elif (state == PlayState.Tie):
            print("It is a tie")
        self.player1.deck.removeCard(cardToPlay)
        self.player2.deck.removeCard(cardToPlayByOpponent)
        return state

    # Play round
    def playRound(self, round, playsEmperorDeck):
        self.createDecks(playsEmperorDeck)
        endRound = False
        turn = 0
        while (not endRound):
            self.displayTurn(round, turn)
            state = self.playTurn()
            if (state == PlayState.Win):
                print(self.player1.name + " a gagne le round")
                endRound = True;
            elif (state == PlayState.Lose):
                print(self.player1.name + " a perdu le round")
                endRound = True;

            cardsRemaining1 = self.player1.cardsRemaining()
            cardsRemaining2 = self.player2.cardsRemaining()
            if (self.player1.distanceRemaining == 0):
                print(self.player1.name + " a perdu les yeux ce round")
                endRound = True
            elif (cardsRemaining1 == 0 or cardsRemaining2 == 0):
                if (cardsRemaining1 > 0):
                    print("%s a gagne plus d'un %d yen ce round" % (self.player1.name , self.player1.winnings))
                else:
                    print("%s a perdu d'un %d yen ce round" % (self.player2.name, self.player1.winnings))
                endRound = True
            turn += 1

    # Start game
    def start(self):
        print("\n=======================================")
        print("Le Jeu Carte d'Empereur")
        print("=======================================")
        endGame = False
        round = 1
        thirdRound = 1
        playEmperorDeck = True
        while (not endGame):
            self.playRound(round, playEmperorDeck)
            round += 1
            if (thirdRound == 3):
                thirdRound = 1
                playEmperorDeck = not playEmperorDeck
            else:
                thirdRound += 1
            if (round == 13):
                print("Maximum de 12 rounds")
                endGame = True
            elif self.player1.distanceRemaining == 0:
                print(self.player1.name + " a perdu le jeu")
                endGame = True
            elif self.player1.winnings >= 20000000:
                print(self.player1.name + " a gagne 200M yen!")
                endGame = True
            if (endGame == True):
                playAgain = self.doYouWantToPlayAgain()
                if (playAgain == "Oui"):
                    round = 1
                    endGame = False

        print("=======================================")
        print("Merci beaucoup de jouer au Carte d'Empereur.")
        print("=======================================")


x = Game("Edy", "Rico")
x.start()


