@echo off
echo Installing CUDA-enabled PyTorch...
uv pip install torch==2.4.1+cu121 --index-url https://download.pytorch.org/whl/cu121

echo.
echo Testing CUDA...
.venv\Scripts\python.exe -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

echo.
echo Done! Press any key to exit...
pause