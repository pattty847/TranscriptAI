"""
AI-powered transcript analysis using Ollama
"""
import asyncio
import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import ollama


@dataclass
class AnalysisResult:
    summary: str
    key_points: List[str]
    quotes: List[str]
    topics: List[str]
    sentiment: str
    custom_analysis: Dict[str, Any]


class OllamaAnalyzer:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.client = ollama.Client()
        # On lower-memory systems, unload model after each call.
        self.keep_alive = "0s"

    @staticmethod
    def _normalize_model_name(name: str) -> str:
        """Normalize model aliases such as `llama3.2` and `llama3.2:latest`."""
        return name.strip().lower().split(":")[0]

    @staticmethod
    def _extract_model_names(response: Any) -> List[str]:
        """Support both dict responses and typed Ollama ListResponse objects."""
        names: List[str] = []

        if isinstance(response, dict):
            for model in response.get("models", []):
                name = model.get("name") or model.get("model")
                if name:
                    names.append(str(name))
            return names

        model_list = getattr(response, "models", None)
        if model_list:
            for model in model_list:
                name = getattr(model, "model", None) or getattr(model, "name", None)
                if name:
                    names.append(str(name))
        return names

    @staticmethod
    def _extract_chat_content(response: Any) -> str:
        """Support both dict responses and typed Ollama ChatResponse objects."""
        if isinstance(response, dict):
            return response.get("message", {}).get("content", "")

        message = getattr(response, "message", None)
        if message is not None:
            content = getattr(message, "content", "")
            if content:
                return str(content)
        return ""

    async def list_available_models(self) -> List[str]:
        """Return available local Ollama model names."""
        try:
            models = await asyncio.to_thread(self.client.list)
            return self._extract_model_names(models)
        except Exception:
            return []

    async def check_model_availability(self) -> bool:
        """Check if the specified model is available"""
        try:
            requested = self._normalize_model_name(self.model)
            available_models = await self.list_available_models()
            if not available_models:
                return False

            for name in available_models:
                normalized = self._normalize_model_name(name)
                if normalized == requested or name.lower() == self.model.lower():
                    return True
            return False
        except Exception:
            return False

    async def resolve_model_name(self) -> Optional[str]:
        """Return the local model name that should be used for calls."""
        requested = self._normalize_model_name(self.model)
        for name in await self.list_available_models():
            if self._normalize_model_name(name) == requested or name.lower() == self.model.lower():
                return name
        return None
            
    async def ensure_model(self) -> bool:
        """Ensure model is available, pull if necessary"""
        resolved = await self.resolve_model_name()
        if resolved:
            self.model = resolved
            return True
            
        try:
            # Pull the model
            await asyncio.to_thread(self.client.pull, self.model)
            resolved = await self.resolve_model_name()
            if resolved:
                self.model = resolved
                return True
            return False
        except Exception as e:
            print(f"Failed to pull model {self.model}: {e}")
            return False

    async def _generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """Generate response from Ollama"""
        try:
            response = await asyncio.to_thread(
                self.client.chat,
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                keep_alive=self.keep_alive,
            )
            content = self._extract_chat_content(response)
            return content or "Error: Empty model response"
        except Exception as e:
            return f"Error: {str(e)}"

    async def summarize(self, transcript: str) -> str:
        """Generate a concise summary of the transcript"""
        system_prompt = "You are an expert at creating concise, engaging summaries. Extract the key points and main narrative."
        
        prompt = f"""
        Create a compelling summary of this transcript. Focus on the main themes, key insights, and most interesting points.
        Keep it engaging and informative, around 3-5 sentences.
        
        Transcript:
        {transcript[:4000]}...
        """
        
        return await self._generate_response(prompt, system_prompt)

    async def extract_quotes(self, transcript: str, max_quotes: int = 10) -> List[str]:
        """Extract the most interesting/quotable moments"""
        system_prompt = "You are an expert at finding the most quotable, interesting, or insightful moments from content."
        
        prompt = f"""
        Find the {max_quotes} most quotable moments from this transcript. Look for:
        - Profound insights
        - Funny or memorable lines  
        - Controversial or thought-provoking statements
        - Key conclusions or revelations
        
        Return ONLY a JSON array of strings, no other text.
        
        Transcript:
        {transcript[:4000]}...
        """
        
        response = await self._generate_response(prompt, system_prompt)
        
        try:
            # Try to parse JSON response
            quotes = json.loads(response)
            return quotes if isinstance(quotes, list) else []
        except:
            # Fallback: extract quotes manually
            lines = response.split('\n')
            quotes = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and len(line) > 20:
                    # Remove quotes and bullet points
                    line = re.sub(r'^[-*•]\s*', '', line)
                    line = line.strip('"\'')
                    if line:
                        quotes.append(line)
            return quotes[:max_quotes]

    async def extract_topics(self, transcript: str) -> List[str]:
        """Extract main topics and themes"""
        system_prompt = "You are an expert at identifying key topics and themes from content."
        
        prompt = f"""
        Identify the main topics, themes, and subjects discussed in this transcript.
        Return 5-10 key topics as a JSON array of strings.
        
        Transcript:
        {transcript[:4000]}...
        """
        
        response = await self._generate_response(prompt, system_prompt)
        
        try:
            topics = json.loads(response)
            return topics if isinstance(topics, list) else []
        except:
            # Fallback parsing
            lines = response.split('\n')
            topics = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    line = re.sub(r'^[-*•]\s*', '', line)
                    if line:
                        topics.append(line)
            return topics[:10]

    async def analyze_sentiment(self, transcript: str) -> str:
        """Analyze overall sentiment and emotional tone"""
        system_prompt = "You are an expert at analyzing emotional tone and sentiment in content."
        
        prompt = f"""
        Analyze the overall sentiment and emotional tone of this transcript.
        Describe it in 1-2 sentences, focusing on the dominant emotions and overall vibe.
        
        Transcript:
        {transcript[:4000]}...
        """
        
        return await self._generate_response(prompt, system_prompt)

    async def custom_analysis(self, transcript: str, custom_prompt: str) -> str:
        """Run custom analysis with user-provided prompt"""
        prompt = (
            f"{custom_prompt}\n\n"
            "Use the following transcript as source material. "
            "If evidence is not present, say so explicitly.\n\n"
            f"Transcript:\n{transcript[:6000]}..."
        )
        return await self._generate_response(prompt)

    async def test_model_response(self) -> str:
        """Run a lightweight model test request."""
        prompt = "Reply with exactly: MODEL_OK"
        return await self._generate_response(prompt, "You are a concise assistant.")

    async def full_analysis(self, transcript: str) -> AnalysisResult:
        """Run comprehensive analysis on transcript"""
        
        # Ensure model is available
        if not await self.ensure_model():
            raise Exception(f"Model {self.model} is not available and could not be downloaded")
        
        # Run analyses sequentially to avoid large RAM spikes.
        summary = await self.summarize(transcript)
        quotes = await self.extract_quotes(transcript)
        topics = await self.extract_topics(transcript)
        sentiment = await self.analyze_sentiment(transcript)
        
        return AnalysisResult(
            summary=summary,
            key_points=[],  # Could add key points extraction
            quotes=quotes,
            topics=topics,
            sentiment=sentiment,
            custom_analysis={}
        )


async def test_analyzer():
    """Test the analyzer with sample text"""
    analyzer = OllamaAnalyzer()
    
    # Test with sample transcript
    sample_transcript = """
    Welcome to today's podcast. We're talking about the future of artificial intelligence
    and how it's going to change everything. I think AI is going to be the most transformative
    technology of our lifetime. It's already changing how we work, how we create, and how we think.
    
    But there are also serious concerns. What happens to jobs? What about privacy? 
    These are questions we need to answer now, not later.
    
    The key is to stay informed and stay engaged. Technology isn't destiny - we shape how it develops.
    """
    
    try:
        print("Running full analysis...")
        result = await analyzer.full_analysis(sample_transcript)
        
        print(f"\nSummary: {result.summary}")
        print(f"\nQuotes: {result.quotes}")
        print(f"\nTopics: {result.topics}")
        print(f"\nSentiment: {result.sentiment}")
        
    except Exception as e:
        print(f"Analysis failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_analyzer())
