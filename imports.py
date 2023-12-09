import streamlit as st
import json
import os
import time
import random
import torch
from torch import cuda, bfloat16
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList
import warnings
import simplejson as json
import pandas as pd

from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

from langchain.chains import (
    LLMChain,
    ConversationChain,
    SequentialChain,
    SimpleSequentialChain
)

from langchain.memory import (
    ConversationBufferWindowMemory,
    ConversationBufferMemory
)

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI, HuggingFaceHub, HuggingFacePipeline
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema.document import Document