"""
MobileNetV2 fine-tuned for 38-class plant disease classification.
Also supports EfficientNet-B0 via the `architecture` argument.
"""
import torch
import torch.nn as nn
import torchvision.models as models
from ml.src.config import NUM_CLASSES, DROPOUT_RATE


def build_model(architecture: str = "mobilenet_v2", num_classes: int = NUM_CLASSES, pretrained: bool = True) -> nn.Module:
    """
    Builds and returns a fine-tuned model.

    Args:
        architecture: "mobilenet_v2" | "efficientnet_b0"
        num_classes:  Output classes (38 for PlantVillage)
        pretrained:   Load ImageNet weights

    Returns:
        nn.Module ready for training
    """
    weights_arg = "DEFAULT" if pretrained else None

    if architecture == "mobilenet_v2":
        model = models.mobilenet_v2(weights=weights_arg)
        # Freeze backbone, fine-tune classifier
        for param in model.features.parameters():
            param.requires_grad = False
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=DROPOUT_RATE),
            nn.Linear(in_features, num_classes),
        )

    elif architecture == "efficientnet_b0":
        model = models.efficientnet_b0(weights=weights_arg)
        for param in model.features.parameters():
            param.requires_grad = False
        in_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=DROPOUT_RATE),
            nn.Linear(in_features, num_classes),
        )

    else:
        raise ValueError(f"Unsupported architecture: {architecture}. Choose 'mobilenet_v2' or 'efficientnet_b0'.")

    total    = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[Model] {architecture}  total_params={total:,}  trainable={trainable:,}")
    return model


def unfreeze_backbone(model: nn.Module, architecture: str = "mobilenet_v2") -> nn.Module:
    """
    Unfreezes all backbone layers for fine-tuning phase 2.
    Call this mid-training after initial classifier warmup.
    """
    if architecture == "mobilenet_v2":
        for param in model.features.parameters():
            param.requires_grad = True
    elif architecture == "efficientnet_b0":
        for param in model.features.parameters():
            param.requires_grad = True
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[Model] Backbone unfrozen. Trainable params: {trainable:,}")
    return model
