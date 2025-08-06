import logging
from typing import Dict, Any

from langchain.chat_models import init_chat_model
from exception.custom_exception import CustomErrorThrowException

class LLMClient:
    """
    支持多模型命名空间的统一模型调用客户端。
    通过 init(namespace, config) 初始化不同命名空间下的模型配置；
    每次调用 get(namespace) 返回该命名空间下的新模型实例。
    """

    _config_map: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def init(cls, config: Dict[str, Any],namespace: str="default"):
        """
        初始化模型配置，并保存在命名空间下。

        Args:
            namespace: 命名空间标识符，用于区分不同模型配置
            config: 模型的配置信息，包含 model_name、deployment_type 等
            (
                model:模型名称，比如gpt-4o-mini
                deployment_type: 模型部署方式，默认三个值（network，ollama，vllm）
                api_key: 网络模型需要，ollama或者vllm使用本地模型文件时并不需要
                base_url: ollama不需要，其他类型均需要
                temperature：模型温度，影响到模型生成的随机性，（0～1）0代表每次生成的结果相差不多，1代表每次生成的结果完全随机
                max_token：输出token数量
            )
        """
        cls._config_map[namespace] = {
            "model_name": config.get("model_name", ""),
            "deployment_type": config.get("deployment_type", ""),
            "temperature": config.get("temperature", 0.5),
            "max_token": config.get("max_token", 4096),
            "api_key": config.get("api_key", ""),
            "base_url": config.get("base_url", ""),
        }
        logging.info(f"LLMClient config initialized for namespace: {namespace}")

    @classmethod
    def get(cls, namespace: str="default",temperature: float=None,max_token: int=None):
        """
        获取指定命名空间下的模型客户端实例。这些实例可以是网络模型，ollama , vllm等方式的模型实例

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

        if namespace not in cls._config_map:
            raise CustomErrorThrowException(301, f"Namespace '{namespace}' not initialized")

        config = cls._config_map[namespace]
        model_name = config["model_name"]
        deployment_type = config["deployment_type"]
        temperature = temperature if temperature else  config["temperature"]
        max_token = max_token if max_token else config["max_token"]
        api_key = config["api_key"]
        base_url = config["base_url"]

        if deployment_type == "network":
            client = init_chat_model(
                model=model_name,
                model_provider="openai",
                api_key=api_key,
                base_url=base_url,
                temperature=temperature,
                max_tokens=max_token
            )
        elif deployment_type == "ollama":
            client = init_chat_model(
                model=model_name,
                model_provider="ollama",
                temperature=temperature,
                max_tokens=max_token
            )
        elif deployment_type == "vllm":
            client = init_chat_model(
                model=model_name,
                model_provider="openai",  # vllm 使用 openai 协议
                base_url=base_url,
                temperature=temperature,
                max_tokens=max_token
            )
        else:
            logging.error(f"Unknown deployment type: {deployment_type}")
            raise CustomErrorThrowException(302, "Unknown deployment type")

        logging.info(f"LLMClient instance created for namespace: {namespace}")
        return client
