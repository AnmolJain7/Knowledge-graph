from app.langgraph.graphs.create_user_graph import create_user_graph

result = create_user_graph.invoke({
    "thread_id": "123",
    "intent": "create_user",
    "current_step": None,
    "last_user_message": None,
    "name":"Anmol Jain",
    "address":"Pune",
    "phone_number":"1234567890",
    "age":10,
    "gender":"male",
    "user_id": None,
    "response":None,
    "is_completed": False
})

print(result)
