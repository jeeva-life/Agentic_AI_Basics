from langchain_aws import ChatBedrock
from langchain_google_genai import GoogleGenerativeAIEmbeddings

llm_model = ChatBedrock(model_id='us.anthropic.claude-sonnet-4-20250514-v1:0',
                        region_name="us-west-2", temperature=0)

embed_model = GoogleGenerativeAIEmbeddings(model_name="text-embedding-004")