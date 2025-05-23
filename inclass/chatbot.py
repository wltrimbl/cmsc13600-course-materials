import requests
import json
from collections import Counter
from itertools import chain
import os
import openai
from openai import OpenAI

# Assume your API returns the data at this endpoint
response = requests.get("http://localhost:8000/app/dumpFeed")
data = response.json()

# Flatten and analyze
all_titles = [post['title'] for post in data]
all_contents = [post['content'] for post in data]
all_comments = list(chain.from_iterable(post['comments'].values() for post in data if post['comments']))

# Optional: count duplicates
title_counts = Counter(all_titles)
comment_counts = Counter(all_comments)


print (os.environ.get("OPENAIKEY")[0:40] )

client = OpenAI(
    api_key=os.environ.get("OPENAIKEY")  # Alternatively, set the OPENAI_API_KEY environment variable
)


def generate_post(example_titles, example_contents, example_comments=None):
    prompt = f"""
You are a witty and wholesome internet user contributing to a website full of posts about fuzzy bunnies. 
Here are some example post titles and contents:

{chr(10).join(f"Title: {t}\nContent: {c}" for t, c in zip(example_titles, example_contents))}

Based on the tone and topics above, generate a new original post with a title and content. 
Be creative but consistent in tone (mix wholesome, skeptical, and humorous).

Return the result in JSON like this:
{{"title": "...", "content": "..."}}
"""
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(repr(response))
    return json.loads(response.choices[0].message.content)

# ChatCompletion(id='chatcmpl-BXslBmhbCj8c4JF5MtZeJXtJ34NDl', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='{"title": "Are fuzzy bunnies secretly ninja masters?", "content": "They hop so quietly—you\'d think they’re sneaking around on ninja stealth. Maybe I should start training my bunny to be my personal guard. Fuzzy but lethal?"}', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1747415021, model='gpt-4.1-nano-2025-04-14', object='chat.completion', service_tier='default', system_fingerprint='fp_8fd43718b3', usage=CompletionUsage(completion_tokens=52, prompt_tokens=196, total_tokens=248, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))


# Use a sample from the dataset for context
new_post = generate_post(all_titles[:5], all_contents[:5])
print(new_post)

