from ai.model.rag_retriever import AnnouncementRetriever
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
import pickle
from konlpy.tag import Okt
from FlagEmbedding import BGEM3FlagModel
from ai.model.rag_generator import GenerationModel
from transformers import AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_elements(fileid):
    with open('./ai/model/preprocessed_data/{}.pkl'.format(fileid), 'rb') as f:
        elements = pickle.load(f)
    f.close()
    return elements


fileid = "51580934"

emb_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

korean_tokenizer = Okt()

elements = get_elements(fileid=fileid)

retriever = AnnouncementRetriever(elements=elements, 
                                        emb_model=emb_model, 
                                        korean_tokenizer=korean_tokenizer)

retrieve_dict = {"51580934": retriever}

model_id = "./ai/model/EEVE-Korean-Instruct-10.8B-v1.0-AIF-QA"

gen_model = GenerationModel.from_pretrained(
    model_id=model_id,
    export=False,
    use_fp16=True
)
gen_tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline("text-generation", model=gen_model, tokenizer=gen_tokenizer, 
                do_sample=True, temperature=0.2, max_new_tokens=512, truncation=True)

hf = HuggingFacePipeline(pipeline=pipe)


prompt_template = """아래는 작업을 설명하는 지시사항과 추가 정보를 제공하는 입력이 짝으로 구성됩니다. 이에 대한 적절한 응답을 작성해주세요.

### 지시사항:
{question}

### 입력:
{input}

### 응답:
"""

prompt = PromptTemplate.from_template(prompt_template)
chain = prompt | hf | StrOutputParser()

print("init 완료")