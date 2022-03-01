%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% File: warehouse.lp
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sort and Object Declaration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
boolean(t;f).
move(-1,0; 1,0; 0,-1; 0,1).

% Get the cells (nodes) in the grid
cell(X,Y) :- init(object(node,N), value(at,pair(X,Y))).
highway(X,Y) :- init(object(highway,N), value(at,pair(X,Y))).
pickStation(P,X,Y) :- init(object(pickingStation,P), value(at,pair(X,Y))).

% Get the lists of robots, shelves, orders, and products
robot(R) :- init(object(robot,R), value(at, pair(X,Y))).
shelf(S) :- init(object(shelf,S), value(at, pair(X,Y))).
order(O) :- init(object(order,O),value(line,pair(I,U))).
product(I) :- init(object(product,I),value(on,pair(S,U))).

% Get shelf inventory and order information
productRemaining(S,I,U,0) :- init(object(product,I),value(on,pair(S,U))).
orderRemaining(O,I,U,0) :- init(object(order,O),value(line,pair(I,U))).
orderTo(O,P) :- init(object(order,O),value(pickingStation,P)).

% Get the initial location of each robot and shelf
locRobot(R,X,Y,0) :- init(object(robot,R), value(at, pair(X,Y))).
locShelf(S,X,Y,0) :- init(object(shelf,S), value(at, pair(X,Y))).

% Set each robot so that it is initially NOT holding ANY shelf
isHolding(R,S,f,0) :- robot(R), shelf(S).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% State Description
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% No two robots can occupy the same cell
:- locRobot(R1,X,Y,T), locRobot(R2,X,Y,T), R1!=R2.

% No two shelves can occupy the same cell
:- locShelf(S1,X,Y,T), locShelf(S2,X,Y,T), S1!=S2.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Effect and Preconditions of Action
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Output syntax conversion
occurs(object(robot,R),move(DX,DY),T) :- moveRobot(R,DX,DY,T).

%%%%%%%%% Effect of Moving a Robot %%%%%%%%%
locRobot(R,X+DX,Y+DY,T+1) :- moveRobot(R,DX,DY,T), locRobot(R,X,Y,T).

% If a robot is holding a shelf, the shelf moves with the robot
locShelf(S,X+DX,Y+DY,T+1) :- moveRobot(R,DX,DY,T),
                             isHolding(R,S,t,T), locRobot(R,X,Y,T).

% The robot cannot move to a cell that is not a location (outside the grid)
:- moveRobot(R,DX,DY,T), locRobot(R,X,Y,T),
   not cell(X+DX,Y+DY).

% no two robots can switch cells
:- locRobot(R1,X1,Y1,T-1), locRobot(R2,X2,Y2,T-1),
   locRobot(R1,X2,Y2,T), locRobot(R2,X1,Y1,T), R1!=R2.

% limit concurrency: the number of actions (A) [occurs(...A...)] per
% time step is limited by the number of robots (NR).
%:- not {occurs(object(robot,R),A,T)}NR,
%   NR = #count{R: robot(R)}, T = 0..m-1.

% limit concurrency: the same robot cannot move and pickup at the same time step
:- moveRobot(R,DX,DY,T), pickupShelf(R,S,T).

% limit concurrency: the same robot cannot move and putdown at the same time step
:- moveRobot(R,DX,DY,T), putdownShelf(R,S,T).

% limit concurrency: the same robot cannot putdown and pickup at the same time step
:- putdownShelf(R,S,T), pickupShelf(R,S,T).

% limit concurrency: the same robot cannot move and deliver at the same time step
:- moveRobot(R,DX,DY,T), deliverShelf(R,S,I,U,O,T).

% limit concurrency: the same robot cannot pickup and deliver at the same time step
:- pickupShelf(R,S,T), deliverShelf(R,S,I,U,O,T).

% limit concurrency: the same robot cannot putdown and deliver at the same time step
:- putdownShelf(R,S,T), deliverShelf(R,S,I,U,O,T).


%%%%%%% Effect of Picking up a Shelf %%%%%%%
occurs(object(robot,R),pickup,T) :- pickupShelf(R,S,T).
isHolding(R,S,t,T+1) :- pickupShelf(R,S,T).

% a robot holding a shelf cannot perform a pickup action
:- pickupShelf(R1,S,T), isHolding(R2,S,t,T), R1==R2.

% there must be a robot and a shelf in the same location
:- pickupShelf(R,S,T), locRobot(R,X1,Y1,T), locShelf(S,X2,Y2,T), cell(X1,Y1) != cell(X2,Y2).


%%%%%% Effect of Putting Down a Shelf %%%%%%
occurs(object(robot,R),putdown,T) :- putdownShelf(R,S,T).
isHolding(R,S,f,T+1) :- putdownShelf(R,S,T).

% a shelf cannot be put down unless one is being held
:- putdownShelf(R,S,T), isHolding(R,S,f,T).

% no shelf can be put down on a highway cell
:- putdownShelf(R,S,T), locRobot(R,X,Y,T), highway(X,Y).


%%%%%%% Effect of Delivering a Shelf %%%%%%%
occurs(object(robot,R),deliver(O,I,U),T) :- deliverShelf(R,S,I,U,O,T).

% reduce the number of units needed to fulfill the order by the number of delivered units
orderRemaining(O,I,U3,T) :- deliverShelf(_,_,I,U1,O,T), orderRemaining(O,I,U2,T-1), U3=U2-U1, U3 >= 0.


% a delivery must consist of at least one unit
:- deliverShelf(_,_,_,U,_,_), U<1.


% number of units required for an order must be >= 0
%:- order(O,I,U,T), U < 0.

% number of units on a shelf must be >= 0
%:- product(S,I,U,T), U < 0.



  % the robot and shelf being delivered are located at the same position
  %:- deliverShelf(R,S,I,U,O,T), locRobot(R,X1,Y1,T-1), locShelf(S,X2,Y2,T-1), cell(X1,Y1) != cell(X2,Y2).

  % the shelf being delivered is located at a picking station at t-1
  :- deliverShelf(R,S,I,U,O,T), locShelf(S,X1,Y1,T-1), pickStation(P,X2,Y2), cell(X1,Y1) != cell(X2,Y2).


% the robot conducting the delivery must be holding the shelf
:- deliverShelf(R,S,I,U,O,T), isHolding(R,S,f,T).

% the robot conducting the delivery is located at a picking station at t-1
:- deliverShelf(R,S,I,U,O,T), locRobot(S,X1,Y1,T-1), pickStation(P,X2,Y2), cell(X1,Y1) != cell(X2,Y2).



% only deliver products on shelves if an order still requires units of product
%:- deliverShelf(R,S,I,U1,O,T), product(S,I,U2), order(O,P,I,U3,T-1), U3<=0.

% only deliver products on shelves with available units of product
%:- deliverShelf(R,S,I,U1,O,T), product(S,I,U2), order(O,P,I,U3,T-1), U2<=0.

% only deliver order to the designated picking station for that order
%:- deliverShelf(R,S,I,U,O,T),





% Get order information
%product(S,I,U,T) :- init(object(product,I),value(on,pair(S,U))).
%order(O,P,I,U,T) :- init(object(order,O),value(line,pair(I,U))),
%                    init(object(order,O),value(pickingStation,P)).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Domain Independent Axioms
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% fluents are initially exogenous
1{locRobot(R,XX,YY,0): cell(XX,YY)}1 :- robot(R).
1{locShelf(S,XX,YY,0): cell(XX,YY)}1 :- shelf(S).
%1{isHolding(R,S,BB,0): boolean(BB)}1 :- shelf(S), robot(R).

% uniqueness and existence of value constraints
:- not 1{locRobot(R,XX,YY,T)}1, robot(R),  T=1..m.
:- not 1{locShelf(S,XX,YY,T)}1, shelf(S), T=1..m.
:- not 1{isHolding(R,S,BB,T)}1, robot(R), shelf(S), T=1..m.
:- not 1{productRemaining(S,I,UU,T)}1, shelf(S), product(I), T=1..m.
:- not 1{orderRemaining(O,I,UU,T)}1, order(O), product(I), T=1..m.

% actions are exogenous
{moveRobot(R,DX,DY,T):move(DX,DY)}1 :- robot(R), T=0..m-1.
{pickupShelf(R,SS,T):shelf(SS)}1 :- robot(R), T=0..m-1.
{putdownShelf(R,SS,T):shelf(SS)}1 :- robot(R), T=0..m-1.
{deliverShelf(R,S,I,UU,O,T):orderRemaining(_,_,UU,_)}1 :- robot(R), shelf(S), product(I), order(O), T=0..m-1.

% commonsense law of inertia
{locRobot(R,X,Y,T+1)} :- locRobot(R,X,Y,T), T=0..m-1.
{locShelf(S,X,Y,T+1)} :- locShelf(S,X,Y,T), T=0..m-1.
{isHolding(R,S,B,T+1)} :- isHolding(R,S,B,T), T=0..m-1.
{productRemaining(S,I,U,T+1)} :- productRemaining(S,I,U,T), T=0..m-1.
{orderRemaining(O,I,U,T+1)} :- orderRemaining(O,I,U,T), T=0..m-1.
