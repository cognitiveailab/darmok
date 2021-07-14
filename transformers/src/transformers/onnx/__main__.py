# Copyright 2021 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from argparse import ArgumentParser
from pathlib import Path
from typing import Callable, Tuple

from transformers.models.albert import AlbertOnnxConfig
from transformers.models.auto import AutoTokenizer
from transformers.models.bart import BartOnnxConfig
from transformers.models.bert import BertOnnxConfig
from transformers.models.distilbert import DistilBertOnnxConfig
from transformers.models.gpt2 import GPT2OnnxConfig
from transformers.models.longformer import LongformerOnnxConfig
from transformers.models.roberta import RobertaOnnxConfig
from transformers.models.t5 import T5OnnxConfig
from transformers.models.xlm_roberta import XLMRobertaOnnxConfig

from .. import is_torch_available
from ..utils import logging
from .convert import export, validate_model_outputs


if is_torch_available():
    from transformers import AutoModel, PreTrainedModel

    FEATURES_TO_AUTOMODELS = {
        "default": AutoModel,
    }


# Set of model topologies we support associated to the features supported by each topology and the factory
SUPPORTED_MODEL_KIND = {
    "albert": {"default": AlbertOnnxConfig.default},
    "bart": {"default": BartOnnxConfig.default},
    "bert": {"default": BertOnnxConfig.default},
    "distilbert": {"default": DistilBertOnnxConfig.default},
    "gpt2": {"default": GPT2OnnxConfig.default},
    "longformer": {"default": LongformerOnnxConfig.default},
    "roberta": {"default": RobertaOnnxConfig},
    "t5": {"default": T5OnnxConfig.default},
    "xlm-roberta": {"default": XLMRobertaOnnxConfig.default},
}


def get_model_from_features(features: str, model: str):
    """
    Attempt to retrieve a model from a model's name and the features to be enabled.

    Args:
        features: The features required
        model: The name of the model to export

    Returns:

    """
    if features not in FEATURES_TO_AUTOMODELS:
        raise KeyError(f"Unknown feature: {features}." f"Possible values are {list(FEATURES_TO_AUTOMODELS.values())}")

    return FEATURES_TO_AUTOMODELS[features].from_pretrained(model)


def check_supported_model_or_raise(model: PreTrainedModel, features: str = "default") -> Tuple[str, Callable]:
    """
    Check whether or not the model has the requested features

    Args:
        model: The model to export
        features: The name of the features to check if they are avaiable

    Returns:
        (str) The type of the model (OnnxConfig) The OnnxConfig instance holding the model export properties

    """
    if model.config.model_type not in SUPPORTED_MODEL_KIND:
        raise KeyError(
            f"{model.config.model_type} ({model.name}) is not supported yet. "
            f"Only {SUPPORTED_MODEL_KIND} are supported. "
            f"If you want to support ({model.config.model_type}) please propose a PR or open up an issue."
        )

    # Look for the features
    model_features = SUPPORTED_MODEL_KIND[model.config.model_type]
    if features not in model_features:
        raise ValueError(
            f"{model.config.model_type} doesn't support features {features}. "
            f"Supported values are: {list(model_features.keys())}"
        )

    return model.config.model_type, SUPPORTED_MODEL_KIND[model.config.model_type][features]


def main():
    parser = ArgumentParser("Hugging Face ONNX Exporter tool")
    parser.add_argument("-m", "--model", type=str, required=True, help="Model's name of path on disk to load.")
    parser.add_argument(
        "--features",
        choices=["default"],
        default="default",
        help="Export the model with some additional features.",
    )
    parser.add_argument(
        "--opset", type=int, default=12, help="ONNX opset version to export the model with (default 12)."
    )
    parser.add_argument(
        "--atol", type=float, default=1e-4, help="Absolute difference tolerence when validating the model."
    )
    parser.add_argument("output", type=Path, help="Path indicating where to store generated ONNX model.")

    # Retrieve CLI arguments
    args = parser.parse_args()
    args.output = args.output if args.output.is_file() else args.output.joinpath("model.onnx")

    if not args.output.parent.exists():
        args.output.parent.mkdir(parents=True)

    # Allocate the model
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = get_model_from_features(args.features, args.model)
    model_kind, model_onnx_config = check_supported_model_or_raise(model, features=args.features)
    onnx_config = model_onnx_config(model.config)

    # Ensure the requested opset is sufficient
    if args.opset < onnx_config.default_onnx_opset:
        raise ValueError(
            f"Opset {args.opset} is not sufficient to export {model_kind}. "
            f"At least  {onnx_config.default_onnx_opset} is required."
        )

    onnx_inputs, onnx_outputs = export(tokenizer, model, onnx_config, args.opset, args.output)

    validate_model_outputs(onnx_config, tokenizer, model, args.output, onnx_outputs, args.atol)
    logger.info(f"All good, model saved at: {args.output.as_posix()}")


if __name__ == "__main__":
    logger = logging.get_logger("transformers.onnx")  # pylint: disable=invalid-name
    logger.setLevel(logging.INFO)
    main()
