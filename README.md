<ul>
<li>Read Financial statements</li>
<li>Read company disclosure</li>
<li>Can you use binomial distribution to calculate the probability in the bullish market if price goes up tomorrow or not?</li>
</ul>

<h3>Sites</h3>
<ul>
<li><a href="https://www.pse.com.ph">https://www.pse.com.ph</a></li>
<li><a href="https://edge.pse.com.ph">https://edge.pse.com.ph</a></li>
<li><a href="https://www1.pse.com.ph/stockMarket/home.html">https://www1.pse.com.ph/stockMarket/home.html (Best for getting stock info like when it was listed)</a></li>
<li><a href="https://ph.investing.com/equities/transasia-oil-historical-data">https://ph.investing.com/equities/transasia-oil-historical-data (Best for historical data download)</a></li>
</ul>


<h3>Dependencies</h3>
<ul>
<li>Mysql</li>
<li>Redis</li>
<li>run rqworker on root</li>
</ul>


<h3>Data type for money</h3>
<ul>
<li>If your application needs to handle money values up to a trillion then this should work: 13,2 If you need to comply with GAAP (Generally Accepted Accounting Principles) then use: 13,4</li>
<li>Usually you should sum your money values at 13,4 before rounding of the output to 13,2.</li>
<li>https://stackoverflow.com/questions/13030368/best-data-type-to-store-money-values-in-mysql</li>
</ul>



<h3>Notes</h3>
<ul>
<li>One of the first goal is to test the average days a stock stays above, 200, 150, 50 MA</li>
<li>Next step is to make a model that predicts how many days a stock stays above , 200, 150, 50 MA</li>
<li>Usually you should sum your money values at 13,4 before rounding of the output to 13,2.</li>
<li>On average, there's too much false alarm when a stock breaks out of its 200, 150, 50 MA.</li>
<li>Create a stock ranking from minvervi scanner</li>
<li>Create a linear regression on what will be the average up days if a stock matches minervinis scanner</li>
<li>Different types of calculation must be made, a computation for all the SMAs, and RSI plus another one for the scoring list</li>
</ul>


<h3>References/Random</h3>
<ul>
<li><a href="https://www.alpharithms.com/relative-strength-index-rsi-in-python-470209/">Calculating RSI</a></li>
<li><a href="https://towardsdatascience.com/visualizing-stock-trading-agents-using-matplotlib-and-gym-584c992bc6d4">Visualizing stock trading</a></li>
<li><a href="https://towardsdatascience.com/how-to-easily-run-python-visualizations-on-a-web-browser-with-pyscript-4b287ef991cd">How to Easily Run Python Visualizations On a Web Browser with PyScript</a></li>
</ul>


<h3>Violations Soon After a breakout</h3>
<ul>
<li>Low volume out of a base</li>
<li>High volume back in three or four lower lows without supportive action</li>
<li>More down days and up days</li>
<li>More bad closes than good closes</li>
<li>A close below the 20-day moving average</li>
<li>A close below the 50-day moving average on heavy volume</li>
<li>Full retracement of a good size gain</li>
</ul>


<h3>Buying rules</h3>
<ul>
<li>If you didn't get to purchase during a breakout, buy at confirmation pullback at 5 minute chart</li>
</ul>