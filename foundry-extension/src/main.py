from fastapi import FastAPI
from pydantic import BaseModel
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

app = FastAPI()

class QueryRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/query")
def query_architect(request: QueryRequest):
    """Query the Architect Agent with a message."""
    
    ### PASTE PROJECTCLIENT CODE HERE ###
    # Example of what to paste:
    # project = AIProjectClient(
    #     credential=DefaultAzureCredential(),
    #     endpoint="https://your-project.services.ai.azure.com/api/projects/your-project")
    # agent = project.agents.get_agent("asst_xxxxx")
    # thread = project.agents.threads.create()
    # message = project.agents.messages.create(
    #     thread_id=thread.id,
    #     role="user",
    #     content=request.message  # <- Replace "Hello Agent" with request.message
    # )
    # run = project.agents.runs.create_and_process(
    #     thread_id=thread.id,
    #     agent_id=agent.id)
    # if run.status == "failed":
    #     print(f"Run failed: {run.last_error}")
    # else:
    #     messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    #     for message in messages:
    #         if message.text_messages:
    #             print(f"{message.role}: {message.text_messages[-1].text.value}")
    ### END PASTE ###
    
    # Extract the assistant's response from the messages
    assistant_response = None
    for msg in messages:
        if msg.role == "assistant" and msg.text_messages:
            assistant_response = msg.text_messages[-1].text.value
    
    return {
        "status": "success",
        "response": assistant_response
    }