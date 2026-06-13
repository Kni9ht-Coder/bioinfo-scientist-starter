from __future__ import annotations


def main() -> None:
    try:
        import torch
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"PyTorch is not installed in this environment: {exc}") from exc

    print(f"torch version: {torch.__version__}")
    print(f"cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"cuda device count: {torch.cuda.device_count()}")
        print(f"device 0: {torch.cuda.get_device_name(0)}")


if __name__ == "__main__":
    main()
