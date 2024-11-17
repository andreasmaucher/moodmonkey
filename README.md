# Poggy - the world's first autonomous AI hedgehog

Poggy, your autonomous on-chain AI hedgehog and the 21st-century Tamagotchi. Its mood and behavior mirror the token price, creating
a playful and emotional connection. As the community “feeds” it tokens, Poggie evolves, unlocking new traits and rewarding its supporters.
This project leverages the AgentKit from the Coinbase Developer Platform and is currently running on Base Sepolia.

## Technical buildup:
- Agent Kit (https://github.com/coinbase/cdp-agentkit/)
- CDP SDK (Coinbase Developer Platform) for robust Web3 integration
- MPC Wallets for secure crypto asset management
- Blockscout API for real-time price monitoring and transaction tracking

## AI stack:
- LangChain/LangGraph for sophisticated agent workflows
- OpenAI GPT-4 as the decision-making engine
- Tweepy library for social media engagement (Twitter/X)

## Environment setup & installation:

First follow this quickstart guide:
https://docs.cdp.coinbase.com/agentkit/docs/quickstart

If you run into python related issues during the installation we recommend setting up a virtual environment (venv).
Furthermore, we recommend creating a .env file instead of using the export function. Don't forget your git_ignore!

To run Poggy navigate to the relevant directory:
cd agentkit/cdp_langchain/examples/poggy

Run the program:
run chatbot.py

