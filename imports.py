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

# these need to be input from user, but for now we are hardcoding them
allowed_args_dict = {'works-update/priority': ['p0', 'p1', 'p2', 'p3'],
 'works-update/type': ['issue', 'task', 'ticket'],
 'works_list/issue.priority': ['p0', 'p1', 'p2', 'p3'],
 'works_list/ticket.needs_response': ['true', 'false'],
 'works_list/ticket.severity': ['blocker', 'low', 'medium', 'high'],
 'works_list/type': ['issue', 'task', 'ticket'],
 'works-create/issue.priority': ['p0', 'p1', 'p2', 'p3'],
 'works-create/type': ['issue', 'task', 'ticket'],
 'works-create/title': ['issue', 'ticket']}

args_in_list_dict = {
 'works_list/applies_to_part': 1,
 'works_list/created_by': 1,
 'works_list/issue.priority': 1,
 'works_list/issue.rev_orgs': 1,
 'works_list/limit': 0,
 'works_list/owned_by': 1,
 'works_list/stage.name': 1,
 'works_list/ticket.needs_response': 0,
 'works_list/ticket.rev_org': 1,
 'works_list/ticket.severity': 1,
 'works_list/ticket.source_channel': 1,
 'works_list/type': 1,
 'works_list/date_of_creation': 0,
 'works_list/last_modified': 0,
 'works_list/target_close_date': 0,
 'works_list/sprint': 1,
 'summarize_objects/objects': 1,
 'prioritize_objects/objects': 1,
 'add_work_items_to_sprint/work_ids': 1,
 'add_work_items_to_sprint/sprint_id': 0,
 'get_similar_work_items/work_id': 0,
 'search_object_by_name/query': 0,
 'create_actionable_tasks_from_text/text': 0,
 'is_empty/list_to_check': 0,
 'count/objects': 1,
 'works-create/applies_to_part': 1,
 'works-create/created_by': 1,
 'works-create/issue.priority': 1,
 'works-create/developed_with': 1,
 'works-create/owned_by': 1,
 'works-create/stage.name': 1,
 'works-create/sprint': 1,
 'works-create/type': 1,
 'works-create/target_close_date': 0,
 'works-create/title': 0,
 'works-delete/id': 1,
 'works-update/id': 1,
 'works-update/applies_to_part': 1,
 'works-update/created_by': 1,
 'works-update/owned_by': 1,
 'works-update/stage.name': 1,
 'works-update/type': 1,
 'works-update/target_close_date': 0,
 'works-update/title': 0,
 'works-update/priority': 1,
 'rev-orgs-create/description': 0,
 'rev-orgs-create/display_name': 0,
 'rev-orgs-create/environment': 0,
 'rev-orgs-delete/id': 0,
 'rev-orgs-update/description': 0,
 'rev-orgs-update/display_name': 0,
 'rev-orgs-update/environment': 0,
 'rev-orgs-update/id': 0,
 'get_works_id/objects': 1,
 'get_current_date/': 0
}