# dash

Hi Adam, here is some more information about my problem.

First some info aobut my file setup: it is a two-tab dashboard that is split into three files:
  - Euronext Tab: with layout of this tab
  - S&P 500 Tab: with layout of this tab
  - financial dashboard: callbacks of both tabs
 
Everything works fine on load and the first stock chosen. However, when I choose another ticker, my DataFrame on which my graph is based updates 
as can be seen by the two other callbacks that change but my graph remains unchanged. I tried to solve this problem by reconfiguring my Euronext tab and callbacks 
to mimic the setup seen in your github repositories: 
https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/bootstrap_card.py and https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/Complete_Guide/live_bootstrap.py
however, i get an Error saying:
  Invalid argument `figure` passed into Graph with ID "linegraph-container-enx".
  Expected `object`.
  Was supplied type `string`.
  Value provided: ""

I have looked everywhere on the internet, but I was unable to solve this error. I was hoping you could solve my problem, 
this would be amazing as I am really struggling with this issue for days.
Kind Regards, Emile
