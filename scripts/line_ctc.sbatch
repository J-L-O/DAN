#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --partition=training
#SBATCH --nodelist=fb10dl07

enroot_path=${ENROOT_PATH:-"/enroot_share/jona/jlo2020+ocr+dan.sqsh"}
code_path=${CODE_PATH:-"/home/jona/OCR/DAN/"}

srun  \
--container-image "$enroot_path"  \
--container-writable  \
--container-remap-root  \
--container-workdir /workspace/OCR/line_OCR/ctc \
--container-mounts "$code_path":/workspace \
python main_line_ctc.py
