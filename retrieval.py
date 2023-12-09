from imports import *

loader = CSVLoader(file_path="Untitled spreadsheet - Sheet1.csv", source_column = 'Queries')
data = loader.load()

embeddings = HuggingFaceEmbeddings()
# persist_directory = 'docs/chroma_db/'
# !rm -rf ./docs/chroma_db
vector_db = FAISS.from_documents(
    documents=data,
    embedding=embeddings,
    # persist_directory=persist_directory
)
# vector_db.persist()

def store_to_df(store):
  v_dict = store.docstore._dict
  data_rows = []
  for k in v_dict.keys():
    content = v_dict[k].page_content
    data_rows.append({"chunk_id" : k, "content" : content})
  vector_df = pd.DataFrame(data_rows)
  return vector_df

def show_vstore(store):
  vector_df = store_to_df(store)
  # display(vector_df)

def delete_tool_examples(store, tool_name):
  vector_df = store_to_df(store)
  mask = vector_df['content'].str.contains(tool_name)
  chunk_ids_to_delete = vector_df.loc[mask, 'chunk_id']
  print(chunk_ids_to_delete)
  store.delete(chunk_ids_to_delete)

def add_to_vector_store(store, example):
  doc = Document(page_content = example)
  extension = FAISS.from_documents([doc], embeddings)
  store.merge_from(extension)
