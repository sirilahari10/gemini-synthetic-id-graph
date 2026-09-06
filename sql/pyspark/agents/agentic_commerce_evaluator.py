"""
AI Agent that evaluates flagged transaction clusters to determine if the velocity 
is legitimate 'Agentic Commerce' (e.g., an AI buying groceries) or malicious fraud.
"""
def evaluate_transaction_intent(user_cluster_data):
    prompt = f"""
    Analyze this user's high-velocity transaction pattern: {user_cluster_data}.
    Is this indicative of legitimate Agentic Commerce (automated routine purchases) 
    or a synthetic identity attempting rapid asset liquidation?
    """
    # LLM evaluation logic here...
