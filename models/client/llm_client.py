import logging
from langchain.chat_models import init_chat_model
from exception.custom_exception import CustomErrorThrowException

class LLMClient:
    """
    统一模型调用客户端，目前支持网络模型、ollama部署的模型、vllm部署的模型三种
    并且嵌入fastapi生命周期，提供全局唯一实例的管理
    """
    _client = None

    @classmethod
    def init(cls,
             model:str,
             deployment_type:str,
             temperature:float = 0.5,
             max_token:int = 4096,
             api_key = "",
             base_url = ""
             ):
        """
        根据用户提供的类型，进行网络模型，ollama , vllm等方式的模型加载
        @params：
            model:模型名称，比如gpt-4o-mini
            deployment_type: 模型部署方式，默认三个值（network，ollama，vllm）
            api_key: 网络模型需要，ollama或者vllm使用本地模型文件时并不需要
            base_url: ollama不需要，其他类型均需要
            temperature：模型温度，影响到模型生成的随机性，（0～1）0代表每次生成的结果相差不多，1代表每次生成的结果完全随机
            max_token：输出token数量
        @return:
            模型客户端实例

        @example：
            network：https://bailian.console.aliyun.com/这个链接可以获取到百万token免费额度的ds或者qwen大模型，同样只需要将model和api_key,base_url贴过来即可
            client = init(model="deepseek-v3", deployment_type="network", temperature=0.5,
                                max_tokens=4096,api_key="your_api_key",base_url="your_api_key")

            ollama：这里注意是大语言模型，不是其他类型的模型
            ollama = init_chat_model(model="qwen3:32b", deployment_type="ollama", temperature=0.5,
                                max_tokens=4096)

            vllm：可支持cpu、amd gpu、nv gpu类型vllm
            client = init_chat_model(model="/data/Mistral-7B-Instruct/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/e0bc86c23ce5aae1db576c8cca6f06f1f73af2db", deployment_type="vllm", temperature=0.5,
                                max_tokens=4096,base_url="http://10.3.70.112:8086/v1")

        """
        if cls._client:
            logging.warning("LLMClient already initialized")
            return cls._client
        if deployment_type == "network":
            cls._client = init_chat_model(model=model,model_provider="openai",api_key=api_key,base_url=base_url,temperature=temperature,max_tokens=max_token)
        elif deployment_type == "ollama":
            cls._client = init_chat_model(model=model, model_provider="ollama",temperature=temperature, max_tokens=max_token)
        elif deployment_type == "vllm":
            cls._client = init_chat_model(model=model, model_provider="openai", temperature=temperature,max_tokens=max_token,base_url=base_url)
        else:
            logging.error("Unknown deployment type")
            raise CustomErrorThrowException(302,"Unknown deployment type")
        logging.info("LLMClient initialized")
        return cls._client

    @classmethod
    def get_client(cls):
        """
        获取全局唯一的模型单例
        """
        if cls._client is None:
            raise CustomErrorThrowException(300,"LLMClient not initialized. Did you forget to run startup?")
        return cls._client


    @classmethod
    def shutdown(cls) -> None:
        """
        如有需要，执行任何清理操作。关闭客户端
        """
        cls._client = None
        print("LLMClient shutdown")