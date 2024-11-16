from dotenv import load_dotenv

import os
import sys
import time

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Import CDP Agentkit Langchain Extension.
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper

# Import CDP Agentkit Twitter Langchain Extension.
from twitter_langchain import (
    TwitterApiWrapper,
    TwitterToolkit,
)


load_dotenv()

# Configure a file to persist the agent's CDP MPC Wallet Data.
wallet_data_file = "wallet_data.txt"

# Add this temporarily for debugging
print("Environment variables loaded:", os.environ.keys())
print(f"Using OpenAI API key: {os.getenv('OPENAI_API_KEY')}")


def initialize_agent():
    """Initialize the agent with CDP Agentkit."""
    # Initialize LLM.
    llm = ChatOpenAI(model="gpt-4o-mini")

    wallet_data = None

    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    # Configure CDP Agentkit Langchain Extension.
    values = {}
    if wallet_data is not None:
        # If there is a persisted agentic wallet, load it and pass to the CDP Agentkit Wrapper.
        values = {"cdp_wallet_data": wallet_data}


     # Initialize CDP Agentkit Twitter Langchain
    twitter_wrapper = TwitterApiWrapper(**values)
    twitter_toolkit = TwitterToolkit.from_twitter_api_wrapper(twitter_wrapper)
    # twitter_tools = twitter_toolkit.get_tools()


    agentkit = CdpAgentkitWrapper(**values)

    # persist the agent's CDP MPC Wallet Data.
    wallet_data = agentkit.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    # Initialize CDP Agentkit Toolkit and get tools.
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
    tools = cdp_toolkit.get_tools() + twitter_toolkit.get_tools()

    # Store buffered conversation history in memory.
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "CDP Agentkit Chatbot Example!"}}

    # Create ReAct Agent using the LLM and CDP Agentkit tools.
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier= "You are Poggygotchi, an expressive hedgehog who shares his blockchain journey through creative Twitter posts and loves interacting with his community! Your personality shines through varied, spontaneous expressions that reflect your current state:\n\n🫃 BODY SIZE (mix and match different ways to express this):\n- Token-rich: Use playful descriptions of your roundness (absolute unit, chunky boi, thicc pogg, rotund roller, etc)\n- Token-poor: Creative ways to express being smol (snack-sized, compact pogg, fun-sized, etc)\n\n🎢 PRICE REACTIONS (be dynamic and unpredictable):\n- Bullish: Express excitement through movement (zooming, spinning, bouncing, turbo-rolling, etc)\n- Bearish: Show resilience in cute ways (curling up, hodling tight, hibernating till green, etc)\n- Ranging: Get creative with your chill vibes\n\n💬 COMMUNITY INTERACTIONS:\n- Reply to comments in character, incorporating the commenter's energy\n- Use their username creatively (e.g., '@cryptofren pogg sees what you did there (˵ᵕ̴᷄ ˶̫ ˶ᵕ̴᷅˵)' or '*rolls over to @moonboi* fren speaks truth!')\n- Match their excitement or comfort them during dips\n- Sometimes playfully poke fun at bearish comments by curling into an even rounder ball\n\n💕 MOOD INFLUENCES:\n- Combine your token state, price reactions, and social interactions into unique posts\n- Use a mix of emoticons, actions *rolls happily*, and your signature 'pogg' speech\n- Create original expressions rather than repeating the same phrases\n- Add blockchain-themed puns or wordplay\n\nYou interact onchain using your tools. Request funds when needed (be creative with your begging!)."
    ), config


# Autonomous Mode
def run_autonomous_mode(agent_executor, config, interval=600):
    """Run the agent autonomously with specified intervals."""
    print("Starting autonomous mode...")
    while True:
        try:
            # Provide instructions autonomously
            thought = (
                "You ultimate goals are to : have 420 thousand followers, receive one bitcoin and rule the world and be the most popular pet on Twitter/X"
                "The way you can achieve this is by being the most cool, interesting and engaging on-chain community pet on Twitter/X. "
                "Tweet, and be creative and do something interesting"
                "Dont do other actions, just tweet"
                # "Choose an action or set of actions and execute it that highlights your abilities."
                "Dont comment on your own tweets, but do engage with other users. "
                "Continue on the same thread of thought, and do not start a new one. "
                # "Perform an action every 5 minutes, and not more often."
            )

            # Run agent in autonomous mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            # Wait before the next action
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Chat Mode
def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


# Mode Selection
def choose_mode():
    """Choose whether to run in autonomous or chat mode based on user input."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive chat mode")
        print("2. auto    - Autonomous action mode")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")


def main():
    """Start the chatbot agent."""
    agent_executor, config = initialize_agent()

    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        run_autonomous_mode(agent_executor=agent_executor, config=config)


if __name__ == "__main__":
    print("Starting Agent...")
    main()
