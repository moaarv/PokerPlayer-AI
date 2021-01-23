# -*- coding: utf-8 -*-
from Client1 import *

Hand = ['As', '2s', '4s', '3s', '5s']
print("Straight flush",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['As', 'Ts', 'Ks', 'Qs', 'Js']
print("Straight flush",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['Ts', 'Js', 'Tc', 'Th', 'Td']
print("Four of a kind",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['2s', '2d', '7c', '7d', '7h']
print("Full House",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['As', '7s', 'Ts', 'Js', 'Qs']
print("flush",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['As', '2d', '4c', '3s', '5s']
print("straight",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['As', 'Td', 'Kh', 'Qd', 'Js']
print("straight",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['As', 'Ad', 'Ts', 'Ah', 'Qs']
print("three of a kind",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['Ah', '2d', 'Ts', 'As', 'Qs']
print("one pair",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ['As', 'Td', 'Ts', 'Ah', 'Qs']
print("two pair",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))
Hand = ["3h", "Qh" ,"Jc", "6s","Tc"]
print("high card",identifyHand(Hand))
print("Throws", queryCardsToThrow(Hand))

