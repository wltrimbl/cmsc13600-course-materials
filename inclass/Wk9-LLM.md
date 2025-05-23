We have some options for running LLMs; we can use an API for powerful models on optimized infrastructure, we can run LLMs on rented hardware (or loss-leader "free" compute) such as jupyter lab or google colab, or we can download the weights and the LLM model and run it ourselves.

1.   chatbot.py  - accesses API key from shell environment
2.  A tutorial on langchain that anyone can run in colab has some hints about the desgin of multistep LLM pipelines: https://github.com/pinecone-io/examples/blob/master/learn/generation/langchain/handbook/02-langchain-chains.ipynb
3.   llm-local.py  requires downloading a 7G parameter model; runs slow because laptops weren't optimized for LLM.
