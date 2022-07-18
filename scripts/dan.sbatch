#!/bin/bash
#SBATCH --partition=training

enroot_path=${ENROOT_PATH:-"/enroot_share/jona/jlo2020+ocr+dan.sqsh"}
code_path=${CODE_PATH:-"/home/jona/OCR/DAN/"}

srun  \
--container-image "$enroot_path"  \
--container-writable  \
--container-remap-root  \
--container-workdir /workspace/OCR/document_OCR/dan \
--container-mounts "$code_path":/workspace \
python main_dan.py
