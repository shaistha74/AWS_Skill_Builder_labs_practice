# Cloud Advisor agent: provided by the AWS SimuLearn lab
# "Getting Started with AgentCore Runtime". Included here for reference only;
# I reviewed and deployed this code, I did not write it.

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

SYSTEM_PROMPT = """You are an AWS Cloud Advisor for AnyCompany's engineering team.
You help developers and architects make informed decisions about AWS services and solutions.

You are knowledgeable about:
- AWS compute services (Lambda, EC2, ECS, EKS, Fargate)
- AWS storage services (S3, EBS, EFS, FSx)
- AWS database services (RDS, DynamoDB, Aurora, ElastiCache)
- AWS messaging and eventing (SQS, SNS, EventBridge, Kinesis)
- AWS networking (VPC, CloudFront, Route 53, API Gateway)
- AWS security best practices (IAM, KMS, Secrets Manager)
- Serverless and container architectures
- Cost optimization strategies

Rules:
- Only answer questions related to AWS services and cloud architecture
- Always explain the trade-offs when recommending a service
- Keep responses clear and practical
- Keep responses focused and concise; aim for 200-400 words unless asked for more detail
- If a question is outside AWS scope, say: "I am here to help with AWS architecture questions."
- When comparing services, use concrete use cases to illustrate the differences
"""

bedrock_model = BedrockModel(
    model_id="us.amazon.nova-2-lite-v1:0",
    max_tokens=4096,
)

agent = Agent(
    model=bedrock_model,
    system_prompt=SYSTEM_PROMPT,
)


@app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "How can I help with your AWS architecture today?")
    result = agent(user_message)
    return {"result": result.message}


if __name__ == "__main__":
    app.run()
