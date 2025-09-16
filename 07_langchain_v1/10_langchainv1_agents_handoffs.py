import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# Setup the OpenAI client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)

@tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"Weather in {city}: Temperature 72°F, Sunny"


class AgentHandoff:
    """Handles agent handoffs based on language detection."""
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

        # Create specialized agents
        self.hungarian_agent = self._create_hungarian_agent()
        self.spanish_agent = self._create_spanish_agent()
        self.english_agent = self._create_english_agent()
        self.triage_agent = self._create_triage_agent()
    
    def _create_spanish_agent(self):
        """Create Spanish-speaking agent."""
        prompt = "Eres un agente que solo habla español. Puedes proporcionar información del clima usando la herramienta get_weather."
        
        agent = create_agent(model=self.llm, prompt=prompt, tools=[get_weather])
        return agent
    
    def _create_hungarian_agent(self):
        """Create Hungarian-speaking agent."""
        prompt = "Ez egy magyar nyelvű agent. Használhatja a get_weather eszközt."
        agent = create_agent(model=self.llm, prompt=prompt, tools=[get_weather])
        return agent
    
    def _create_english_agent(self):
        """Create English-speaking agent."""
        prompt = "You are an agent that only speaks English. You can provide weather information using the get_weather tool."
        
        agent = create_agent(model=self.llm, prompt=prompt, tools=[get_weather])
        return agent
    
    def _create_triage_agent(self):
        """Create triage agent that determines language and hands off."""
        prompt = """You are a triage agent. Your job is to determine the language of the user's request and hand off to the appropriate agent:
        - If the request is in Spanish, respond with: "HANDOFF_TO_SPANISH"
        - If the request is in English, respond with: "HANDOFF_TO_ENGLISH"
        - If the request is in Hungarian, respond with: "HANDOFF_TO_HUNGARIAN"
        - Only respond with the handoff instruction, nothing else."""
        
        agent = create_agent(model=self.llm, prompt=prompt, tools=[])
        return agent
    
    def _detect_language_and_handoff(self, input_text: str) -> str:
        """Detect language and determine which agent to hand off to."""
        handoff_decision = self.triage_agent.invoke({"messages": [{"role": "user", "content": input_text}]})
        
        # Extract the content from the response
        latest_message = handoff_decision["messages"][-1]
        handoff_text = latest_message.content
        
        if "HANDOFF_TO_SPANISH" in handoff_text:
            result = self.spanish_agent.invoke({"messages": [{"role": "user", "content": input_text}]})
            latest_message = result["messages"][-1]
            return latest_message.content
        elif "HANDOFF_TO_ENGLISH" in handoff_text:
            result = self.english_agent.invoke({"messages": [{"role": "user", "content": input_text}]})
            latest_message = result["messages"][-1]
            return latest_message.content
        elif "HANDOFF_TO_HUNGARIAN" in handoff_text:
            result = self.hungarian_agent.invoke({"messages": [{"role": "user", "content": input_text}]})
            latest_message = result["messages"][-1]
            return latest_message.content
        else:
            # Fallback to English agent
            result = self.english_agent.invoke({"messages": [{"role": "user", "content": input_text}]})
            latest_message = result["messages"][-1]
            return latest_message.content
    
    async def run(self, input_text: str) -> str:
        """Run the handoff logic with the given input."""
        result = self._detect_language_and_handoff(input_text)
        return result


async def main():
    """Main function to demonstrate the handoff logic."""
    handoff_system = AgentHandoff()

    # Test with Hungarian input
    hungarian_input = "Üdv, hogy vagy? Kérem, add meg a San Francisco CA időjárását."
    print("Hungarian input:", hungarian_input)
    result = await handoff_system.run(hungarian_input)
    print("Result:", result)
    print("-" * 50)

    # Test with Spanish input
    spanish_input = "Hola, ¿cómo estás? ¿Puedes darme el clima para San Francisco CA?"
    print("Spanish input:", spanish_input)
    result = await handoff_system.run(spanish_input)
    print("Result:", result)
    print("-" * 50)
    
    # Test with English input
    english_input = "Hello, how are you? Can you give me the weather for San Francisco CA?"
    print("English input:", english_input)
    result = await handoff_system.run(english_input)
    print("Result:", result)


if __name__ == "__main__":
    asyncio.run(main())
