import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("xyo_database")

# Collections for storing conversations, memory, and task results
conversations_collection = db.get_collection("conversations")
memory_collection = db.get_collection("memory")
task_results_collection = db.get_collection("task_results")

def store_conversation(user_id, message, response):
    """Stores user messages and agent responses."""
    conversations_collection.insert_one({
        "user_id": user_id,
        "message": message,
        "response": response,
    })

def store_memory(key, value):
    """Stores key-value pairs in memory."""
    memory_collection.update_one({"key": key}, {"$set": {"value": value}}, upsert=True)

def retrieve_memory(key):
    """Retrieves a value from memory using a key."""
    record = memory_collection.find_one({"key": key})
    return record["value"] if record else None

def store_task_result(task_description, result):
    """Stores task results for future reference."""
    task_results_collection.insert_one({
        "task_description": task_description,
        "result": result,
    })
def get_conversation_history(user_id):
    """Retrieve the conversation history for a specific user."""
    return list(conversations_collection.find({"user_id": user_id}))

def save_conversation(user_id, user_message, agent_response):
    """Save a conversation entry in the database."""
    conversations_collection.insert_one({
        "user_id": user_id,
        "user_message": user_message,
        "agent_response": agent_response
    })