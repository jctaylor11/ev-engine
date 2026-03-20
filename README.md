# ev-engine
An engine that quantifies expected value of a trade within a holding period, given market state and a risk-reward ratio

## Architecture
Modular architecture with separation of concerns for each stage of the pipeline. 

1. **Ingestion**     Fetch and clean data
2. **Database**      Connection, schema and loaders
3. **Indicators**    Compute state for each candle
4. **Outcomes**      Compute outcomes from each candle
5. **Analysis**      Conditional probability and statistics
6. **Visualisation** Heatmaps