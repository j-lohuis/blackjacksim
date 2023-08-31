# Blackjack Simulator

This project aims to simulate multiple strategies of playing Blackjack.

We hope to distinguish the differences in making money between different strategies,
especially different card counting approaches.

## How to run

```
$ git clone <link>

Either
$ conda install --file requirements.txt
or
$ pip -r requirements.txt


$ python blackjack.py
```

## Strategies

-   Basic Strategy
-   Random player
-   Gamblers fallacy player
-   Hi-Lo card counter
-   Hi-Opt I card counter
-   Hi-Opt II card counter
-   KO card counter
-   Omega II card counter
-   Zen count card counter
-   10 count card counter

More detail about the different card counter strategies can be found [here](https://en.wikipedia.org/wiki/Card_counting)

## Playing by yourself

We have also implemented a way you can play via the terminal.

You can choose 'play by yourself' when starting the application.

## Notes

For the simulations we chose to not limit the budget and start off with 0 as this leads to a more accurate simulation over time. This is because otherwise hitting a budget of 0 would lead to the player leaving the table. Additionally, we can also measure losses of all strategies more precisely.

Most casinos play with multiple decks, called a shoe. The most common number of decks we found is 6, so we implemented that.

Simulating more than 100.000 rounds might take a while, but still has a small memory footprint.

## Results

Here are a few pre-computed plots for various strategies and number of rounds played:

### All Players

As you can see in both charts above the _Average Player_ is quite eratic while the _Random Player_ is just loosing money continuously.
The _Average Player_ (or Gamblers fallacy player) doubles their bet after every loss. So theoretically they will always win back the losses. In practice you don't have an unlimited budget. As you can see in the bottom plot the player lost 50 million at one point.

![All Players 10k rounds](plots/10000_all.png)

![All Players 100k rounds](plots/100000_all.png)

### Only Basic Strategy and Card Counters

In both of these charts you can see that the Basic Strategy (_Optimal Player_) looses over time while the card counters tend to win.
The Basic Strategy wins in the top plot over 100.000 games, but that is only a statistical anomaly and it loses over time.
While the card counters tend to win over time, they can also lose a lot of money as you can see at the start of the first plot.

![Optimal + Card Counters 100k rounds](plots/100000_opt+count.png)

![Optimal + Card Counters 1m](plots/1000000_opt+count.png)

### Only Card Counters

These charts give a more detailed overview of the different card counting strategies.
While the rankings of the different counting strategies change due to the randomness of the game, we still observed some trends:

-   Hi-Lo, Hi-Opt I and Hi-Opt II are more stable and win less over time. So it seems they tend to bet less and keep the risk lower than the other strategies.
-   10 Count and KO are fluctuating the most. They tend to bet big and the count seems to be more sensitive with these strategies.
-   Zen Count and Omega II seem to find a middle ground. They also seem to perform the best and most consistent in our simulations.

![Only Card Counters 100k rounds](plots/100000_count.png)

![Only Card Counters 1m rounds](plots/1000000_count.png)
