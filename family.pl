% ================================================================
% FAMILY RELATIONSHIP KNOWLEDGE BASE
% AI Assignment - Family Chatbot
% ================================================================
% FACT TYPES (5 distinct types):
%   1. male/1       - gender fact
%   2. female/1     - gender fact
%   3. parent/2     - parent-child relationship
%   4. husband/2    - marital relationship
%   5. wife/2       - marital relationship
% ================================================================

% ----------------------------------------------------------------
% FACT TYPE 1: MALE MEMBERS
% ----------------------------------------------------------------
male(ali).
male(asad).
male(shakeel).
male(zain).
male(usman).
male(hamza).

% ----------------------------------------------------------------
% FACT TYPE 2: FEMALE MEMBERS
% ----------------------------------------------------------------
female(alia).
female(shakeela).
female(zaini).
female(laiba).
female(sana).
female(nadia).

% ----------------------------------------------------------------
% FACT TYPE 3: PARENT RELATIONSHIPS  parent(Parent, Child)
% ----------------------------------------------------------------
parent(ali,   zain).
parent(alia,  zain).
parent(alia,  zaini).
parent(shakeel, ali).
parent(shakeela, ali).
parent(shakeel, asad).
parent(shakeela, asad).
parent(asad,  laiba).
parent(sana,  laiba).
parent(asad,  hamza).
parent(sana,  hamza).
parent(usman, nadia).

% ----------------------------------------------------------------
% FACT TYPE 4: HUSBAND RELATIONSHIPS  husband(Husband, Wife)
% ----------------------------------------------------------------
husband(ali,    alia).
husband(shakeel, shakeela).
husband(asad,   sana).
husband(usman,  nadia).

% ----------------------------------------------------------------
% FACT TYPE 5: WIFE RELATIONSHIPS  wife(Wife, Husband)
% ----------------------------------------------------------------
wife(alia,      ali).
wife(shakeela,  shakeel).
wife(sana,      asad).
wife(nadia,     usman).

% ================================================================
% RULES SECTION  (30+ rules)
% ================================================================

% ----------------------------------------------------------------
% RULE 1: Father - male parent
% ----------------------------------------------------------------
father(X, Y) :-
    parent(X, Y),
    male(X).

% ----------------------------------------------------------------
% RULE 2: Mother - female parent
% ----------------------------------------------------------------
mother(X, Y) :-
    parent(X, Y),
    female(X).

% ----------------------------------------------------------------
% RULE 3: Son - male child
% ----------------------------------------------------------------
son(X, Y) :-
    parent(Y, X),
    male(X).

% ----------------------------------------------------------------
% RULE 4: Daughter - female child
% ----------------------------------------------------------------
daughter(X, Y) :-
    parent(Y, X),
    female(X).

% ----------------------------------------------------------------
% RULE 5: Sibling (helper) - shares at least one parent
% ----------------------------------------------------------------
sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \== Y.

% ----------------------------------------------------------------
% RULE 6: Brother - male sibling
% ----------------------------------------------------------------
brother(X, Y) :-
    sibling(X, Y),
    male(X).

% ----------------------------------------------------------------
% RULE 7: Sister - female sibling
% ----------------------------------------------------------------
sister(X, Y) :-
    sibling(X, Y),
    female(X).

% ----------------------------------------------------------------
% RULE 8: Spouse (helper) - husband or wife
% ----------------------------------------------------------------
spouse(X, Y) :-
    husband(X, Y).
spouse(X, Y) :-
    wife(X, Y).

% ----------------------------------------------------------------
% RULE 9: Grandparent - parent of parent
% ----------------------------------------------------------------
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

% ----------------------------------------------------------------
% RULE 10: Grandfather - male grandparent
% ----------------------------------------------------------------
grandfather(X, Y) :-
    father(X, Z),
    parent(Z, Y).

% ----------------------------------------------------------------
% RULE 11: Grandmother - female grandparent
% ----------------------------------------------------------------
grandmother(X, Y) :-
    mother(X, Z),
    parent(Z, Y).

% ----------------------------------------------------------------
% RULE 12: Grandchild (helper)
% ----------------------------------------------------------------
grandchild(X, Y) :-
    grandparent(Y, X).

% ----------------------------------------------------------------
% RULE 13: Grandson - male grandchild
% ----------------------------------------------------------------
grandson(X, Y) :-
    grandparent(Y, X),
    male(X).

% ----------------------------------------------------------------
% RULE 14: Granddaughter - female grandchild
% ----------------------------------------------------------------
granddaughter(X, Y) :-
    grandparent(Y, X),
    female(X).

% ----------------------------------------------------------------
% RULE 15: Uncle - brother of parent
% ----------------------------------------------------------------
uncle(X, Y) :-
    parent(Z, Y),
    brother(X, Z).

% ----------------------------------------------------------------
% RULE 16: Aunt - sister of parent
% ----------------------------------------------------------------
aunt(X, Y) :-
    parent(Z, Y),
    sister(X, Z).

% ----------------------------------------------------------------
% RULE 17: Cousin - child of sibling of parent
% ----------------------------------------------------------------
cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2),
    X \== Y.

% ----------------------------------------------------------------
% RULE 18: Nephew - male child of sibling
% ----------------------------------------------------------------
nephew(X, Y) :-
    parent(Z, X),
    sibling(Z, Y),
    male(X).

% ----------------------------------------------------------------
% RULE 19: Niece - female child of sibling
% ----------------------------------------------------------------
niece(X, Y) :-
    parent(Z, X),
    sibling(Z, Y),
    female(X).

% ----------------------------------------------------------------
% RULE 20: EASTERN RELATION - Chacha (Father's Brother)
% ----------------------------------------------------------------
chacha(X, Y) :-
    father(F, Y),
    brother(X, F).

% ----------------------------------------------------------------
% RULE 21: EASTERN RELATION - Phoophi (Father's Sister)
% ----------------------------------------------------------------
phoophi(X, Y) :-
    father(F, Y),
    sister(X, F).

% ----------------------------------------------------------------
% RULE 22: EASTERN RELATION - Maamu (Mother's Brother)
% ----------------------------------------------------------------
maamu(X, Y) :-
    mother(M, Y),
    brother(X, M).

% ----------------------------------------------------------------
% RULE 23: EASTERN RELATION - Khala (Mother's Sister)
% ----------------------------------------------------------------
khala(X, Y) :-
    mother(M, Y),
    sister(X, M).

% ----------------------------------------------------------------
% RULE 24: EASTERN GRANDPARENT - Dada (Paternal Grandfather)
% ----------------------------------------------------------------
dada(X, Y) :-
    father(F, Y),
    father(X, F).

% ----------------------------------------------------------------
% RULE 25: EASTERN GRANDPARENT - Dadi (Paternal Grandmother)
% ----------------------------------------------------------------
dadi(X, Y) :-
    father(F, Y),
    mother(X, F).

% ----------------------------------------------------------------
% RULE 26: EASTERN GRANDPARENT - Nana (Maternal Grandfather)
% ----------------------------------------------------------------
nana(X, Y) :-
    mother(M, Y),
    father(X, M).

% ----------------------------------------------------------------
% RULE 27: EASTERN GRANDPARENT - Nani (Maternal Grandmother)
% ----------------------------------------------------------------
nani(X, Y) :-
    mother(M, Y),
    mother(X, M).

% ----------------------------------------------------------------
% RULE 28: IN-LAW - Father-in-law
% ----------------------------------------------------------------
father_in_law(X, Y) :-
    spouse(S, Y),
    father(X, S).
father_in_law(X, Y) :-
    spouse(Y, S),
    father(X, S).

% ----------------------------------------------------------------
% RULE 29: IN-LAW - Mother-in-law
% ----------------------------------------------------------------
mother_in_law(X, Y) :-
    spouse(S, Y),
    mother(X, S).
mother_in_law(X, Y) :-
    spouse(Y, S),
    mother(X, S).

% ----------------------------------------------------------------
% RULE 30: IN-LAW - Brother-in-law
% ----------------------------------------------------------------
brother_in_law(X, Y) :-
    spouse(S, Y),
    brother(X, S).
brother_in_law(X, Y) :-
    spouse(Y, S),
    brother(X, S).

% ----------------------------------------------------------------
% RULE 31: IN-LAW - Sister-in-law
% ----------------------------------------------------------------
sister_in_law(X, Y) :-
    spouse(S, Y),
    sister(X, S).
sister_in_law(X, Y) :-
    spouse(Y, S),
    sister(X, S).

% ----------------------------------------------------------------
% RULE 32: STEP RELATIONS - Step Father
% ----------------------------------------------------------------
step_father(X, Y) :-
    mother(M, Y),
    husband(X, M),
    \+ father(X, Y).

% ----------------------------------------------------------------
% RULE 33: STEP RELATIONS - Step Mother
% ----------------------------------------------------------------
step_mother(X, Y) :-
    father(F, Y),
    wife(X, F),
    \+ mother(X, Y).

% ----------------------------------------------------------------
% RULE 34: LINEAGE - Ancestor (recursive)
% ----------------------------------------------------------------
ancestor(X, Y) :-
    parent(X, Y).
ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).

% ----------------------------------------------------------------
% RULE 35: LINEAGE - Descendant (recursive)
% ----------------------------------------------------------------
descendant(X, Y) :-
    ancestor(Y, X).

% ----------------------------------------------------------------
% RULE 36: FAMILY MEMBER - Any person in the family tree
% ----------------------------------------------------------------
family_member(X) :-
    male(X).
family_member(X) :-
    female(X).

% ================================================================
% END OF KNOWLEDGE BASE
% ================================================================
