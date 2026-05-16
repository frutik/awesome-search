---
title: "GGUF in Practice: From Model to Production (Part 2)"
source: "https://medium.com/@michael.hannecke/gguf-in-practice-from-model-to-production-part-2-27c7eed23daa"
author:
  - "[[Michael Hannecke]]"
published: 2025-12-07
created: 2026-05-15
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*fep7ij_2WxKrlqsvb-Olxg.jpeg)

In [Part 1](https://medium.com/@michael.hannecke/gguf-optimization-a-technical-deep-dive-for-practitioners-ce84c8987944), we explored the theoretical foundations of GGUF and how quantization works under the hood. Now comes the practical payoff: converting models, running inference, and deploying to production. I learned most of this through trial and error on real projects, so I'll share what actually works.

If not a medium meber, access for free [here.](https://medium.com/@michael.hannecke/gguf-in-practice-from-model-to-production-part-2-27c7eed23daa?sk=ef45a92d5bd90912ecf2d7342b79dd60)

## Starting Point: Your Environment

Before diving into conversions, let's get the environment right. I've seen too many teams waste hours debugging issues that stem from missing dependencies or misconfigured GPU drivers.

### The Foundation

Your machine needs a few basics. For CPU-only work, 8GB RAM is the minimum, but I recommend 16GB or more if you're working with models above 3B parameters. For GPU acceleration, you'll need CUDA 11.7+ (12.x recommended) for NVIDIA cards, ROCm 5.0+ for AMD, or macOS 13+ for Apple Silicon.

**Ubuntu/Debian setup:**

```c
sudo apt update && sudo apt install -y \
    build-essential \
    cmake \
    git \
    python3 \
    python3-pip \
    python3-venv
```

**macOS (via Homebrew):**

```c
brew install cmake git python3
```

**Windows (via Chocolatey in PowerShell Admin):**

```c
choco install cmake git python3 visualstudio2022-workload-vctools
```

### Python Environment

I always use a virtual environment. Always. It prevents dependency conflicts that will haunt you later:

```c
python3 -m venv gguf-env
source gguf-env/bin/activate  # Linux/macOS
# gguf-env\Scripts\activate   # Windows
pip install --upgrade pip
pip install huggingface_hub transformers torch sentencepiece protobuf
```

## Building llama.cpp

The llama.cpp toolkit is your Swiss Army knife for GGUF work. You have several installation options, but I recommend building from source for maximum control.

### Option 1: Build from Source (My Preference)

```c
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
 
# Basic CPU build
cmake -B build
cmake --build build --config Release
 
# Verify it works
./build/bin/llama-cli --help
```

### Option 2: GPU-Accelerated Builds

For production work, GPU acceleration is essential. Here's how to build for different platforms:

**NVIDIA CUDA:**

```c
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j $(nproc)
```

**AMD ROCm:**

```c
cmake -B build -DGGML_HIP=ON
cmake --build build --config Release -j $(nproc)
```

**Apple Metal (macOS):**

```c
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

**Intel SYCL:**

```c
cmake -B build -DGGML_SYCL=ON
cmake --build build --config Release -j $(nproc)
```

**Vulkan (cross-platform):**

```c
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release -j $(nproc)
```

### Option 3: Package Managers

If you prefer convenience over control:

```c
# macOS/Linux
brew install llama.cpp
 
# Windows
winget install llama.cpp
 
# Verify
llama-cli --version
```

## Converting Models to GGUF

This is where the rubber meets the road. You've got a model on HuggingFace, and you need it in GGUF format.

### Step 1: Download the Model

I use the HuggingFace CLI for this. It's cleaner than cobbling together Python scripts:

```c
pip install huggingface_hub[cli]
 
# Login (required for gated models like LLaMA)
huggingface-cli login
 
# Download the model
# Note: meta-llama models require accepting Meta's license agreement on HuggingFace
huggingface-cli download meta-llama/Llama-3.2-3B-Instruct \
    --local-dir ./models/Llama-3.2-3B-Instruct
```

Or, if you prefer Python:

```c
from huggingface_hub import snapshot_download
 
MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
 
model_path = snapshot_download(
    repo_id=MODEL_ID,
    local_dir=f"./models/{MODEL_ID.split('/')[-1]}",
    local_dir_use_symlinks=False
)
 
print(f"Model downloaded to: {model_path}")
```

### Step 2: Convert to GGUF Format

The conversion script handles the heavy lifting. You'll want FP16 (16-bit floating point) as your base format:

```c
pip install -r llama.cpp/requirements.txt
 
python llama.cpp/convert_hf_to_gguf.py \
    ./models/Llama-3.2-3B-Instruct \
    --outtype f16 \
    --outfile ./models/Llama-3.2-3B-Instruct-f16.gguf
```

If your model was trained in BF16 (bfloat16), use that instead:

```c
python llama.cpp/convert_hf_to_gguf.py \
    ./models/Llama-3.2-3B-Instruct \
    --outtype bf16 \
    --outfile ./models/Llama-3.2-3B-Instruct-bf16.gguf
```

### Step 3: Verify the Conversion

Always verify. I've had conversions appear to succeed but produce corrupted files:

```c
./llama.cpp/build/bin/llama-cli \
    -m ./models/Llama-3.2-3B-Instruct-f16.gguf \
    --verbose-prompt \
    -p "Hello" \
    -n 1
```

If this runs without errors and produces output, your conversion worked.

## Quantization: Where the Magic Happens

FP16 models are huge. Quantization shrinks them dramatically while preserving most of the quality. In Part 1, we covered the theory. Here's how to do it in practice.

### Basic Quantization

Start with Q4\_K\_M. It's the sweet spot for most use cases:

```c
./llama.cpp/build/bin/llama-quantize \
    ./models/Llama-3.2-3B-Instruct-f16.gguf \
    ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    Q4_K_M
```

For higher quality (with larger files):

```c
./llama.cpp/build/bin/llama-quantize \
    ./models/Llama-3.2-3B-Instruct-f16.gguf \
    ./models/Llama-3.2-3B-Instruct-Q5_K_M.gguf \
    Q5_K_M
```

For near-lossless quality:

```c
./llama.cpp/build/bin/llama-quantize \
    ./models/Llama-3.2-3B-Instruct-f16.gguf \
    ./models/Llama-3.2-3B-Instruct-Q8_0.gguf \
    Q8_0
```

### Batch Quantization

In production, I generate multiple quantizations and benchmark them. Here's a script I use:

```c
#!/bin/bash
INPUT_MODEL="./models/Llama-3.2-3B-Instruct-f16.gguf"
OUTPUT_DIR="./models/quantized"
MODEL_NAME="Llama-3.2-3B-Instruct"
 
mkdir -p $OUTPUT_DIR
 
QUANT_TYPES=("Q4_K_M" "Q5_K_M" "Q6_K" "Q8_0" "IQ4_XS" "IQ3_M")
 
for QTYPE in "${QUANT_TYPES[@]}"; do
    echo "Quantizing to $QTYPE..."
    ./llama.cpp/build/bin/llama-quantize \
        $INPUT_MODEL \
        "${OUTPUT_DIR}/${MODEL_NAME}-${QTYPE}.gguf" \
        $QTYPE
 
    ls -lh "${OUTPUT_DIR}/${MODEL_NAME}-${QTYPE}.gguf"
done
 
echo "Quantization complete!"
```

### Understanding Quantization Types

Here's what each quantization type gives you (example results for a 7B parameter model):

- **Q4\_K\_M**: 4.58GB, +0.0535 ppl — The recommended default. Best balance.
- **Q5\_K\_M**: 5.33GB, +0.0142 ppl — Higher quality, slightly larger.
- **Q6\_K**: 6.14GB, +0.0044 ppl — Near-lossless, for quality-critical work.
- **Q8\_0**: 7.96GB, +0.0004 ppl — Barely any quality loss.
- **IQ4\_XS**: 4.25 bpw — Smaller than Q4, needs importance matrix.
- **IQ3\_M**: 3.66 bpw — Very small, needs importance matrix.
- **Q2\_K**: 2.96GB, +3.5199 ppl — Extreme compression, significant quality loss.

Lower perplexity (ppl) means better quality. The "IQ" (importance-quantization) types need an importance matrix to work well. Note that sizes and perplexity deltas vary by model architecture and size.

## Advanced Quantization with Importance Matrix

For aggressive quantization (IQ3, IQ2), you need an importance matrix. This tells the quantizer which weights matter most. It's extra work, but the quality improvement is worth it.

### Step 1: Prepare Calibration Data

Download a standard calibration dataset:

```c
# Option 1: WikiText-2 (official, stable)
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip
mv wikitext-2-raw/wiki.test.raw .
```

Or create your own. Good calibration data is diverse (different topics and styles) and substantial (1–5MB of text). Avoid domain-specific overfitting unless you know your use case is narrow.

### Step 2: Generate the Importance Matrix

This takes 30–60 minutes, depending on your hardware:

```c
./llama.cpp/build/bin/llama-imatrix \
    -m ./models/Llama-3.2-3B-Instruct-f16.gguf \
    -f wiki.test.raw \
    --chunk 512 \
    -o ./models/Llama-3.2-3B-imatrix.dat \
    -ngl 99  # Use GPU if available
```

Parameters:

- `-m`: Input model (FP16 or BF16 recommended)
- `-f`: Calibration data file
- `--chunk`: Chunk size for processing (512 is a good default)
- `-o`: Output importance matrix file
- `-ngl`: Number of GPU layers (99 = all)

### Step 3: Quantize with the Importance Matrix

Now quantize using the importance matrix:

```c
./llama.cpp/build/bin/llama-quantize \
    --imatrix ./models/Llama-3.2-3B-imatrix.dat \
    ./models/Llama-3.2-3B-Instruct-f16.gguf \
    ./models/Llama-3.2-3B-Instruct-IQ4_XS-imat.gguf \
    IQ4_XS
```

For very aggressive compression (IQ3\_M):

```c
./llama.cpp/build/bin/llama-quantize \
    --imatrix ./models/Llama-3.2-3B-imatrix.dat \
    ./models/Llama-3.2-3B-Instruct-f16.gguf \
    ./models/Llama-3.2-3B-Instruct-IQ3_M-imat.gguf \
    IQ3_M
```

For extreme compression (IQ2\_M):

```c
./llama.cpp/build/bin/llama-quantize \
    --imatrix ./models/Llama-3.2-3B-imatrix.dat \
    ./models/Llama-3.2-3B-Instruct-f16.gguf \
    ./models/Llama-3.2-3B-Instruct-IQ2_M-imat.gguf \
    IQ2_M
```

### Complete Pipeline Script

Here's the full workflow I use in production:

```c
#!/bin/bash
set -e  # Exit on error
 
MODEL_ID="meta-llama/Llama-3.2-3B-Instruct"
MODEL_NAME="Llama-3.2-3B-Instruct"
MODELS_DIR="./models"
LLAMA_CPP="./llama.cpp"
 
echo "=== Step 1: Download Model ==="
pip install huggingface_hub
python -c "
from huggingface_hub import snapshot_download
snapshot_download('${MODEL_ID}', local_dir='${MODELS_DIR}/${MODEL_NAME}')
"
 
echo "=== Step 2: Convert to GGUF F16 ==="
python ${LLAMA_CPP}/convert_hf_to_gguf.py \
    ${MODELS_DIR}/${MODEL_NAME} \
    --outtype f16 \
    --outfile ${MODELS_DIR}/${MODEL_NAME}-f16.gguf
 
echo "=== Step 3: Generate Importance Matrix ==="
if [ ! -f "wiki.test.raw" ]; then
    wget -q https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip
    unzip -q wikitext-2-raw-v1.zip
    mv wikitext-2-raw/wiki.test.raw .
fi
 
${LLAMA_CPP}/build/bin/llama-imatrix \
    -m ${MODELS_DIR}/${MODEL_NAME}-f16.gguf \
    -f wiki.test.raw \
    --chunk 512 \
    -o ${MODELS_DIR}/${MODEL_NAME}-imatrix.dat \
    -ngl 99
 
echo "=== Step 4: Quantize ==="
mkdir -p ${MODELS_DIR}/quantized
 
# Standard quants
for QTYPE in Q4_K_M Q5_K_M Q6_K Q8_0; do
    echo "Quantizing ${QTYPE}..."
    ${LLAMA_CPP}/build/bin/llama-quantize \
        ${MODELS_DIR}/${MODEL_NAME}-f16.gguf \
        ${MODELS_DIR}/quantized/${MODEL_NAME}-${QTYPE}.gguf \
        ${QTYPE}
done
 
# I-quants with importance matrix
for QTYPE in IQ4_XS IQ3_M IQ3_S IQ2_M; do
    echo "Quantizing ${QTYPE} with imatrix..."
    ${LLAMA_CPP}/build/bin/llama-quantize \
        --imatrix ${MODELS_DIR}/${MODEL_NAME}-imatrix.dat \
        ${MODELS_DIR}/${MODEL_NAME}-f16.gguf \
        ${MODELS_DIR}/quantized/${MODEL_NAME}-${QTYPE}.gguf \
        ${QTYPE}
done
 
echo "=== Complete! ==="
ls -lh ${MODELS_DIR}/quantized/
```

## Running Inference with llama.cpp

Now you have a quantized model. Let's run it.

### Basic Text Generation

```c
# Simple completion
./llama.cpp/build/bin/llama-cli \
    -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    -p "The capital of France is" \
    -n 50
 
# With system prompt and conversation mode
./llama.cpp/build/bin/llama-cli \
    -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    --chat-template llama3 \
    -cnv \
    -p "You are a helpful assistant."
```

### Interactive Chat Mode

For experimentation, interactive mode is invaluable:

```c
./llama.cpp/build/bin/llama-cli \
    -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    -cnv \
    --chat-template llama3 \
    -ngl 99 \
    -c 4096
```

Commands available in chat:

- `/quit` or `/exit` - End session
- `/clear` - Clear context
- `/save ` - Save conversation
- `/load ` - Load conversation

### Key CLI Parameters

Here are the parameters I use most often:

**Model loading:**

- `-m, --model `: Model file path
- `-ngl, --n-gpu-layers `: Layers to offload to GPU (99 = all)
- `-c, --ctx-size `: Context size (default: 2048)

**Generation control:**

- `-n, --predict `: Number of tokens to generate
- `-t, --threads `: CPU threads (default: auto)
- `--temp `: Temperature (0.0-2.0, default: 0.8)
- `--top-k `: Top-K sampling (default: 40)
- `--top-p `: Top-P (nucleus) sampling (default: 0.9)
- `--repeat-penalty `: Repetition penalty (default: 1.1)

**Chat/conversation:**

- `-cnv, --conversation`: Enable conversation mode
- `--chat-template `: Chat template (llama2, llama3, chatml, etc.)
- `-p, --prompt `: Initial prompt
- `-f, --file `: Read prompt from file

**Output control:**

- `--color`: Colorize output
- `--no-display-prompt`: Don't echo the prompt
- `-v, --verbose`: Verbose output
- `--log-file `: Log to file

### Running an OpenAI-Compatible Server

For production, you'll want a server. llama.cpp includes one:

```c
./llama.cpp/build/bin/llama-server \
    -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 99 \
    -c 4096
```

The server exposes OpenAI-compatible endpoints:

- `POST /v1/chat/completions`
- `POST /v1/completions`
- `POST /v1/embeddings`

### Using the Server with curl

Test the server with curl:

```c
# Chat completion
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "llama-3.2-3b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }'
 
# Text completion
curl http://localhost:8080/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "llama-3.2-3b",
        "prompt": "The meaning of life is",
        "max_tokens": 50,
        "temperature": 0.8
    }'
```

## Python Integration

For application development, Python is usually more convenient than the CLI.

### Installing llama-cpp-python

```c
# CPU-only
pip install llama-cpp-python
 
# With CUDA support (NVIDIA GPU)
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
 
# With Metal support (Apple Silicon)
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
 
# With ROCm support (AMD GPU)
CMAKE_ARGS="-DGGML_HIP=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
 
# With Vulkan support
CMAKE_ARGS="-DGGML_VULKAN=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### Basic Usage

```c
from llama_cpp import Llama
 
# Load model
llm = Llama(
    model_path="./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,        # Context window
    n_threads=8,       # CPU threads
    n_gpu_layers=-1,   # -1 = all layers on GPU
    verbose=False
)
 
# Simple completion
output = llm(
    "The capital of France is",
    max_tokens=32,
    stop=[".", "\n"],
    echo=False
)
print(output["choices"][0]["text"])
```

### Chat Completion

```c
from llama_cpp import Llama
 
# Load model with chat format
llm = Llama(
    model_path="./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=-1,
    chat_format="llama-3"  # or "chatml", "llama-2", etc.
)
 
# Chat completion
response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about programming."}
    ],
    max_tokens=100,
    temperature=0.7
)
 
print(response["choices"][0]["message"]["content"])
```

### Streaming Responses

For real-time applications:

```c
from llama_cpp import Llama
 
llm = Llama(
    model_path="./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=-1,
    chat_format="llama-3"
)
 
# Streaming chat
stream = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    max_tokens=500,
    stream=True
)
 
# Print tokens as they're generated
for chunk in stream:
    delta = chunk["choices"][0]["delta"]
    if "content" in delta:
        print(delta["content"], end="", flush=True)
print()
```

### Download from HuggingFace Directly

For downloading pre-quantized GGUF models:

```c
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
 
# Download model file
model_path = hf_hub_download(
    repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
    filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf"
)
 
# Load model
llm = Llama(
    model_path=model_path,
    n_gpu_layers=-1,
    verbose=False
)
 
response = llm.create_chat_completion(
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response["choices"][0]["message"]["content"])
```

### OpenAI-Compatible Server in Python

You can run an OpenAI-compatible server using the CLI invocation:

```c
# Start the server
python -m llama_cpp.server \
    --model ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    --n_gpu_layers -1 \
    --n_ctx 4096 \
    --chat_format llama-3 \
    --host 0.0.0.0 \
    --port 8000
```

### Using with OpenAI Python Client

Point the OpenAI client to your local server:

```c
from openai import OpenAI
 
# Point to local llama-cpp-python server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # Local server doesn't require API key
)
 
# Use exactly like OpenAI API
response = client.chat.completions.create(
    model="llama-3.2-3b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2+2?"}
    ],
    temperature=0.7,
    max_tokens=100
)
 
print(response.choices[0].message.content)
```

### Integration with LangChain

For more complex workflows (using LangChain Expression Language):

```c
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
 
# Initialize LlamaCpp LLM
llm = LlamaCpp(
    model_path="./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=4096,
    temperature=0.7,
    max_tokens=256,
    verbose=False
)
 
# Create a chain using LCEL
template = """Question: {question}
 
Answer: Let me think step by step."""
 
prompt = PromptTemplate(template=template, input_variables=["question"])
chain = prompt | llm
 
# Run the chain
response = chain.invoke({"question": "What causes rainbows?"})
print(response)
```

## Using Ollama for Easy Deployment

Ollama is the easiest way to run GGUF models if you don't need fine-grained control. I use it for quick experiments and demos.

### Installing Ollama

```c
# Linux
curl -fsSL https://ollama.com/install.sh | sh
 
# macOS
brew install ollama
 
# Windows
winget install ollama
 
# Verify
ollama --version
```

### Running Models from Ollama Library

```c
# Pull and run a model
ollama pull llama3.2:3b
ollama run llama3.2:3b
 
# Other popular models
ollama run mistral
ollama run codellama
ollama run phi3
ollama run gemma2
```

### Running GGUF from HuggingFace

This is brilliant: Ollama can run models directly from HuggingFace without downloading:

```c
# Direct from HuggingFace
ollama run hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF
 
# With specific quantization
ollama run hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:Q4_K_M
ollama run hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:IQ3_M
ollama run hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

### Importing Custom GGUF Files

For your own quantized models:

```c
# Create a Modelfile
cat > Modelfile << 'EOF'
FROM ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf
 
# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER stop "<|eot_id|>"
 
# System prompt
SYSTEM """You are a helpful, harmless, and honest assistant."""
 
# Chat template
TEMPLATE """{{ if .System }}<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>
{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>
{{ .Response }}<|eot_id|>"""
EOF
 
# Create the model in Ollama
ollama create my-llama3 -f Modelfile
 
# Run the model
ollama run my-llama3
```

### Ollama REST API

Ollama exposes a REST API:

```c
# Generate completion
curl http://localhost:11434/api/generate -d '{
    "model": "llama3.2:3b",
    "prompt": "Why is the sky blue?",
    "stream": false
}'
 
# Chat completion
curl http://localhost:11434/api/chat -d '{
    "model": "llama3.2:3b",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "stream": false
}'
 
# List models
curl http://localhost:11434/api/tags
 
# Model info
curl http://localhost:11434/api/show -d '{"name": "llama3.2:3b"}'
```

### Python with Ollama

```c
pip install ollama
```
```c
import ollama
 
# Simple generation
response = ollama.generate(
    model='llama3.2:3b',
    prompt='What is machine learning?'
)
print(response['response'])
 
# Chat
response = ollama.chat(
    model='llama3.2:3b',
    messages=[
        {'role': 'user', 'content': 'Explain neural networks simply'}
    ]
)
print(response['message']['content'])
 
# Streaming
for chunk in ollama.chat(
    model='llama3.2:3b',
    messages=[{'role': 'user', 'content': 'Write a poem about AI'}],
    stream=True
):
    print(chunk['message']['content'], end='', flush=True)
```

## GPU Acceleration Setup

CPU inference is fine for experimentation, but production workloads need GPUs. Here's how to set them up properly.

### NVIDIA CUDA Setup

```c
# 1. Install CUDA Toolkit (if not already installed)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-4
 
# 2. Set environment variables
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
 
# 3. Rebuild llama.cpp with CUDA
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j $(nproc)
 
# 4. Verify GPU detection
./build/bin/llama-cli -m model.gguf -ngl 99 --verbose
 
# Should show:
# ggml_cuda_init: found 1 CUDA devices:
#   Device 0: NVIDIA GeForce RTX 4090, compute capability 8.9
```

### AMD ROCm Setup

```c
# 1. Install ROCm (Ubuntu 22.04)
wget https://repo.radeon.com/amdgpu-install/5.7/ubuntu/jammy/amdgpu-install_5.7.50700-1_all.deb
sudo apt install ./amdgpu-install_5.7.50700-1_all.deb
sudo amdgpu-install -y --usecase=rocm
 
# 2. Add user to groups
sudo usermod -a -G render,video $USER
 
# 3. Rebuild llama.cpp with HIP
cd llama.cpp
cmake -B build -DGGML_HIP=ON
cmake --build build --config Release -j $(nproc)
 
# 4. Verify
./build/bin/llama-cli -m model.gguf -ngl 99 --verbose
```

### Apple Metal Setup

Metal is enabled by default on macOS, but rebuild for optimal performance:

```c
cd llama.cpp
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
 
# Verify Metal is being used
./build/bin/llama-cli -m model.gguf -ngl 99 --verbose
 
# Should show:
# ggml_metal_init: allocating
# ggml_metal_init: found device: Apple M3 Max
```

### GPU Layer Offloading Strategy

When VRAM is limited, you need to partially offload to GPU. Here's a helper function:

```c
def estimate_layers_for_vram(
    model_size_gb: float,
    vram_gb: float,
    total_layers: int,
    quant_type: str
) -> int:
    """
    Estimate how many layers can fit in VRAM.
 
    Args:
        model_size_gb: Total model size in GB
        vram_gb: Available VRAM in GB
        total_layers: Number of transformer layers
        quant_type: Quantization type (e.g., "Q4_K_M")
 
    Returns:
        Number of layers to offload
    """
    # Reserve ~1.5GB for KV cache and overhead
    available = vram_gb - 1.5
 
    # Calculate per-layer size
    size_per_layer = model_size_gb / total_layers
 
    # How many layers fit
    layers = int(available / size_per_layer)
 
    return min(layers, total_layers)
 
# Examples
print(estimate_layers_for_vram(4.0, 8.0, 32, "Q4_K_M"))   # ~52 layers (all fit)
print(estimate_layers_for_vram(8.0, 8.0, 80, "Q4_K_M"))   # ~65 layers (partial)
print(estimate_layers_for_vram(40.0, 24.0, 80, "Q4_K_M")) # ~45 layers (partial)
```

## Performance Tuning & Benchmarking

You need data to make informed decisions. Here's how I benchmark models.

### Running Benchmarks

```c
# Built-in benchmark tool
./llama.cpp/build/bin/llama-bench \
    -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    -ngl 99
 
# Output example:
# | model              | size    | params | backend    | threads | test       | t/s         |
# |--------------------|---------|--------|------------|---------|------------|-------------|
# | llama 3.2 3B Q4_K_M| 1.92 GB | 3.21B  | Metal,BLAS | 8       | pp512      | 2847.21±45  |
# | llama 3.2 3B Q4_K_M| 1.92 GB | 3.21B  | Metal,BLAS | 8       | tg128      | 87.54±2.1   |
# Compare different quantizations
for model in ./models/quantized/.gguf; do
    echo "Testing: $model"
    ./llama.cpp/build/bin/llama-bench -m "$model" -ngl 99
done
```

### Measuring Perplexity

*Perplexity measures model quality. Lower is better:*

```c
# Download test dataset
wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-raw-v1.zip
unzip wikitext-2-raw-v1.zip
 
# Run perplexity test
./llama.cpp/build/bin/llama-perplexity \
    -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
    -f wikitext-2-raw/wiki.test.raw \
    -ngl 99
 
# Output:
# Final estimate: PPL = 6.2345 +/- 0.0234
```

### Optimization Parameters

***CPU Optimization:***

```c
./llama.cpp/build/bin/llama-cli \
    -m model.gguf \
    -t 8 \           # CPU threads (try cores/2 for hyperthreading)
    -tb 16 \         # Batch processing threads
    --mlock \        # Lock model in memory (prevents swapping)
    --no-mmap        # Disable memory mapping (sometimes faster)
```

***GPU Optimization:***

```c
./llama.cpp/build/bin/llama-cli \
    -m model.gguf \
    -ngl 99 \        # All layers on GPU
    -c 4096 \        # Context size
    --flash-attn \   # Flash attention (if supported)
    -b 512           # Batch size for prompt processing
```

***Memory Optimization:***

```c
./llama.cpp/build/bin/llama-cli \
    -m model.gguf \
    -c 2048 \                    # Reduce context if needed
    --cache-type-k q8_0 \        # Quantized KV cache
    --cache-type-v q8_0
```

### Python Benchmarking Script

*For automated benchmarking:*

```c
import time
from llama_cpp import Llama
 
def benchmark_model(model_path: str, n_runs: int = 5):
    """Benchmark a GGUF model."""
 
    print(f"Loading: {model_path}")
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        n_gpu_layers=-1,
        verbose=False
    )
 
    # Warmup
    llm("Hello", max_tokens=1)
 
    # Test prompt
    prompt = "Explain the theory of relativity in simple terms."
 
    # Benchmark
    times = []
    tokens = []
 
    for i in range(n_runs):
        start = time.perf_counter()
        output = llm(prompt, max_tokens=100, echo=False)
        elapsed = time.perf_counter() - start
 
        n_tokens = output["usage"]["completion_tokens"]
        times.append(elapsed)
        tokens.append(n_tokens)
 
        print(f"  Run {i+1}: {n_tokens} tokens in {elapsed:.2f}s "
              f"({n_tokens/elapsed:.1f} tok/s)")
 
    avg_time = sum(times) / len(times)
    avg_tokens = sum(tokens) / len(tokens)
    avg_speed = avg_tokens / avg_time
 
    print(f"\n  Average: {avg_speed:.1f} tokens/second")
    return avg_speed
 
# Benchmark multiple models
models = [
    "./models/quantized/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    "./models/quantized/Llama-3.2-3B-Instruct-Q5_K_M.gguf",
    "./models/quantized/Llama-3.2-3B-Instruct-Q6_K.gguf",
]
 
results = {}
for model in models:
    results[model] = benchmark_model(model)
 
print("\n=== Summary ===")
for model, speed in sorted(results.items(), key=lambda x: -x[1]):
    print(f"{model}: {speed:.1f} tok/s")
```

## Troubleshooting Common Issues

*I've hit every one of these issues. Here's how to fix them.*

### Issue: Model Fails to Load

```c
# Error: "failed to open model"
# Solution: Check file path and permissions
ls -la ./models/.gguf
chmod 644 ./models/.gguf
 
# Error: "unsupported model architecture"
# Solution: Update llama.cpp to latest version
cd llama.cpp
git pull
cmake -B build -DGGML_CUDA=ON  # or your backend
cmake --build build --config Release
```

### Issue: Out of Memory

```c
# Error: "CUDA out of memory" or "failed to allocate"
# Solution 1: Reduce GPU layers
./llama.cpp/build/bin/llama-cli -m model.gguf -ngl 20  # Partial offload
 
# Solution 2: Use smaller quantization
./llama.cpp/build/bin/llama-quantize model-f16.gguf model-q4.gguf Q4_K_S
 
# Solution 3: Reduce context size
./llama.cpp/build/bin/llama-cli -m model.gguf -c 2048
 
# Solution 4: Use quantized KV cache
./llama.cpp/build/bin/llama-cli -m model.gguf \
    --cache-type-k q4_0 \
    --cache-type-v q4_0
```

### Issue: GPU Not Being Used

```c
# Check if CUDA is detected
./llama.cpp/build/bin/llama-cli -m model.gguf -ngl 99 --verbose 2>&1 | grep -i cuda
 
# If not detected, rebuild with CUDA
cd llama.cpp
rm -rf build
CMAKE_ARGS="-DGGML_CUDA=ON" cmake -B build
cmake --build build --config Release
 
# Verify CUDA installation
nvidia-smi
nvcc --version
```

### Issue: llama-cpp-python GPU Not Working

```c
# Check if GPU is being used
from llama_cpp import Llama
 
llm = Llama(
    model_path="model.gguf",
    n_gpu_layers=-1,
    verbose=True  # Shows backend info
)
 
# Should print:
# ggml_cuda_init: found X CUDA devices
# ...
# llm_load_tensors: offloading X layers to GPU
# If not working, reinstall with CUDA
# pip uninstall llama-cpp-python
# CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --no-cache-dir
```

### Issue: Slow Inference

```c
# Diagnosis: Check if memory-bound
./llama.cpp/build/bin/llama-bench -m model.gguf -ngl 0   # CPU only
./llama.cpp/build/bin/llama-bench -m model.gguf -ngl 99  # Full GPU
 
# If CPU is competitive, you're memory-bound
# Solution: Use smaller quant or increase GPU offload
# Check thread utilization
htop  # While running inference
# If CPU threads are idle, increase -t parameter
```

### Issue: Poor Output Quality

```c
# Possible causes:
# 1. Too aggressive quantization
#    Solution: Use higher bit quant (Q5_K_M instead of Q3_K_S)
# 2. Missing importance matrix for low-bit quants
#    Solution: Generate imatrix and re-quantize
# 3. Wrong chat template
#    Solution: Check model's chat format
./llama.cpp/build/bin/llama-cli -m model.gguf --chat-template llama3 -cnv
 
# 4. Context length exceeded
#    Solution: Increase context or use sliding window
./llama.cpp/build/bin/llama-cli -m model.gguf -c 8192
```

## Production Deployment Patterns

*Moving from experimentation to production requires some infrastructure.*

### Docker Deployment

```c
# Check https://hub.docker.com/r/nvidia/cuda for latest CUDA base images
FROM nvidia/cuda:12.4.0-devel-ubuntu22.04
 
# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/
 
# Clone and build llama.cpp
RUN git clone https://github.com/ggml-org/llama.cpp /llama.cpp
WORKDIR /llama.cpp
RUN cmake -B build -DGGML_CUDA=ON && \
    cmake --build build --config Release -j $(nproc)
 
# Install Python bindings
RUN CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python[server]
 
# Copy model (or mount as volume)
COPY ./models /models
 
# Expose port
EXPOSE 8000
 
# Run server
CMD ["python3", "-m", "llama_cpp.server", \
     "--model", "/models/model.gguf", \
     "--n_gpu_layers", "-1", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
```

Build and run:

```c
docker build -t llama-server .
docker run --gpus all -p 8000:8000 -v $(pwd)/models:/models llama-server
```

### Docker Compose with Multiple Models

```c
version: '3.8'
 
services:
  llama-server:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - MODEL_PATH=/models/llama-3.2-3b-q4_k_m.gguf
      - N_GPU_LAYERS=-1
      - N_CTX=4096
    restart: unless-stopped
 
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - llama-server
```

### Kubernetes Deployment

```c
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llama-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llama-server
  template:
    metadata:
      labels:
        app: llama-server
    spec:
      containers:
      - name: llama-server
        image: your-registry/llama-server:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "16Gi"
          requests:
            nvidia.com/gpu: 1
            memory: "8Gi"
        volumeMounts:
        - name: models
          mountPath: /models
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: models-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: llama-service
spec:
  selector:
    app: llama-server
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Health Checks and Monitoring

```c
from fastapi import FastAPI, HTTPException
from llama_cpp import Llama
import time
 
app = FastAPI()
llm = None
model_loaded_time = None
 
@app.on_event("startup")
async def load_model():
    global llm, model_loaded_time
    llm = Llama(
        model_path="/models/model.gguf",
        n_gpu_layers=-1,
        n_ctx=4096
    )
    model_loaded_time = time.time()
 
@app.get("/health")
async def health():
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "status": "healthy",
        "model_loaded": True,
        "uptime_seconds": time.time() - model_loaded_time
    }
 
@app.get("/ready")
async def ready():
    if llm is None:
        raise HTTPException(status_code=503, detail="Not ready")
    # Quick inference test
    try:
        llm("test", max_tokens=1)
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

## Quick Reference Card

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zEpbqcOCuy_riURIx2q6Nw.jpeg)

## Where to Go From Here

GGUF and llama.cpp give you everything you need to run language models efficiently on your own infrastructure. Start with the basics (convert a model, quantize it, run inference), then expand to production patterns as your needs grow.

The key lessons I've learned:

- Start with Q4\_K\_M quantization. It's the sweet spot.
- Always benchmark before committing to a quantization strategy.
- GPU acceleration is worth the setup effort for production workloads.
- Importance matrices make a real difference for aggressive quantization.
- Ollama is great for quick experiments; llama.cpp is better for production control.

In Part 1, we covered the theory. Now you have the practice. Go build something.

This article reflects my professional perspective. Drafting was assisted by Claude, but the insights and final curation are entirely my own.